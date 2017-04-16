$(document).ready(function() {
    // For each element, if its data-toggle is clicked, it will slideToggle
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

    // When clicked, the item will replace all <data-update> elements with its text
    $("[data-update]").each(function(i, e) {
        e = $(this);
        let selector = e.attr('data-update');
        var target = $(selector);

        $(e).click(function() {
            target.html(e.text());
        });
    });
});
