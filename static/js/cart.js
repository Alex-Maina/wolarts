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
        console.log('User is not logged in')
    }else{
        updateUserOrder(productId, action)
    }
})
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