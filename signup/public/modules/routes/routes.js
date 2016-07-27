(function(angular) {
    'use strict';

    /**
     * This module requires all routes.
     *
     * The main app depends on this module, which provides a convenient way to
     * import all routes. Each route module in turn depends on the module or
     * modules that contain its controllers, services and directives.
     *
     * Be sure to add your route module below when adding new pages.
     */
    angular.module('signup.routes', [
        // Keep this list alphabetized!
        'ui.router',
        'signup.common'
    ])

    .config([
        '$urlRouterProvider',
        '$stateProvider',
        function($urlRouterProvider, $stateProvider) {
            // default url
            $urlRouterProvider.otherwise('/signup');

            $stateProvider.state('signup', {
                url: '/signup',
                views: {
                    main: {
                        controller: 'common.MainCtrl',
                        templateUrl: 'modules/common/views/main.html'
                    }
                }
            });

            $stateProvider.state('shift', {
                url: '/shift/:shiftId',
                views: {
                    main: {
                        controller: 'common.ShiftCtrl',
                        templateUrl: 'modules/common/views/shift.html'
                    },
                }
            });

        }])
    ;
}(window.angular));
