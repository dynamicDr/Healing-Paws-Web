$(document).ready(function(){
	// add all event handlers here
	console.log("Adding event handlers");
	$(".question").click(function () {
		let index = $(".question").index(this);
		$.post('/answerquestion', {
			'index': index 
		})
	});
	console.log("function registered");
});