$(document).ready(function(){
   // workaround for labels of inputs not animating properly
    $('input').focusin(function(){
        $(this).siblings('label').addClass('active');
    });
    $('input').focusout(function(){
        if ($(this).val()== "") {
            $(this).siblings('label').removeClass('active');
        }
    });
    $('input').filter(function(){
        return this.value.length > 0;
    }).siblings('label').addClass('active');

    $.fn.select2.defaults.set("theme", "bootstrap");
});
