$(document).ready(function(){
	// add all event handlers here
	console.log("Adding event handlers");
	$("[name='delete']").on("click", delete_pet);
	console.log("function registered");
});

function delete_pet(){

	console.log("delete_pet() called");
	var pet_id = $(this).parent().next();
    console.log("pet id: " + pet_id.html());
	
	// // ajax code 
	$.get('/delete_pet', {
		'id': pet_id.html() //field value being sent to the server
	}).done(function (response){
		var server_response = response['text']
		var server_code = response['returnvalue']
		console.log(server_code)
        if (server_code == 0){
			console.log(pet_id.parent());
            pet_id.parent().hide();
		}else{ 
            alert("This pet cannot be delete now.\nIt still has appointment(s).");
		}
	}).fail(function() {
		alert("fail to connect server")
	});
	// end of ajax code
	
	console.log("finished delete_pet");
}