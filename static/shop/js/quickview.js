function getCsrfToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('[data-toggle="modal"]').forEach(function(button) {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            const productId = button.getAttribute('data-product-id');
            fetch(`/quick-view/${productId}/`)
                .then(response => response.json())
                .then(data => {
                    document.getElementById('quick-view-img').src = data.image_url;
                    document.getElementById('quick-view-name').textContent = data.name;
                    document.getElementById('quick-view-new-price').textContent = `$${data.new_price}`;
                    document.getElementById('quick-view-description').innerHTML = data.description;
                    document.getElementById('quick-view-read-more').href = data.full_description_url;

                    const quantityInput = document.querySelector('.cart-plus-minus-box');
                    const addToCartButton = document.getElementById('quick-view-add-to-cart');

                    addToCartButton.onclick = function(e) {
                        e.preventDefault();
                        const quantity = quantityInput.value;
                        const formData = new FormData();
                        formData.append('quantity', quantity);

                        fetch(`/cart/add/${productId}/`, {
                            method: 'POST',
                            body: formData,
                            headers: {
                                'X-CSRFToken': getCsrfToken()
                            }
                        }).then(response => {
                            if (response.ok) {
                                window.location.href = '/cart/';
                            }
                        });
                    };

                    document.getElementById('quick-view-add-to-wishlist').href = `/wishlist/add/${productId}/`;
                });
        });
    });
});
