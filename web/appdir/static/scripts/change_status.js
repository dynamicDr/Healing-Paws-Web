$(document).ready(function(){
	$("#status").on("change", change_status);
	console.log("function registered");
});

function change_status(){
    var status_str = $(this).val();
    var apt_id = $("#apt_id").html();
	console.log(status_str);
	console.log(apt_id);

	$("#check_update").html('<img src="static/images/loading.gif">');

	// // ajax code 
	$.get('/set_status', {
        'apt_id': apt_id,
		'status': status_str
	}).done(function (response){
		var server_response = response['text']
		var server_code = response['returnvalue']
		if (server_code == 0){ // success: 
			$("#check_update").html('<span>' + server_response + '</span>');
			$("#check_update").addClass("success");
			$("#check_update").removeClass("failure");
		}
	}).fail(function() {
		$("#check_update").html('<span>Error contacting server</span>');
		$("#check_update").addClass("failure");
	});
	// end of ajax code
	
	console.log("finished change");
}