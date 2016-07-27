/**
 * Common constants
 *
 * An example common module that defines constants.
 */

(function(angular) {
    'use strict';

    angular.module('signup.common.constants', [])

    .constant('SIGNUP_URLS', {
        SHIFT: 'v1/shift/:id',
        SHIFTS: 'v1/shifts'
    })

    ;

})(window.angular);
