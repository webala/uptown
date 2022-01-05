let updateBtns = Array.from(document.getElementsByClassName('update-cart'));

updateBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
        var productId = btn.dataset.product;
        var action = btn.dataset.action;
        console.log(productId, action)

        console.log('USER: ', user)

        if (user == 'AnonymousUser') {
            console.log('User not authenticated')
        } else {
            updateUserOrder(productId, action);
        }

    });
});

function updateUserOrder (productId, action) {
    console.log('User authenticated, sending data.')

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