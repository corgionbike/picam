$(document).ready(function () {

    $SCRIPT_ROOT = {{ request.script_root|tojson|safe }};
    var $btns = $('[id ^= btn_shoot]');  
    var $modal = $('#main_modal');
    $btns.each(function (indx, element) {
        $(element).click(
            function (e) {
                $modal.modal({
                    backdrop: false
                });
                $btns.addClass('disabled');
            }
        )
    });
    var $cpu = $("#cpu");
    var $rem = $("#rem");
    var $cpu_temp = $("#cpu_temp");
    
    setInterval(function()
        {
            $.getJSON($SCRIPT_ROOT + 'sys_info', {
            }, function (data) {
                if (data) {
                    //console.log(data);
                    $cpu.text(data.cpu + '%'); 
                    $rem.text(data.ram + '%');
                    $cpu_temp.text(data.cpu_temp);
                }
            });


        }
    , 5000);

    $('a#set_servo').click(function () {
        $.getJSON($SCRIPT_ROOT + 'set_servo', {
            x: $('input[name="x"]').val(),
            y: $('input[name="y"]').val()
        }, function (data) {
            if (data) {
                $(".fas.fa-compass").fadeOut().fadeIn();
            }
            console.log(data);
        });
        return false;
    });
    
    $('a#btn_reload').click(function () {
        $.getJSON($SCRIPT_ROOT + 'reload', {
        }, function (data) {
            if (data) {
                $(".fas.fa-sync").addClass('fa-spin');
                var $links = $("div.carousel-inner").find("a");
                $links.each(function(indx, element){
                    $(element).attr('href', data.photo_list[indx]); 
                    $(element).children('img').attr('src', data.photo_list_thumbnail[indx]);
                });
                setTimeout(() => { $(".fas.fa-sync").removeClass('fa-spin'); }, 1000);
                
            };
            //console.log($links);
            //#console.log(data);
        });
        return false;
    });


    $('a#btn_arch').click(function () {
        $.getJSON($SCRIPT_ROOT + 'copy_to_archive', {
            s: $('input[name="s"]').val(),
        }, function (data) {
            if (data) {
                //console.log(data);
                $(".fas.fa-archive").fadeOut().fadeIn();
            }
            console.log(data);
        });
        return false;
    });

    $('a[id ^= "btn_del_photo_"]').click(function (e) {
        $btn = $(this);
        var link = $btn.data('href');
        $.getJSON(link, {}, function (data) {
            if (data) {
                $btn.parents('card').fadeOut('slow', function()
                {
                    $(this).remove();
                    if ($('a[id ^= "btn_del_photo_"]').length == 0)
                        $('#msg_empty_arch').show();
                });
                //console.log(data);
            }
            //console.log(data);
        });
        return false;
    });

    $('a#set_calibration').click(function () {
        $.getJSON($SCRIPT_ROOT + 'set_calibration', {
            x: $('input[name="x"]').val(),
            y: $('input[name="y"]').val()
        }, function (data) {
            if (data) {
                $('input[name="x"]').val(0);
                $('input[name="y"]').val(0);
                $(".fas.fa-arrows-alt").fadeOut().fadeIn();
            }
            console.log(data);
        });
        return false;
    });

});

