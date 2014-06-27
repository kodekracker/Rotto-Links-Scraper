/* Angular JS App File */
var app = angular.module('RottoApp',[]);

/* App Configuration */

app.config(['$routeProvider', function($routeProvider){
        // provide routes
        $routeProvider.when('/', {
            templateUrl: '../static/html/index.html',
            controller: 'RottoController'
        }).otherwise({ redirectTo : '/' });
}]);
/* End of App Configuration   */

/* App Controllers */
app.controller('RottoController',['$scope',function($scope){
    $scope.url = 'None';
    $scope.keywords = 'None';
    $scope.emailId = 'None';
    $scope.showForm = true;
    $scope.showMessage = false;
    $scope.limit = 10;

    $scope.showNextStep = function(event){
        event.preventDefault();
        event.stopPropagation();
        var id = get_curr_step_id();
        id = parseInt(id)+1;
        set_step_selected(id);
    };

    $scope.showStep = function(id){
        set_step_selected(id);
    };
    $scope.submitForm = function(isValid){
        // submit form
        if (isValid) {
            $scope.showForm = false;
            $scope.showMessage = true;
        }else{
            alert("Please correct all inputs.")
        }
    };
}]);
/* End of App Controllers */


/* Utility Fuction */
function get_cur_step(){
    var curr_step = $('div').find('.selected');
    return curr_step;
}
function get_curr_step_id(){
    var curr_step = get_cur_step();
    var id = curr_step.attr('id');
    return id;
}
function set_step_selected(id) {
    var marginValue = -(id-1)*660;
    get_cur_step().removeClass('selected');
    var step = "[id="+id+"]";
    $("[id=2]").addClass("selected");
    $(".steps").animate({"margin-left":marginValue},300, function(){
        // callback action
    });
}
