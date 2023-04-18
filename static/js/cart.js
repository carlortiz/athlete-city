const buttons = document.getElementsByClassName("update-cart");

for (let i = 0; i < buttons.length; i++) {
    buttons[i].addEventListener("click", function() {
        const name = this.dataset.name;
        const action = this.dataset.action;

        const data = { 
            'product_name': name,
            'action': action
        };

        console.log(action);
        updateUserOrder(data);
    });
}

function updateUserOrder(data)
{
    const url = "/update_item/";

    // This is the fetch API
    // It sends a POST request to the 'update_item' with a product name
    // It receives a response and updates the cart total value in nav bar
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(data),
    })
    .then(response => {
        return response.json();
    })
    .then(data => {
        const cartTotalElement = document.getElementById("cart-total");
        if (cartTotalElement) {
            cartTotalElement.innerText = data['cart_items'];
        }

        // This grabs the first element in the document with that ID
        // We need it to grab the element that corresponds to the product
        const itemTotalElement = document.getElementById("item-total");
        if (itemTotalElement) {
            itemTotalElement.innerText = 'x' + data['item_quantity'];
        } 
    })
    .catch(error => console.error(error));
}

