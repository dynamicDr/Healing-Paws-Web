$(document).ready(function(){
	// add all event handlers here
	console.log("Adding event handlers");
	$("#username").on("change", check_username);
    $("#email").on("change", check_email);
	$("#birthday").on("change", check_birthday);
	$("#password").on("change", check_password);
	$("#password2").on("change", check_password2);
	console.log("function registered");
});

function check_username(){
    $("#username").find(".flash").hide();
	// get the source element
	console.log("check_username called");
	var chosen_user = $(this).find("input");
	console.log("User chose: " + chosen_user.val());
	
	$("#checkuser").removeClass();
	$("#checkuser").html('<img src="static/images/loading.gif">');
	
	// ajax code 
	$.post('/checkuser', {
		'username': chosen_user.val() //field value being sent to the server
	}).done(function (response){
		var server_response = response['text']
		var server_code = response['returnvalue']
		if (server_code == 0){ // success: Username does not exist in the database
			$("#username").focus();
			$("#checkuser").html('<span>' + server_response + '</span>');
			$("#checkuser").addClass("success");
			$("#checkuser").removeClass("failure");
		}else{ // failure: Username already exists in the database
			chosen_user.val("");
			chosen_user.focus();
			$("#checkuser").html('<span>' + server_response + '</span>');
			$("#checkuser").addClass("failure");
            $("#checkuser").removeClass("success");
		}
	}).fail(function() {
		$("#checkuser").html('<span>Error contacting server</span>');
		$("#checkuser").addClass("failure");
	});
	// end of ajax code
	
	console.log("finished check_username");
}
function check_email(){
    $("#email").find(".flash").hide();
	console.log("check_email called");
	var email = $(this).find("input");
	console.log("email input: " + email.val());
	var reg = /^[\w\.]+@([a-z0-9]+\.)+[a-z0-9]+$/g
	if(reg.test(email.val()) &&  !/\.\./.test(email.val())){
		$("#checkemail").html('<span>Valid Email</span>');
		$("#checkemail").addClass("success");
		$("#checkemail").removeClass("failure");
	}else{
		email.val("");
		// $("#email").focus();
		setTimeout(function(){email.focus()},0); //https://www.cnblogs.com/djh-create/p/5511277.html
		$("#checkemail").html('<span>Invalid Email</span>');
		$("#checkemail").addClass("failure");
        $("#checkemail").removeClass("success");
	}
}

function check_birthday(){
	$("#birthday").find(".flash").hide();
	console.log($("#birthday").find(".flash"))
    var bd = $(this).find("input");
    
    var reg = /^(\d{4})\-(\d{2})\-(\d{2})$/g;
    console.log(bd.val()+ " " + reg.test(bd))
    if(reg.test(bd.val())){
		$("#checkdob").html('<span>Valid Format</span>');
		$("#checkdob").addClass("success");
        $("#checkdob").removeClass("failure");
    }else{//格式错误
        bd.val("");
		// bd.focus();
		setTimeout(function(){bd.focus()},0); //https://www.cnblogs.com/djh-create/p/5511277.html
		$("#checkdob").html('<span>Wrong Format! (YYYY-MM-DD)</span>');
		$("#checkdob").addClass("failure");
        $("#checkdob").removeClass("success");
    }
    
}

function check_password(){
    $("#password").find(".flash").hide();
    console.log("check_password called");
	var password = $(this);
	var password_str = password.val()
    if(password_str.length < 8){//长度太短
        password.val("");
		setTimeout(function(){password.focus()},0); //https://www.cnblogs.com/djh-create/p/5511277.html
        $("#checkpassword").html('<span>The password should longer than 8</span>');
		$("#checkpassword").addClass("failure");
		$("#checkpassword").removeClass("success");
	}else if(/\W/.test(password_str)){//需要英文字母和数字
		password.val("");
		setTimeout(function(){password.focus()},0); //https://www.cnblogs.com/djh-create/p/5511277.html
        $("#checkpassword").html('<span>The password should only contain letters, numbers and _</span>');
		$("#checkpassword").addClass("failure");
		$("#checkpassword").removeClass("success");
	}else if(!(/\d/.test(password_str) && /[a-zA-Z]/.test(password_str))){
		password.val("");
		setTimeout(function(){password.focus()},0); //https://www.cnblogs.com/djh-create/p/5511277.html
        $("#checkpassword").html('<span>The password should contain letters and numbers</span>');
		$("#checkpassword").addClass("failure");
		$("#checkpassword").removeClass("success");
	}else{
		$("#checkpassword").html('<span>The password is ok!</span>');
		$("#checkpassword").addClass("success");
		$("#checkpassword").removeClass("failure");
    }
    
}

function check_password2(){
    $("#passwords").find(".flash").hide();
    console.log("check_password2 called");
    var password2 = $(this);
    var password1 = $("#password");
    console.log("password repeat: " + password1.val() + " "+ password2.val());
    if(password1.val() == password2.val()){
        $("#checkpassword2").html('<span>Repeat Password is same</span>');
		$("#checkpassword2").addClass("success");
		$("#checkpassword2").removeClass("failure");
    }else{
        password2.val("");
		setTimeout(function(){password2.focus()},0); //https://www.cnblogs.com/djh-create/p/5511277.html
        $("#checkpassword2").html('<span>Repeat Password is not same</span>');
		$("#checkpassword2").addClass("failure");
    	$("#checkpassword2").removeClass("success");
    }
    
}

