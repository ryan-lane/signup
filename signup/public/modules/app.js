(function(angular) {
'use strict';

    angular.module('signupApp', [
        // external libs
        'ngRoute',

        // load routes
        'signup.routes'
    ])

    /*
     * Main controller
     */
    .controller('SignupMainCtrl', [
        '$scope',
        '$log',
        function SignupMainCtrl($scope, $log) {
    }])

    ;

})(window.angular);
