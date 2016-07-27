/**
 * common $resources for shifts
 */
(function(angular) {
    'use strict';

    angular.module('signup.common.services.Shift', [
        'ngResource',
        'signup.common.constants'
    ])

    .factory('common.Shift', ['$resource', 'SIGNUP_URLS', function($resource, SIGNUP_URLS) {
        return $resource(SIGNUP_URLS.SHIFT, {id: '@id'}, {
            update: {method: 'PUT', isArray: false}
        });
    }])

    .factory('common.Shifts', ['$resource', 'SIGNUP_URLS', function($resource, SIGNUP_URLS) {
        return $resource(SIGNUP_URLS.SHIFTS);
    }])

    ;

})(window.angular);
