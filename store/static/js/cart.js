// -------------------------------
// Utility: Get CSRF token
// -------------------------------
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// -------------------------------
// Helper: Show bootstrap alert
// -------------------------------
function showAlert(message, type = 'success') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed top-0 end-0 m-3`;
    alertDiv.style.zIndex = 9999;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.appendChild(alertDiv);
    setTimeout(() => alertDiv.remove(), 2000);
}

// -------------------------------
// Recalculate total cart price
// -------------------------------
function updateCartTotal() {
    let total = 0;
    document.querySelectorAll('[id^="total-"]').forEach(el => {
        total += parseFloat(el.textContent) || 0;
    });
    const cartTotalElem = document.getElementById('cart-total');
    if (cartTotalElem) cartTotalElem.textContent = total.toFixed(2);
}

// -------------------------------
// Event delegation for cart actions
// -------------------------------
document.body.addEventListener('click', function (e) {
    const target = e.target;
    const isRemove = target.classList.contains('remove-from-cart');
    const isIncrease = target.classList.contains('increase-btn');
    const isDecrease = target.classList.contains('decrease-btn');

    if (isRemove || isIncrease || isDecrease) {
        e.preventDefault();
        const productId = target.dataset.product;
        let url = '';

        if (isRemove) url = `/cart/remove/${productId}/`;
        if (isIncrease) url = `/cart/increase/${productId}/`;
        if (isDecrease) url = `/cart/decrease/${productId}/`;

        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(res => res.json())
        .then(data => {
            if (!data.success) return;

            // Update navbar count
            const cartCount = document.getElementById('cart-count');
            if (cartCount) cartCount.textContent = data.qty;

            // Handle remove
            if (isRemove) {
                const item = document.getElementById(`cart-item-${productId}`);
                if (item) item.remove();
                showAlert('Removed from cart!');
                updateCartTotal();
                return;
            }

            // Handle increase/decrease
            const priceElem = document.getElementById(`price-${productId}`);
            const qtyElem = document.getElementById(`qty-${productId}`);
            const totalElem = document.getElementById(`total-${productId}`);

            const price = parseFloat(priceElem.textContent);
            let qty = parseInt(qtyElem.textContent);

            if (isIncrease) qty++;
            if (isDecrease) qty--;

            if (qty <= 0) {
                document.getElementById(`cart-item-${productId}`).remove();
                showAlert('Item removed from cart');
            } else {
                qtyElem.textContent = qty;
                totalElem.textContent = (price * qty).toFixed(2);
            }

            updateCartTotal();
        })
        .catch(err => console.error(err));
    }
});



// // Utility function to get CSRF token
// function getCookie(name) {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         const cookies = document.cookie.split(';');
//         for (let cookie of cookies) {
//             cookie = cookie.trim();
//             if (cookie.startsWith(name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }

// document.addEventListener('DOMContentLoaded', function() {

//     // Add to Cart
//     document.querySelectorAll('.add-to-cart-btn').forEach(button => {
//         button.addEventListener('click', function(e) {
//             e.preventDefault();
//             const productId = this.dataset.product;

//             fetch(`/cart/add/${productId}/`, {
//                 method: 'POST',
//                 headers: {
//                     'X-CSRFToken': getCookie('csrftoken'),
//                     'X-Requested-With': 'XMLHttpRequest'
//                 }
//             })
//             .then(res => res.json())
//             .then(data => {
//                 const cartCount = document.getElementById('cart-count');
//                 if (cartCount) cartCount.textContent = data.cartItemCount;
//                 showAlert('Added to cart!');
//             })
//             .catch(err => console.error(err));
//         });
//     });

//     // Remove from Cart
//     document.querySelectorAll('.remove-from-cart').forEach(button => {
//         button.addEventListener('click', function(e) {
//             e.preventDefault();
//             const productId = this.dataset.product;

//             fetch(`/cart/remove/${productId}/`, {
//                 method: 'POST',
//                 headers: {
//                     'X-CSRFToken': getCookie('csrftoken'),
//                     'X-Requested-With': 'XMLHttpRequest'
//                 }
//             })
//             .then(res => res.json())
//             .then(data => {
//                 if (data.success) {
//                     const cartCount = document.getElementById('cart-count');
//                     if (cartCount) cartCount.textContent = data.qty;

//                     const itemCard = document.getElementById(`cart-item-${productId}`);
//                     if (itemCard) itemCard.remove();

//                     showAlert('Removed from cart!');
//                 }
//             })
//             .catch(err => console.error(err));
//         });
//     });

//     function showAlert(message) {
//         const alertDiv = document.createElement('div');
//         alertDiv.className = 'alert alert-success alert-dismissible fade show position-fixed top-0 end-0 m-3';
//         alertDiv.style.zIndex = 9999;
//         alertDiv.innerHTML = `${message} <button type="button" class="btn-close" data-bs-dismiss="alert"></button>`;
//         document.body.appendChild(alertDiv);
//         setTimeout(() => {
//             alertDiv.classList.remove('show');
//             alertDiv.remove();
//         }, 2500);
//     }
// });
