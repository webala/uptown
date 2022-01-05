var cartTotal = document.getElementById('cart-total');

const getCartTotal = (cartTotal) => {
    let url = '/get_cart_total/';
    fetch(url)
    .then(response => response.json())
    .then(data => {
        
        cartTotal.innerHTML = data.cart_items.toString();
    });
}

getCartTotal(cartTotal);