const buttons = document.getElementsByClassName("update-cart");

for (let i = 0; i < buttons.length; i++) {
    buttons[i].addEventListener("click", function() {
        const name = this.dataset.name;
        const data = { 'product_name': name };

        updateUserOrder(data);
    });
}

function updateUserOrder(data)
{
    const url = "update_item/";

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
    })
    .catch(error => console.error(error));
}

