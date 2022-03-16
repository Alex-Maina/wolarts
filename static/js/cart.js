var updateButtons = document.getElementsByClassName('update-cart')

//add an event handler looping through the clicks
for (var i = 0; i <updateButtons.length; i++) {
//create a query set 
updateButtons[i].addEventListener('click', function(){
    var productId = this.dataset.product
    var action = this.dataset.action
    console.log('Product ID:', productId, 'Action:', action)

    console.log('USER:', user)

    //Determines if the user is logged in or not
    if (user == 'AnonymousUser'){
        updateCookieItem(productId, action)
    }else{
        updateUserOrder(productId, action)
    }
})
}

//adds and item to cookie
function updateCookieItem(productId, action){
	console.log('User is not authenticated')

	if (action == 'add'){
		if (cart[productId] == undefined){
		cart[productId] = {'quantity':1}

		}else{
			cart[productId]['quantity'] += 1
		}
	}

	if (action == 'remove'){
		cart[productId]['quantity'] -= 1

		if (cart[productId]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete cart[productId];
		}
	}
	console.log('CART:', cart)
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
	location.reload()
}

//triggered when the user is logged in
function updateUserOrder(productId, action){
	console.log('User is authenticated, sending data...')

		var url = '/update_item/'

        //sends post request to the updateItem view (uses fetch API)
		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			}, 
			body:JSON.stringify({'productId':productId, 'action':action})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    console.log('Data:', data)
			location.reload()
		});
}