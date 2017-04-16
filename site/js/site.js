$(document).ready(function() {
    $("[data-toggle]").each(function(i, e) {
        e = $(this);
        let selector = e.attr('data-toggle');
        var target = e;

        $(selector).click(function() {
            target.slideToggle();

            let chevron = $(this).find('.glyphicon');
            console.log(chevron);

            if(chevron.hasClass('glyphicon-chevron-down')) {
                chevron.removeClass('glyphicon-chevron-down');
                chevron.addClass('glyphicon-chevron-up');
            }
            else if(chevron.hasClass('glyphicon-chevron-up')) {
                chevron.removeClass('glyphicon-chevron-up');
                chevron.addClass('glyphicon-chevron-down');
            }
        });
    });
});
