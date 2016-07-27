(function(angular) {
    'use strict';


    /**
     * This module requires all common services.
     *
     * It mainly provides a convenient way to import all common services by only
     * requiring a dependency on a single module.
     *
     */
    angular.module('signup.common.services', [
        // Keep this list sorted alphabetically!
        'signup.common.services.NavService',
        'signup.common.services.Shift'
    ])
    ;
}(angular));
