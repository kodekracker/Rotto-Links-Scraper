/* Angular JS App File */
var app = angular.module('RottoApp',[
    'ngRoute',
    'ngTagsInput'
    ]);

/* App Configuration */

app.config(['$routeProvider', function($routeProvider){
        // provide routes
        $routeProvider.when('/', {
            templateUrl: '../static/html/index.html',
            controller: 'RottoController'
        }).when('/result/:job_id', {
            templateUrl: '../static/html/result.html',
            controller: 'ResultController'
        }).otherwise({ redirectTo : '/' });
}]);
/* End of App Configuration   */

/* App Controllers */
app.controller('RottoController',['$scope','$location',function($scope,$location){
    $scope.userDetails = {};
    $scope.isFormComplete = false;
    $scope.showMessage = false;
    $scope.currentStepId = 1;

    $scope.showStep = function(id){
        if(id==2)
            $scope.userDetails.url = $scope.url || 'None';
        else if(id==3){
            $scope.userDetails.keywords = getKeys($scope.keywords) || 'None';
        }

        $scope.currentStepId = id;
    };

    $scope.confirmFormDetails = function(isValid,data){
        // submit form
        $scope.userDetails.email = $scope.email || 'None' ;
        if (isValid) {

        console.log($scope.userDetails);
            $scope.isFormComplete = true;
        }else{
            alert("Please correct all inputs.")
        }
    };

    $scope.cancelRequest = function(){
        $location.url('#/');
    }

    $scope.submitRequest = function(){
        $scope.showMessage = true;
    }

    function getKeys(data){
        var arr = [];
        for (var i in data){
            arr.push(data[i].text)
        }
        return arr;
    };
}]);

app.controller('ResultController',['$scope','$routeParams',function($scope,$routeParams){
    $scope.job_id = $routeParams.job_id;
}]);