$(document).ready(function(){
	// add all event handlers here
	console.log("Adding event handlers");
	$(".question li").click(function () {
		let index = $(".question li").index(this);
		$.post('/answerquestion', {
			'index': index 
		})
	});
	console.log("function registered");
});