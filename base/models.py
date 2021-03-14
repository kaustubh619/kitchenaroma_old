from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.conf import settings
from user.models import CustomUser

# Create your models here.
class Kitchen(models.Model):
    choices = (
        ('Open', 'Open'),
        ('Closed', 'Closed')
    )
    user = models.OneToOneField(CustomUser, on_delete=models.PROTECT, blank=True, null=True)
    kitchen_name = models.CharField(max_length=100)
    kitchen_logo = models.ImageField(upload_to='images/kitchenlogo')
    about = models.TextField(blank=True, null=True)
    contact = models.BigIntegerField(blank=True, null=True)
    mail = models.EmailField(blank=True, null=True)
    address_line_1 = models.CharField(max_length=500, blank=True, null=True)
    address_line_2 = models.CharField(max_length=500, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    fb_link = models.URLField(blank=True, null=True)
    insta_link = models.URLField(blank=True, null=True)
    kitchen_latitude = models.FloatField(blank=True, null=True)
    kitchen_longitude = models.FloatField(blank=True, null=True)
    gmap_address = models.TextField(blank=True, null=True)
    cover_radius_in_kms = models.IntegerField(blank=True, null=True)
    status = models.CharField(choices=choices, default="Closed", max_length=100)

    def __str__(self):
        return str(self.kitchen_name)

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    slug = slugify(instance.kitchen_name)
    instance.slug = slug

pre_save.connect(pre_save_post_receiver, sender=Kitchen)


class Category(models.Model):
    kitchen = models.ForeignKey(Kitchen, on_delete=models.PROTECT)
    category_title = models.CharField(max_length=100)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.kitchen) + " - " + str(self.category_title)


class MenuItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)        
    item_name = models.CharField(max_length=200)
    item_description = models.TextField(blank=True, null=True)
    item_price = models.IntegerField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.category) + " - " + str(self.item_name)


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    session_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return str(self.item) + " - " + str(self.quantity)


class KitchenRatingsAndReviews(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    kitchen = models.ForeignKey(Kitchen, on_delete=models.CASCADE)
    ratings = models.IntegerField(default=0)
    reviews = models.TextField(blank=True,null=True)

    def __str__(self):
        return str(self.user) + " - " + str(self.kitchen)


class KitchenGallery(models.Model):
    kitchen = models.ForeignKey(Kitchen, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/gallery')

    def __str__(self):
        return str(self.kitchen)


class Timing(models.Model):
    Weekdays = {
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'), 
        ('Sunday', 'Sunday'),
    }
    kitchen = models.ForeignKey(Kitchen, on_delete=models.CASCADE)
    weekday = models.CharField(blank=True, null=True, max_length= 100, choices=Weekdays)
    from_hour = models.TimeField()
    to_hour = models.TimeField()

    def __str__(self):
        return str(self.kitchen) + " - " + str(self.weekday)


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    kitchen = models.ForeignKey(Kitchen, on_delete=models.DO_NOTHING, blank=True, null=True)
    item = models.ForeignKey(MenuItem, on_delete=models.DO_NOTHING)
    item_price = models.FloatField()
    quantity = models.IntegerField()
    total = models.FloatField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user) + " - " + str(self.item)


class OrderTotal(models.Model):
    status = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Preparing', 'Preparing'),
        ('On The Way', 'On The Way'),
        ('Delivered', 'Delivered'),
        ('Canceled', 'Canceled'),
        ('Payment Incomplete', 'Payment Incomplete')
    )
    payment_request_id = models.CharField(max_length=200, blank=True, null=True)
    payment_id = models.CharField(max_length=200, blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    kitchen = models.ForeignKey(Kitchen, on_delete=models.DO_NOTHING)
    item_order = models.ManyToManyField(Order, blank=True, null=True)
    total = models.IntegerField()
    status = models.CharField(max_length=100, choices=status, default="Payment Incomplete")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)


class Contact(models.Model):
    full_name = models.CharField(max_length=100)        
    email = models.EmailField()
    subject = models.CharField(max_length=500)
    message = models.TextField()

    def __str__(self):
        return str(self.full_name) + ", " + str(self.email)

