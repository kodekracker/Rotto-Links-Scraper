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
        }).when('/result/:jobId', {
            templateUrl: '../static/html/result.html',
            controller: 'ResultController'
        }).otherwise({ redirectTo : '/' });
});
/* End of App Configuration   */

/* App Controllers */
app.controller('RottoController',function($scope,$location,$http){
    $scope.userDetails = {};
    $scope.isFormComplete = false;
    $scope.showMessage = false;
    $scope.currentStepId = 1;
    $scope.jobDetails = 'null';
    $scope.job_url = 'null';
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
        var url = 'http://localhost:5000/api/v1.0/crawl/';
        $http.post(url,$scope.userDetails).success(function(data,status){
            $scope.jobDetails = data;
            $scope.job_url = makeJobUrl($scope.jobDetails.job_id);
            console.log("success");
            console.log($scope.jobDetails);
             $scope.showMessage = true;
        }).error(function(data,status){
            console.log("failure");
            $scope.userDetails = data || "Request failed";
            console.log($scope.jobDetails);
            $scope.showMessage = true;
        });
    }

    function getKeys(data){
        var arr = [];
        for (var i in data){
            arr.push(data[i].text)
        }
        return arr;
    };

    function makeJobUrl(job_key){
        var url = 'http://localhost:5000/#/result/'+job_key;
        return url;
    };
});


app.controller('ResultController',function($scope,$location,$routeParams,$http){
    $scope.jobId = $routeParams.jobId;
    $scope.isError = false;
    $scope.jobDetails = {};
    var url = 'http://localhost:5000/api/v1.0/crawl/'+$scope.jobId;


    $http.get(url).success(function(data, status, headers, config){
        console.log(data);
        if(status=='202'){
            $scope.isError = true;
            $scope.errorMessage = data.error;
        }else{
            $scope.jobDetails = data;
        }
    }).error(function(data, status, headers, config){
        $scope.isError = true;
        $scope.errorMessage = 'Error in Request, Please Try Again.';
    });
});
