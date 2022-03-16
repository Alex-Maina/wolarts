from django.shortcuts import render, redirect
from .models import * 
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse 
import json 
from datetime import datetime
from django.contrib import messages
from .forms import OrderForm, CreateUserForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .utils import cookieCart



def register(request):
    form = CreateUserForm()
    cookieData = cookieCart(request)
    cartItems = cookieData['cartItems']
    order = cookieData['order']
    items = cookieData['items']
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            Customer.objects.create(
                user=user,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
            )
            Customer()
            
            
            user=form.cleaned_data.get('username')
            messages.success(request, 'Hey ' + user + '! Account created successfully.')
            return redirect('login')
    
    context = {'form': form, 'cartItems':cartItems}
    return render(request, 'store/register.html', context)


def loginPage(request):
    cookieData = cookieCart(request)
    cartItems = cookieData['cartItems']
    order_cookie = cookieData['order']
    items = cookieData['items']
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login (request, user)
            
            #gets data stored in cookie and updates the database
            customer = request.user.customer
            order, created = Order.objects.get_or_create(
                customer=customer,
                complete=False,
            )
            for item in items:
                product = Product.objects.get(id=item['product']['id'])
                orderItem, created = OrderItem.objects.get_or_create(order=order, product=product, quantity=item['quantity'])
                
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
            
            
            
            return redirect('store')
        else:
            messages.info(request,'Username or Password is incorrect')
            
    context = {'cartItems':cartItems}
    return render(request, 'store/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('store')
    

def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        #Create empty cart for now for non-logged in user
        items = []
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
    
    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems}
    return render(request, 'store/store.html', context)

def cart(request):
    #updates cart for authenticated user
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    
    #updates cart for unauthenticated user
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    
    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)
	
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        return redirect('login')
    
    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)

def updateItem (request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    
    print('Action:', action)
    print('ProductId:', productId)
    
    #Create or update order and order item
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()
    if orderItem.quantity <= 0:
        messages.info(request,f"{product.name} removed from cart")
        orderItem.delete()
    
    return JsonResponse('Item was added', safe=False)

def processOrder (request):
    transaction_id = datetime.now().timestamp()
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        total=float(data['form']['total'])
        order.transaction_id = transaction_id
        
        if total == order.get_cart_total:
            order.complete = True
            order.save()
            
            #Reduce inventory after successful purchase
            for item in items:
                item.product.inventory -= item.quantity
                item.save()
                item.product.save()
                order.complete = True
                order.save()
            
            
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            street=data['shipping']['street'],
            county=data['shipping']['county'],
            phone=data['shipping']['phone'],
        )
        
        
    else:
        print("Customer is not logged in")
    
    return JsonResponse ('Payment Complete!', safe=False)

def product (request, pk):
    product = Product.objects.get(id=pk)
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        #Create empty cart for now for non-logged in user
        items = []
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
    
    context = {'product':product,'cartItems':cartItems}
    return render(request, 'store/product.html', context)

def ourStory(request):
    return render(request, 'store/our_story.html')

def contactUs(request):
    return render(request, 'store/contact_us.html')

def articles(request):
    return render(request, 'store/articles.html')