(function(){

    var routineAppServices = angular.module('routineApp.services', []);

    var domain = 'http://127.0.0.1:8000/';

    routineAppServices.factory("RoutineService", ['$http', function($http, AuthUser){

        var routine = {};

        routine.getRoutines = function() {
            return $http.get(domain + 'routines/routines/');
        };

        routine.getRoutine = function(routineId) {
            return $http.get(domain + 'routines/routines/' + routineId);
        };

        routine.createRoutine = function(routineJson) {
            return $http.post(domain + 'routines/routines/', routineJson);
        };

        routine.editRoutine = function(routineJson, routineId) {
            return $http.put(domain + 'routines/routines/' + routineId +'/', routineJson);
        };

        routine.deleteRoutine = function(routineId) {
            return $http.delete(domain + 'routines/routines/' + routineId + '/');
        };

        routine.getExercises = function(routineId) {
            return $http.get(domain + 'routines/exercises/', {
                params: {
                    routineId: routineId
                }
            });
        }

        routine.createExercises = function(exercisesJson) {
            return $http.post(domain + 'routines/exercises/create-many/', exercisesJson);
        };

        routine.createExercise = function(exerciseJson) {
            return $http.post(domain + 'routines/exercises/', exerciseJson)
        };

        routine.editExercise = function(exerciseJson, exerciseId) {
            return $http.put(domain + 'routines/exercises/' + exerciseId + '/', exerciseJson)
        };

        routine.deleteExercise = function(exerciseId) {
            return $http.delete(domain + 'routines/exercises/' + exerciseId + '/');
        };

        return routine;

    }]);

    routineAppServices.factory("SharedProperties", function() {

        var property = {};

        var value;

        property.getProperty = function() {
            return value;
        };

        property.setProperty = function(newValue) {
            value = newValue;
        };

        return property;

    });

})();
