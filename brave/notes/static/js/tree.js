$(document).ready(function () {
    $('label.tree-toggler').click(function () {
        $(this).parent().children('ul.tree').toggle(300);
        if($(this).children('span').hasClass('glyphicon-chevron-right')){
            $(this).children('span').removeClass( "glyphicon-chevron-right" ).addClass( "glyphicon-chevron-down" );
        }else{
            $(this).children('span').removeClass( "glyphicon-chevron-down" ).addClass( "glyphicon-chevron-right" );
        }
    });
});