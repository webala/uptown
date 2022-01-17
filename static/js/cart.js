let updateBtns = Array.from(document.getElementsByClassName('update-cart'));

updateBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
        var productId = btn.dataset.product;
        var action = btn.dataset.action;
        console.log(productId, action)

        console.log('USER: ', user)

        if (user == 'AnonymousUser') {
            addCokieItem(productId, action);
        } else {
            updateUserOrder(productId, action);
        }

    });
});

function addCokieItem (productId, action) {
    console.log('User not authenticated');
    if (action == 'add') {
        if (cart[productId] == undefined) {
            cart[productId] = {'quantity': 1}
        }
        else {
            cart[productId]['quantity'] += 1;
        }
    }
    else if (action == 'remove') {
        cart[productId]['quantity'] -= 1;

        if (cart[productId]['quantity'] <= 0) {
            console.log('Remove item');
            delete cart[productId];
        }
    }
    console.log(cart);
    document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/';
    location.reload();
}

function updateUserOrder (productId, action) {
   
    let url = '/update_item/';
    
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({'productId': productId, 'action': action})
    }).then(response => response.json())
    .then(data => {
        location.reload();
    })
    .catch(error => {
        console.log('Error', error)
    });
    
}