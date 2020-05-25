$(document).ready(function(){
	$("#status").on("change", change_status);
	console.log("function registered");
});

function change_status(){
    var status_str = $(this).val();
    var apt_id = $("#apt_id").html();
	console.log(status_str);
	console.log(apt_id)
	// // ajax code 
	$.get('/set_status', {
        'apt_id': apt_id,
		'status': status_str
	});
	// end of ajax code
	
	console.log("finished change");
}