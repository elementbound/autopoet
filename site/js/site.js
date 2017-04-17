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

    // When clicking on a poet, ask the server to cache it
    // Also store it in a global-ish variable
    var current_poet = undefined;

    $("a[data-poet]").click(function() {
        let url = '/load/' + $(this).attr('data-poet');
        var e = $(this);
        var update = $(this).attr('data-update');

        $(update).html('<span class="glyphicon glyphicon-hourglass"></span>');

        $.getJSON(url, function(data) {
            if(!data.error) {
                $(update).html(e.text());
                current_poet = e.attr('data-poet');
            }
            else
                $(update).html(data.error);
        });
    });

    // Send AJAX requests to the server for autocomplete
    var autocomplete_needs_update = false;
    var autocomplete_rest = 250;
    var last_word = '';
    var requests = 0;

    function update_autocomplete(word) {
        let url = '/autocomplete/' + current_poet + '/' + word;
        console.log(url);

        requests += 1;
        $('.requests-counter').html(requests);

        $.getJSON(url, function(data) {
            let table = $('table.autocomplete-suggestions');
            table.empty();

            requests -= 1;
            $('.requests-counter').html(requests);

            if(data.error)
                $('<td>')
                    .html('Error: ' + data.error)
                    .appendTo(
                        $('<tr>').appendTo(table));
            else {
                for(let i = 0; i < data.length; i++) {
                    let suggestion = data[i].word;
                    let weight = data[i].weight;

                    let cells = [
                        $('<td>').html(suggestion),
                        $('<td>').html(Math.round(weight*100) + '%')
                    ]

                    let row = $('<tr>');
                        row.append(cells[0]);
                        row.append(cells[1]);

                    row.appendTo(table);
                }
            }
        });
    }

    function schedule_update() {
        if(autocomplete_needs_update != false) {
            if(autocomplete_needs_update != last_word)
                update_autocomplete(autocomplete_needs_update);

            autocomplete_needs_update = false;
        }

        setTimeout(schedule_update, autocomplete_rest);
    }

    schedule_update();

    var f = function(event) {
        let text = $(this).val();
        if(text == '') {
            autocomplete_needs_update = false;
            return;
        }

        text = text.split(/\s+/);
        text = text[text.length-1];
        console.log(text);

        autocomplete_needs_update = text;
    };

    $('.autocomplete-input').keyup(f);
    $('.autocomplete-input').blur(f);

    // Debug current poet at all times
    var f = function() {
        $('.poet-variable').text(current_poet);
        setTimeout(f, 100);
    };

    f();
});
