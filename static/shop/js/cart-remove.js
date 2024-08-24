function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(document).ready(function() {
    $('.remove-from-cart').click(function(e) {
        e.preventDefault();
        var productId = $(this).data('product-id');
        var url = $(this).data('url');
        var $cartItem = $('#cart-item-' + productId);

        $.ajax({
            url: url,
            method: 'POST',
            data: {
                product_id: productId
            },
            success: function(response) {
                if (response.success) {
                    $cartItem.remove();
                    $('.shop-total').text('$' + response.total_price);
                    $('.count-style').text(response.cart_count);

                    if (response.cart_count === 0) {
                        $('.shopping-cart-total').hide();
                        $('.shopping-cart-btn').hide();
                        $('.cart-empty-title').show();
                    }
                }
            }
        });
    });
});
