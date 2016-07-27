(function(angular) {
    'use strict';

    angular.module('signup.common.controllers.MainCtrl', [
        'ngResource',
        'ngCookies',
        'ui.bootstrap',
        'signup.common',
    ])

    /*
     * Main controller
     */
    .controller('common.MainCtrl', [
        '$scope',
        '$cookies',
        '$log',
        'common.Shifts',
        function MainCtrl($scope, $cookies, $log, Shifts) {
            $scope.cocAccepted = $cookies.cocAccepted;
            $scope.$log = $log;

            Shifts.get().$promise.then(function(shifts) {
                $scope.shifts = shifts.shifts;
            }, function() {
                $scope.error = 'Failed to load shifts';
                $log.log($scope.error);
            });

            $scope.acceptCOC = function() {
                $cookies.cocAccepted = true;
                $scope.cocAccepted = true;
            };

    }])

    ;
}(window.angular));
