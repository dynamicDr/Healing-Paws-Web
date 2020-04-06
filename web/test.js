var url="http://172.17.11.201:3000/mock/643/devices/getDevicesInfoList.do";

var date = [];

/*-------------choose-------------------*/

$(document).ready(function() {
    $.ajax({
        url : url,
        type : 'GET',
        async : false,
        data : {},

        success : function(message) {
            if (message.resCode == '10000') {
                devices = message.detail;
                if (devices.devicesBrandList.length < 10) {
                    $(".more").hide();
                }
                if (devices.resolutionList.length < 10) {
                    $(".more2").hide();
                }
                if (devices.androidVersionList.length < 10) {
                    $(".more1").hide();
                }

                if (devices.iosVersionList.length < 10) {
                    $(".more3").hide();
                }

                for (var i = 0; i < devices.devicesBrandList.length; i++) {
                    if ("" != devices.devicesBrandList[i] && i < 10) {
                        $("#devicebrand").append("<span class='before_color brand'>"+ devices.devicesBrandList[i]+ "</span>");
                    } else if ("" != devices.devicesBrandList[i] && i >= 10) {
                        if(i % 10 ==0 && i>10){
                            $(".more_brand").append("<p class='type_name1'></p>");
                        }
                        $(".more_brand").append("<span class='before_color brand'>"+ devices.devicesBrandList[i]+ "</span>");
                    }
                }

                for (var i = 0; i < devices.androidVersionList.length; i++) {
                    if ("" != devices.androidVersionList[i] && i < 10) {
                        $("#androidVersion").append("<span class='before_color edition_android'>"+ devices.androidVersionList[i]+ "</span>");
                    } else if ("" != devices.androidVersionList[i] && i >= 10) {
                        if(i % 10 ==0 && i>10){
                            $(".more_androidVersion").append("<p class='type_name1'></p>");
                        }
                        $(".more_androidVersion").append("<span class='before_color edition_android'>"+ devices.androidVersionList[i]+ "</span>");
                    }
                }

                for (var i = 0; i < devices.iosVersionList.length; i++) {
                    if ("" != devices.iosVersionList[i] && i < 10) {
                        $("#iosVersion").append("<span class='before_color edition_ios'>"+ devices.iosVersionList[i]+ "</span>");
                    } else if ("" != devices.iosVersionList[i] && i >= 10) {
                        if(i % 10 ==0 && i>10){
                            $(".more_iosVersion").append("<p class='type_name1'></p>");
                        }
                        $(".more_iosVersion").append("<span class='before_color edition_ios'>"+ devices.iosVersionList[i]+ "</span>");
                    }
                }

                for (var i = 0; i < devices.resolutionList.length; i++) {
                    if ("" != devices.resolutionList[i] && i < 10) {
                        $("#resolution").append("<span class='before_color resolution'>"+ devices.resolutionList[i]+ "</span>");
                    } else if ("" != devices.resolutionList[i] && i >= 10) {
                        if(i % 10 ==0 && i>10){
                            $(".more_resolution").append("<p class='type_name1'></p>");
                        }
                        $(".more_resolution").append("<span class='before_color resolution'>"+ devices.resolutionList[i]+ "</span>");
                    }
                }
            } else {
                console.log("获取出错");
            }
        },
        error : function(message) {
        }
    });

        date.deviceBrand = "",
        date.searchStr = "",
        date.sysVersion = "",
        date.resolution = "";

    search();

});

/* 设置choose类下li标签选中背景色变色 */

$(this).removeClass('font_color');
$(this).removeClass('before_color');
$(this).removeClass('default_color');
$(document).ready(function() {
    $('#brand_addr').click(function() {
        $('.brand').removeClass('add_color');
    });
    $('#resolution_addr').click(function() {
        $('.resolution').removeClass('add_color');
    });
    $('#edition_android ').click(function() {
        $('.edition_android').removeClass('add_color');
    });
    $('#edition_ios ').click(function() {
        $('.edition_ios').removeClass('add_color');
    });
    $('.type_name span').click(function() {
        if ($(this).hasClass('add_color')) {
            $(this).removeClass("add_color");
            $('#brand_addr').removeClass('add_color');
            $('.brand').removeClass('default_color');
            $('.type_name span').removeClass('default_color');
        } else {
            $('#brand_addr').removeClass('add_color');
            $('.brand').removeClass('default_color');
            $('.type_name span').removeClass('default_color');
            $(this).addClass("add_color");
        }
        search();
    });

    $('.type_name1 span').click(function() {
        if ($(this).hasClass('add_color')) {
            $(this).removeClass("add_color");
            $('#edition_android').removeClass('add_color');
            $('.edition_android').removeClass('default_color');
            $('.type_name1 span').removeClass('default_color');
        } else {
            $('#edition_android').removeClass('add_color');
            $('.edition_android').removeClass('default_color');
            $('.type_name1 span').removeClass('default_color');
            $(this).addClass('add_color');
        }
        search();
    });

    $('.type_name2 span').click(function() {
        if ($(this).hasClass('add_color')) {
            $(this).removeClass("add_color");
            $('#resolution_addr').removeClass('add_color');
            $('.resolution').removeClass('default_color');
            $('.type_name2 span').removeClass('default_color');
        } else {
            $('#resolution_addr').removeClass('add_color');
            $('.resolution').removeClass('default_color');
            $('.type_name2 span').removeClass('default_color');
            $(this).addClass('add_color');
        }
        search();
    });

    $('.type_name3 span').click(function() {

        if ($(this).hasClass('add_color')) {

            $(this).removeClass("add_color");

            $('#edition_ios').removeClass('add_color');

            $('.edition_ios').removeClass('default_color');

            $('.type_name3 span').removeClass('default_color');

        } else {

            $('#edition_ios').removeClass('add_color');

            $('.edition_ios').removeClass('default_color');

            $('.type_name3 span').removeClass('default_color');

            $(this).addClass('add_color');

        }

        search();

    });

})

/* 设置列表加载更多 */

$(document).ready(function() {
    $('.more').click(function() {
        $('#more_brand').css("display","block");
        $('.more').css("display","none");
        $(".back").css("display","block");
    });
    $('.back').click(function() {
        $('#more_brand').css("display","none");
        $('.more').css("display","block");
        $(".back").css("display","none");
    });

    $('.more1').click(function() {
        $('#more_androidVersion').css("display","block");
        $('.more1').css("display","none");
        $('.back1').css("display","block");
    });

    $('.back1').click(function() {

        $('#more_androidVersion').css("display","none");

        $('.more1').css("display","block");

        $(".back1").css("display","none");

    });

    $('.more3').click(function() {

        $('#more_iosVersion').css("display","block");

        $('.more3').css("display","none");

        $(".back3").css("display","block");

    });

    $('.back3').click(function() {

        $('#more_iosVersion').css("display","none");

        $('.more3').css("display","block");

        $(".back3").css("display","none");

    });

    $('.more2').click(function() {

        $('#more_resolution').css("display","block");

        $('.more2').css("display","none");

        $(".back2").css("display","block");

    });

    $('.back2').click(function() {

        $('#more_resolution').css("display","none");

        $('.more2').css("display","block");

        $(".back2").css("display","none");

    });

});

//筛选获取已选标签

function search(){

        date.deviceBrand = "",
        date.AndroidVersion = "",
        date.IosVersion = "",
        date.resolution = "";

    if($('#brand_addr').hasClass('add_color') || $('#brand_addr').hasClass('default_color')){
        $('.brand').each(function() {
            date.deviceBrand += $(this).text() + "|";
        });
    }

    if($('#edition_android').hasClass('add_color') || $('#edition_android').hasClass('default_color')){
        $('.edition_android').each(function() {
            date.AndroidVersion += "android" + $(this).text() + "|";
        });
    }

    if($('#edition_ios').hasClass('add_color') || $('#edition_ios').hasClass('default_color')){
        $('.edition_ios').each(function() {
            date.IosVersion +=  "ios" + $(this).text() + "|";
        });
    }

    if($('#resolution_addr').hasClass('add_color') || $('#resolution_addr').hasClass('default_color')){
        $('.resolution').each(function() {
            date.resolution += $(this).text() + "|";
        });
    }

    $('.brand').each(function() {
        if ($(this).hasClass('add_color')){
            date.deviceBrand += $(this).text() + "|";
        }
    });

    $('.edition_android').each(function() {
        if ($(this).hasClass('add_color')){
            date.AndroidVersion += "android" + $(this).text() + "|";
        }
    });

    $('.resolution').each(function() {
        if ($(this).hasClass('add_color')){
            date.resolution += $(this).text() + "|";
        }
    });

    $('.edition_ios').each(function() {
        if ($(this).hasClass('add_color')){
            date.IosVersion += "ios" +$(this).text() + "|";
        }
    });

    //console.log(date);

    document.getElementById("choosedBrand").innerHTML="";
    document.getElementById("choosedAndroidVersion").innerHTML="";
    document.getElementById("choosedIosVersion").innerHTML="";
    document.getElementById("choosedResolution").innerHTML="";
    $('#choosedBrand').append(date.deviceBrand);
    $('#choosedAndroidVersion').append(date.AndroidVersion);
    $('#choosedIosVersion').append(date.IosVersion);
    $('#choosedResolution').append(date.resolution);
};