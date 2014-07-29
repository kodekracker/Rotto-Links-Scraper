/* Angular JS App File */
var app = angular.module('RottoApp',[
    'ngRoute',
    'ngTagsInput'
    ]);

/* App Configuration */
app.config(function($routeProvider){
        // provide routes
        $routeProvider.when('/', {
            templateUrl: '../static/html/index.html',
            controller: 'RottoController'
        }).when('/result/:websiteId', {
            templateUrl: '../static/html/result.html',
            controller: 'ResultController'
        }).otherwise({ redirectTo : '/' });
});
/* End of App Configuration   */

/* App Controllers */
app.controller('RottoController',function($scope,$location,$http){
    $scope.userDetails = {};
    $scope.formFilling = true
    $scope.confirmDetails = false;
    $scope.showMessage = false;
    $scope.currentStepId = 1;
    $scope.jobDetails = 'null';
    $scope.error = {'status':false}

    $scope.showStep = function(id){
        $scope.currentStepId = id;
    };

    $scope.confirmFormDetails = function(isValid){
        // submit form
        console.log('Conform');
        if (isValid) {
            $scope.userDetails.url = $scope.url || 'None';
            $scope.userDetails.keywords = getKeywordsArray($scope.keywords) || 'None';
            $scope.userDetails.email_id = $scope.email || 'None' ;
            console.log($scope.userDetails);
            $scope.formFilling = false;
            $scope.confirmDetails = true;
        }else{
            alert("Please correct all inputs.")
        }
    };

    $scope.cancelRequest = function(){
        console.log('cancel');
        $location.url('/');
    };

    $scope.submitRequest = function(){
        var url = 'http://localhost:5000/api/v1.0/crawl/';
        console.log($scope.userDetails);
        $scope.confirmDetails = false
        $http.post(url,$scope.userDetails).success(function(data,status){
            console.log("success");
            console.log(data);
            if(status!==200){
                $scope.error.status = true;
                $scope.error.message = data.error
            }else
                $scope.showMessage = true;
        }).error(function(data,status){
            console.log("failure");
            $scope.error.status = true;
            $scope.error.message = data
        });
    }

    function getKeywordsArray(data){
        var arr = [];
        for (var i in data){
            arr.push(data[i].text)
        }
        return arr;
    };
});


app.controller('ResultController',function($scope,$location,$routeParams,$http){
    $scope.websiteId = $routeParams.websiteId;
    $scope.error = {'status':false};
    $scope.website = {};

    var url = 'http://localhost:5000/api/v1.0/crawl/'+$scope.jobId;
    $http.get(url).success(function(data, status, headers, config){
        console.log(data);
        if(status!==200){
            $scope.error.status = true;
            $scope.error.message = data.error;
        }else{
            $scope.website = data;
        }
    }).error(function(data, status, headers, config){
        $scope.error.status = true;
        $scope.error.message = 'Error in Request, Please Try Again.';
    });
});
