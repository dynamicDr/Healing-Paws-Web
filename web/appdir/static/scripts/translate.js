
$(document).ready(function(){
	// add all event handlers here
    $("#loc-0").next().addClass("i18n").attr("name","beijing");
    $("#loc-1").next().addClass("i18n").attr("name","shanghai");
    $("#loc-2").next().addClass("i18n").attr("name","chengdu");

    $("#is_emergency-0").next().addClass("i18n").attr("name","emergency");
    $("#is_emergency-1").next().addClass("i18n").attr("name","standard");

    $("#new_question #type [value=1]").addClass("i18n").attr("name","about_pets");
    $("#new_question #type [value=2]").addClass("i18n").attr("name","about_doctors");
    $("#new_question #type [value=3]").addClass("i18n").attr("name","others");

    $("#category-0").next().addClass("i18n").attr("name","dog");
    $("#category-1").next().addClass("i18n").attr("name","cat");
});
