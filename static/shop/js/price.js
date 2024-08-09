$( function() {
    var min_price = parseFloat($('#min_price').val()) || 0;
    var max_price = parseFloat($('#max_price').val()) || 1000;

    $("#slider-range").slider({
        range: true,
        min: 0,
        max: 1000,
        values: [min_price, max_price],
        slide: function(event, ui) {
            $("#amount").val("$" + ui.values[0] + " - $" + ui.values[1]);
            $("#min_price").val(ui.values[0]);
            $("#max_price").val(ui.values[1]);
        }
    });
    $("#amount").val("$" + $("#slider-range").slider("values", 0) +
        " - $" + $("#slider-range").slider("values", 1));
});
