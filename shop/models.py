from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse("Customer_detail", kwargs={"pk": self.pk})

class Product(models.Model):
    product_name = models.CharField(max_length=264,)
    price = models.FloatField()
    digital = models.BooleanField(default=False,null=True,blank=True)
    image = models.ImageField(upload_to='images',blank=True,null=True)
                                  
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
    def __str__(self):
        return self.product_name

    # def get_absolute_url(self):
    #     return reverse("Product_detail", kwargs={"pk": self.pk})

class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=264)

    def __str__(self):
        return str(self.id)
    
    @property
    def shipping(self):
        ship = False
        items = self.orderitem_set.all()
        for i in items:
            if i.product.digital == False:
                ship = True
        return ship

    @property
    def get_cart_total(self):
        items = self.orderitem_set.all()
        total = sum([item.get_total for item in items])
        return total
    
    @property
    def get_cart_items(self):
        items = self.orderitem_set.all()
        total = sum([item.quantity for item in items])
        return total

    # def get_absolute_url(self):
    #     return reverse("Order_detail", kwargs={"pk": self.pk})

class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.product_name
    
    @property
    def get_total(self):
        total = self.quantity*self.product.price
        return total

    # def get_absolute_url(self):
    #     return reverse("OrderItem_detail", kwargs={"pk": self.pk})


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    address = models.CharField(max_length=264)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

