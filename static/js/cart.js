$('.update-cart').on('click', function () {
    var productId = $(this).data('product')
    var action = $(this).data('action')
    var price = $(this).data('price')
    console.log("productId", productId, "action", action)

    if (user === 'AnonymousUser') {
        addCookies(productId, action, price)
    } else {
        userOrderUpdate(productId, action)
    }

})

function addCookies(productId, action,price) {

    if (action == 'add') {

        price = parseFloat(price)
        
        if (cart[productId] == undefined) {
            console.log("ADD IF")

            cart[productId] = { 'qty': 1, 'price':price}


        } else {
            console.log("ADD ELSE")
            cart[productId]['qty'] += 1


            if ($('#' + productId).val() == undefined) {
                console.log("HOME PAGE")
            } else {
                $("#" + productId).html(cart[productId]['qty'])
                
                var totalitems = 0
                var totalprice = 0
                for (var item in cart){
                    totalitems += cart[item]['qty']
                    totalprice = (totalprice + (cart[item]['price']*cart[item]['qty']))
                }
                totalprice = totalprice.toString()
                $("#totalitems").html(totalitems)
                $("#totalprice").html("$"+totalprice)
            }
        }

    }
    else if (action == 'remove') {
        if (cart[productId]['qty'] > 0) {
            console.log("Remove IF = -1")
            cart[productId]['qty'] -= 1
            $("#" + productId).html(cart[productId]['qty'])

            var totalitems = 0
                var totalprice = 0
                for (var item in cart){
                    totalitems += cart[item]['qty']
                    totalprice = (totalprice + (cart[item]['price']*cart[item]['qty']))
                }
                totalprice = totalprice.toString()
                $("#totalitems").html(totalitems)
                $("#totalprice").html("$"+totalprice)

            if(cart[productId]['qty'] == 0){
                console.log("DELETE")
            $('#div' + productId).html("")
            delete cart[productId]
            }
        }

    }
    console.log(cart)
    document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/"

    carttotal = 0

    for (item in cart) {
        carttotal += cart[item]['qty']
    }
    $('#cart-total').html(carttotal)

}


function userOrderUpdate(productId, action) {
    var url = '/update_item/'

    var cartData = {
        'productId': productId,
        'action': action
    }

    $.ajax({
        type: 'POST',
        url: url,
        data: JSON.stringify(cartData),
        'Content-Type': 'application/json',
        headers: {
            'X-CSRFToken': csrftoken,
        },

    }).done(function (data) {
        console.log(data)
        $('#cart-total').html(data['cartItems'])

        if ($('#' + productId).val() == undefined) {
            console.log("Home Page")
        } else {
            $("#" + productId).html(data['itemsTotal'])
                if (data['itemsTotal'] > 0) {

                    $("#"+productId).html(data['itemsTotal'])
                    $("#totalitems").html(data['cartItems'])
                    $("#totalprice").html("$"+data['cartTotal'])
                }
                else{
                
                    console.log("ID IS 0")
                    $("#div"+productId).remove()
                    $("#totalitems").html(data['cartItems'])
                    $("#totalprice").html("$"+data['cartTotal'])
                    
                }
                
            }
        }).fail(function (error) {
        console.error("Error:", error);
    });
}