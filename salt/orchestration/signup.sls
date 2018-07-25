# Fail if required environment variables aren't passed in.
{% for var in ['service_name', 'service_instance', 'region'] %}
{% if not grains.get(var, None) %}
{{ var.upper() }} environment variable check:
    test.configurable_test_state:
        - name: {{ var.upper() }} environment variable not set
        - comment: {{ var.upper() }} environment variable must be set
        - failhard: True
        - changes: False
        - result: False
{% endif %}
{% endfor %}

Ensure {{ grains.cluster_name }}-2017 DynamoDB table exists:
  boto_dynamodb.present:
    - name: {{ grains.cluster_name }}-2017
    - read_capacity_units: 10
    - write_capacity_units: 10
    - hash_key: shift_id
    - hash_key_data_type: S
    - profile: orchestration_profile

Ensure {{ grains.cluster_name }}-2018 DynamoDB table exists:
  boto_dynamodb.present:
    - name: {{ grains.cluster_name }}-2018
    - read_capacity_units: 10
    - write_capacity_units: 10
    - hash_key: shift_id
    - hash_key_data_type: S
    - profile: orchestration_profile

Ensure elb-external security group exists:
  boto_secgroup.present:
    - name: elb-external
    - description: elb-external
    - vpc_id: {{ pillar.vpc_id }}
    - rules:
        - ip_protocol: tcp
          from_port: 80
          to_port: 80
          cidr_ip:
            - 0.0.0.0/0
        - ip_protocol: tcp
          from_port: 443
          to_port: 443
          cidr_ip:
            - 0.0.0.0/0
    - profile: orchestration_profile

Ensure {{ grains.cluster_name }} security group exists:
  boto_secgroup.present:
    - name: {{ grains.cluster_name }}
    - description: {{ grains.cluster_name }}
    - vpc_id: {{ pillar.vpc_id }}
    - rules:
        # TLS terminated traffic from the ELB
        - ip_protocol: tcp
          from_port: 80
          to_port: 80
          source_group_name:
            - elb-external
    - profile: orchestration_profile

Ensure {{ grains.cluster_name }} iam role exists:
  boto_iam_role.present:
    - name: {{ grains.cluster_name }}
    - policies:
        'iam':
          Version: '2012-10-17'
          Statement:
            - Action:
                - 'iam:ListRoles'
                - 'iam:GetRole'
              Effect: 'Allow'
              Resource: '*'
        'kms':
          Version: '2012-10-17'
          Statement:
            - Action:
                - 'kms:GenerateRandom'
              Effect: 'Allow'
              Resource: '*'
        'dynamodb':
          Version: '2012-10-17'
          Statement:
            - Action:
                - 'dynamodb:*'
              Effect: 'Allow'
              Resource:
                - 'arn:aws:dynamodb:*:*:table/{{ grains.cluster_name }}'
                - 'arn:aws:dynamodb:*:*:table/{{ grains.cluster_name }}/*'
                - 'arn:aws:dynamodb:*:*:table/{{ grains.cluster_name }}-2017'
                - 'arn:aws:dynamodb:*:*:table/{{ grains.cluster_name }}-2017/*'
            - Action:
                - 'dynamodb:DeleteTable'
              Effect: 'Deny'
              Resource:
                - 'arn:aws:dynamodb:*:*:table/{{ grains.cluster_name }}'
                - 'arn:aws:dynamodb:*:*:table/{{ grains.cluster_name }}-2017'
    - profile: orchestration_profile

Ensure {{ grains.cluster_name }} elb exists:
  boto_elb.present:
    - name: {{ grains.cluster_name }}
    - subnets: {{ pillar.vpc_subnets }}
    - scheme: internet-facing
    - security_groups:
        - elb-external
        - {{ grains.cluster_name }}
    - listeners:
        - elb_port: 80
          instance_port: 80
          elb_protocol: HTTP
          instance_protocol: HTTP
        {% if pillar.get('elb_cert', '') %}
        - elb_port: 443
          instance_port: 80
          elb_protocol: HTTPS
          instance_protocol: HTTP
          certificate: '{{ pillar.elb_cert }}'
        {% endif %}
    - health_check:
        target: 'HTTP:80/healthcheck'
        timeout: 4
        interval: 5
        healthy_threshold: 3
        unhealthy_threshold: 8
    {% if pillar.get('dns_domain', '') %}
    - cnames:
        - name: {{ grains.cluster_name }}.{{ pillar.dns_domain }}
          zone: {{ pillar.dns_domain }}
        {% if pillar.get('custom_dns', {}).get(grains.cluster_name, '') %}
        - name: {{ pillar.custom_dns.get(grains.cluster_name) }}.{{ pillar.dns_domain }}
          zone: {{ pillar.dns_domain }}
        {% endif %}
    {% endif %}
    - profile: orchestration_profile

Ensure {{ grains.cluster_name }} asg exists:
  boto_asg.present:
    - name: {{ grains.cluster_name }}
    - launch_config_name: {{ grains.cluster_name }}
    - launch_config:
      # TODO: load this from pillars. This specific AMI is us-east-1, ubuntu
      # trusty, hvm-ssd
      - image_id: ami-3bdd502c
      - key_name: {{ pillar.ssh_boot_key_name }}
      - security_groups:
        - base
        - {{ grains.cluster_name }}
      - instance_profile_name: {{ grains.cluster_name }}
      # TODO: load this from pillars
      - instance_type: t2.nano
      - associate_public_ip_address: True
      - instance_monitoring: true
      - cloud_init:
          scripts:
            salt: |
              #!/bin/bash
              apt-get -y update
              apt-get -y install python python-virtualenv python-pip python-dev build-essential libffi-dev ruby-full npm nodejs nodejs-legacy git git-core libxml2-dev libxmlsec1-dev
              cd /srv
              git clone https://github.com/ryan-lane/signup
              cd /srv/signup
              virtualenv venv
              source venv/bin/activate
              pip install -U pip
              pip install -r piptools_requirements.txt
              pip install -r requirements.txt
              deactivate
              gem install compass
              npm install grunt-cli
              npm install
              node_modules/grunt-cli/bin/grunt build
              cat << EOF > /srv/signup/service.env
              {% for key, val in pillar.signup_env.items() -%}
              export {{ key }}='{{ val }}'
              {% endfor -%}
              EOF
              cat << EOF > /etc/init/signup.conf
              description "signup"
              start on (filesystem)
              stop on runlevel [016]
              respawn
              script
                . /srv/signup/service.env
                cd /srv/signup
                exec /srv/signup/venv/bin/gunicorn wsgi:app --workers=2 -k gevent
              end script
              EOF
              service signup start
    - vpc_zone_identifier: {{ pillar.vpc_subnets }}
    - availability_zones: {{ pillar.availability_zones }}
    - min_size: 3
    - max_size: 3
    - desired_capacity: 3
    - load_balancers:
      - {{ grains.cluster_name }}
    - tags:
      - key: 'Name'
        value: '{{ grains.cluster_name }}'
        propagate_at_launch: true
    - profile: orchestration_profile
