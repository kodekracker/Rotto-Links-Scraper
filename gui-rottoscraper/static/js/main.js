//asdf
$(document).ready(function(){

	$(".btn").click(function(e){
		$(".steps").animate({"margin-left":"-=660px"},500, function(){
			// callback action
		});

        e.preventDefault();
	});
});
