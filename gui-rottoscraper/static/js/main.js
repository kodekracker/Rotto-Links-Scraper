//asdf
$(document).ready(function(){

	$(".btn").click(function(e){
		var $this   = $(this);
		$(".steps").animate({"margin-left":"-=660px"},500, function(){
			// callback action
		});
	});
	e.preventDefault();
});
