function addToCart(productId) {
    fetch(`/add_to_cart/${productId}`,
        { method: 'POST' }
    )
}

function changeOrderStatus(orderId, status) {
    fetch(`/change_order_status548548/${orderId}/${status}`,
        { method: 'POST' }
    )
}

function PlusCount(productId) { 
    fetch(`/change_count/${productId}/plus`,
        { method: 'POST' }
    )
    const quantityInput = document.querySelector(`.quantity-${productId}`);
    quantityInput.value = Number(quantityInput.value) + 1;
}

function MinusCount(productId) {
    fetch(`/change_count/${productId}/minus`,
        { method: 'POST' }
    )
    const quantityInput = document.querySelector(`.quantity-${productId}`);
    quantityInput.value = quantityInput.value - 1;

}