from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
import json
from django.contrib.auth.models import AnonymousUser

import datetime

# Create your views here.

def store(request):
	products = Product.objects.all()
	cartitems = cartItems(request)
	context = {'products':products,'cartitems':cartitems}
	return render(request, 'shop/store.html', context)

def cart(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		orders = Order.objects.filter(customer=customer, complete=False)

		if orders.exists():
			order = orders.first()
		else:
			order = Order.objects.create(customer=customer,complete=False)
			
		items = order.orderitem_set.all()
		cartitems = cartItems(request)

	else:
		items = []
		order = {'get_cart_total':0,'get_cart_items':0}

		try:
			cart = json.loads(request.COOKIES['cart'])
		except:
			cart = {}

		cartitems = 0
		for item in cart:
			product = Product.objects.get(id=item)

			total = (product.price*cart[item]['qty'])
			cartitems += cart[item]['qty']

			order['get_cart_total'] += total
			order['get_cart_items'] += cartitems

			item = {'product':{
				'id':product.id, 
				'product_name': product.product_name,
				'price': product.price,
				'imageURL':product.imageURL
				},
				'quantity': cart[item]['qty'],
				'get_total': total
				}
			items.append(item)

	context = {'items':items,'order':order,'cartitems':cartitems}
	return render(request, 'shop/cart.html', context)



def checkout(request):

	if request.user.is_authenticated:
		customer = request.user.customer
		orders = Order.objects.filter(customer=customer, complete=False)
		
		if orders.exists():
			order = orders.first()
		else:
			order = Order.objects.create(customer=customer,complete=False)
		
		items = order.orderitem_set.all()

		if request.method == "POST":
			customer = request.user.customer
			print(customer)
			address = request.POST['address']
			city = request.POST['city']
			state = request.POST['state']
			zipcode = request.POST['zipcode']

			shippingaddress = ShippingAddress.objects.create(customer=customer,order=order,address=address,city=city,state=state,zipcode=zipcode)
			shippingaddress.save()

			order.complete = True
			order.save()
			return redirect('store')
		cartitems = cartItems(request)
	else:
		items = []
		order = {'get_cart_total':0,'get_cart_items':0,"shipping":False}

		try:
			cart = json.loads(request.COOKIES['cart'])
		except:
			cart = {}

		cartitems = 0
		for item in cart:
			product = Product.objects.get(id=item)

			total = (product.price*cart[item]['qty'])
			cartitems += cart[item]['qty']

			order['get_cart_total'] += total
			order['get_cart_items'] += cartitems

			item = {'product':{
				'id':product.id, 
				'product_name': product.product_name,
				'price': product.price,
				'imageURL':product.imageURL
				},
				'quantity': cart[item]['qty'],
				'get_total': total
				}
			items.append(item)

	context = {'items':items,'order':order,'cartitems':cartitems}


	return render(request, 'shop/checkout.html', context)


# Fetching JSON
def updateItem(request):

	if request.user.is_authenticated:
		try:
			data = json.loads(request.body)
			productId = data['productId']
			action = data['action']

			customer = request.user.customer
			product = Product.objects.get(id=productId)

			orders = Order.objects.filter(customer=customer, complete=False)

			if orders.exists():
				order = orders.first()
			else:
				order = Order.objects.create(customer=customer, complete=False)

			item = OrderItem.objects.filter(order=order, product=product)

			if item.exists():
				item = item.first()
			else:
				item = OrderItem.objects.create(order=order, product=product,quantity=0)

			if action == 'add':
				item.quantity += 1
			elif action == 'remove':
				item.quantity = max(item.quantity - 1, 0)

			item.save()

			itemsTotal = item.quantity
			cartItems = order.get_cart_items
			cartTotal = order.get_cart_total

			if item.quantity <= 0:
				item.delete()

			dictionary = {'cartItems':cartItems,'itemsTotal':itemsTotal,'id':productId,'cartTotal':cartTotal}

			return JsonResponse(dictionary)

		except Exception as e:
			print(e)
		
	return JsonResponse('Item was added', safe=False)



# Fuzoool
def main(request):
	cartitems = cartItems(request)
	return render(request, 'shop/main.html',{'cartitems':cartitems})

# Gettting cart Items
def cartItems(request):
	
	if request.user.is_authenticated:
		customer = request.user.customer
		orders = Order.objects.filter(customer=customer,complete=False)
		
		if orders.exists():
			order = orders.first()
			cartitems = order.get_cart_items
		else:
			cartitems = 0

	else:
		try:
			cart = json.loads(request.COOKIES['cart'])
		except Exception as e:
			cart = {}
		cartitems = 0
		for item in cart:
			cartitems += cart[item]['qty']
	return cartitems


def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	print(transaction_id)

	if request.method == 'POST':
		try:
			data = json.loads(request.body)
			print(data)

			if request.user.is_authenticated:
				print("Authenticated")
				customer = request.user.customer

				orders = Order.objects.filter(customer=customer,complete=False)
				order = orders.first()

				total = float(data['form']['total'])
				order.transaction_id = str(transaction_id)

				if float(order.get_cart_total) == total:
					order.complete = True
				order.save()
				print('Shipping:',order.shipping)

				if order.shipping != False:
					print('shipping is True')

					address = data['shipping']['address']
					city = data['shipping']['city']
					state = data['shipping']['state']
					zipcode = data['shipping']['zipcode']
					
					print('shipping is True')
					print(address,city,state,zipcode)

					shippingAddress = ShippingAddress.objects.create(customer=customer,order=order,
															address=address,city=city,state=state,zipcode=zipcode)
					shippingAddress.save()
			else:
				print("USER NOT LOGGEN IN")

		except Exception as e:
			print(e)

	return JsonResponse("Order Processed!", safe=False)

