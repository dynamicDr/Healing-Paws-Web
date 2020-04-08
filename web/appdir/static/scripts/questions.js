$(document).ready(function(){
	// add all event handlers here
	console.log("Adding event handlers");
	$(".question li").click(function () {
		let index = $(".question li").index(this);
		$.post('/answerquestion', {
			'index': index 
		})
	});

	$("#search").find("button").on("click", search);  

	console.log("function registered");
});

function search(){
    var input = $("#search").find("input");
    var keyword = input.val();
    window.location.replace("reviewquestions?page=1&key="+keyword);
    
}