from django.shortcuts import render, redirect
from .models import Kitchen, Category, Cart, MenuItem, KitchenRatingsAndReviews, KitchenGallery, Timing, Order, OrderTotal
from user.models import CustomUser
from .serializers import CartSerializer, KitchenSerializer, CartSerializerWithDepth, KitchenNameSerializer, TimingSerializer, CreateOrderSerializer
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK
)
from django.http import Http404
from django.contrib.auth.models import User
from .models import Cart, Kitchen, Timing, Contact
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework import generics, permissions, status
from math import sin, cos, sqrt, atan2, radians
import datetime 
import calendar
from instamojo_wrapper import Instamojo

api = Instamojo(api_key="", auth_token="")

# Create your views here.
def home(request):
    today = datetime.datetime.now().weekday()
    day = calendar.day_name[today]
    kitchens = Kitchen.objects.all()
    context = {'kitchens': kitchens}
    return render(request, 'home.html', context)


def kitchen(request, kitchen):
    try:
        time = datetime.datetime.now().time()
        today = datetime.datetime.now().weekday()
        weekday = calendar.day_name[today]
        kitchen_obj =  Kitchen.objects.get(slug=kitchen)
        if kitchen_obj.status == "Open":
            timings = Timing.objects.filter(Q(kitchen=kitchen_obj) & Q(weekday=weekday))
            category_obj = Category.objects.filter(kitchen=kitchen_obj)
            context = {'kitchen': kitchen_obj, 'categories': category_obj}
            if timings.count() > 0:
                for timing in timings:
                    if timing.from_hour < time < timing.to_hour:
                        # return render(request, 'kitchen.html', context)
                        break
                    else:
                        return redirect("/")
            else:
                return redirect("/")
        else:
            return redirect("/")
    except:
        return redirect("/")
    return render(request, 'kitchen.html', context)


class AddItemToCart(viewsets.ViewSet):
    def cart_items(self, request):
        queryset = Cart.objects.filter(user=request.user)
        serializer = CartSerializerWithDepth(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.is_authenticated:
            serializer = CartSerializer(data={"user": request.user.id, "item": request.data["item"], "quantity": request.data["quantity"]})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        else:
            serializer = CartSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request):
        if request.user.is_authenticated:
            user_cart_items = Cart.objects.filter(user=request.user)
            user_cart_items.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors)


class EditCart(APIView):
    def get_object(self, pk):
        try:
            return Cart.objects.get(item=pk)
        except Cart.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        cart_item = self.get_object(pk)
        CartItem = CartSerializer(cart_item, context={"request": request})
        return Response(CartItem.data)

    def put(self, request, pk):
        cart_obj = Cart.objects.get(Q(user=request.user) & Q(item=MenuItem.objects.get(id=pk)))
        serializer = CartSerializer(cart_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        cart_obj = Cart.objects.get(Q(user=request.user) & Q(item=MenuItem.objects.get(id=pk)))
        cart_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartByUser(APIView):
    def get(self, request):
        obj = Cart.objects.filter(user=request.user)
        serializer = CartSerializerWithDepth(obj, many=True)
        return Response(serializer.data)


@login_required(login_url="/")
def cart(request):
    item_word = "item"
    cart_bool = False
    cart_items = Cart.objects.filter(user=request.user)
    if cart_items.count() > 0:
        cart_bool = True
    if cart_items.count() > 1:
        item_word = "items"
    total_cost = 0        
    for item in cart_items:
        total_cost += item.item.item_price * item.quantity
    message = ""
    kitchen_filter = []
    kitchens = []
    if request.method == "POST":
        user = request.user
        if len(request.POST['phone']) != 10:
            message = "Invalid Contact Number"
        else:
            user.phone_number = request.POST['phone']
            user.save()
            message = "Contact number updated successfully"
    context = {
        'items': cart_items,
        "item_word": item_word,
        "total_cost": total_cost,
        "cost_with_delivery": total_cost + 40,
        "cart_bool": cart_bool,
        "message": message
    }

    for item in cart_items:
        lat = radians(item.item.category.kitchen.kitchen_latitude)
        lon = radians(item.item.category.kitchen.kitchen_longitude)
        user_lat = radians(request.user.user_location_latitude)
        user_lon = radians(request.user.user_location_longitude)
        R = 6378.137
        dlon = user_lon - lon
        dlat = user_lat - lat
        a = (sin(dlat/2))**2 + cos(lat) * cos(user_lat) * (sin(dlon/2))**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        distance = R * c
        if item.item.category.kitchen.cover_radius_in_kms > distance:
            kitchens.append(item.item.category.kitchen.kitchen_name)
        else:
            kitchen_filter.append(item.item.category.kitchen.kitchen_name)
    try:
        kitchen = Kitchen.objects.get(kitchen_name=kitchens[0])
        context['kitchen_filter'] = kitchen_filter
        context['kitchen_status'] = kitchen.status
        context['kitchen_name'] = kitchen.kitchen_name
        context['kitchen_id'] = kitchen.id
    except:
        pass    
    return render(request, "cart.html", context)


def login_user(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                return redirect('/login')
    return render(request, 'login.html')


def logout_func(request):
    logout(request)
    return redirect('/login')


def order_online(request, pk):
    categories = Category.objects.filter(Q(kitchen=pk) & Q(active=True))
    context = {
        "categories": categories
    }
    return render(request, 'order_online.html', context)


def menu(request, pk):
    items = MenuItem.objects.filter(category_id=pk)
    return render(request, "menu.html", {"items": items})


def overview(request, pk):
    kitchen = Kitchen.objects.get(id=pk)
    images = KitchenGallery.objects.filter(kitchen=kitchen)
    context = {
        "kitchen": kitchen,
        "images": images
    }
    return render(request, 'overview.html', context)


def ratings_and_reviews(request, pk, num):
    kitchen = Kitchen.objects.get(id=pk)
    ratings_paginated = KitchenRatingsAndReviews.objects.filter(kitchen=pk)[:num]
    obj = KitchenRatingsAndReviews.objects.filter(kitchen=pk)
    total_ratings = obj.count()
    ratings_bool = False
    if num < total_ratings:
        ratings_bool = True
    average_ratings = 0
    total_ratings = 0
    five_stars = 0
    four_stars = 0
    three_stars = 0
    two_stars = 0
    one_star = 0
    for i in obj:
        if i.ratings == 5:
            five_stars += 1
        if i.ratings == 4:
            four_stars += 1
        if i.ratings == 3:
            three_stars += 1
        if i.ratings == 2:
            two_stars += 1
        if i.ratings == 1:
            one_star += 1                
        total_ratings += i.ratings
    try:
        average_ratings = round(total_ratings / obj.count(), 2)
        five_stars = (five_stars/obj.count()) * 160
        four_stars = (four_stars/obj.count()) * 160
        three_stars = (three_stars/obj.count()) * 160
        two_stars = (two_stars/obj.count()) * 160
        one_star = (one_star/obj.count()) * 160
    except:
        average_ratings = 0
        five_stars = 0
        four_stars = 0
        three_stars = 0
        two_stars = 0
        one_star = 0

    context = {
        "kitchen": kitchen,
        "ratings_paginated": ratings_paginated,
        "ratings_and_reviews_obj": obj,
        "average_ratings": average_ratings,
        "five_stars": five_stars,
        "four_stars": four_stars,
        "three_stars": three_stars,
        "two_stars": two_stars,
        "one_star": one_star,
        "num": num,
        "ratings_bool": ratings_bool
    }
    return render(request, "ratings-and-reviews.html", context)


class KitchenAPIView(APIView):
    def get_object(self, pk):
        try:
            return Kitchen.objects.get(id=pk)
        except Kitchen.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        kitchen = self.get_object(pk)
        KitchenDetails = KitchenSerializer(kitchen, context={"request": request})
        return Response(KitchenDetails.data)

    def put(self, request, pk):
        kitchen = self.get_object(pk)
        serializer = KitchenSerializer(kitchen, data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@login_required(login_url="/")
def user_location(request):
    return render(request, "user_location.html") 


class KitchenName(APIView):
    def get_object(self, slug):
        try:
            return Kitchen.objects.get(slug=slug)
        except Kitchen.DoesNotExist:
            raise Http404

    def get(self, request, slug):
        kitchen = self.get_object(slug)
        Kitchen = KitchenNameSerializer(kitchen, context={"request": request})
        return Response(Kitchen.data)


class KitchenTimings(APIView):
    def get_object(self, pk):
        try:
            return Timing.objects.filter(kitchen=pk)
        except Timing.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        timings = self.get_object(pk)
        Timings = TimingSerializer(timings, context={"request": request}, many=True)
        return Response(Timings.data)


class CreateOrder(generics.CreateAPIView):
    lookup_field = 'id'
    serializer_class = CreateOrderSerializer
    queryset = Order.objects.all()
    def post(self, request, format=None):
        response = api.payment_request_create(
            amount=request.data.get("actual_amount"),
            buyer_name=request.user.first_name,
            purpose='KitchenAroma Food Delivery',
            send_email=False,
            email=request.user.email,
            phone=request.user.phone_number,
            send_sms=True,
            redirect_url="https://kitchenaroma.co.in/order_history"
        )
        cart_items = Cart.objects.filter(user=request.user)
        kitchen_name = request.data.get("kitchen_name")
        kitchen_obj = Kitchen.objects.get(kitchen_name=kitchen_name)
        total_order_cost_with_delivery = 0
        order_item_ids = []
        for obj in cart_items:
            order = Order()
            order.user = request.user
            order.kitchen = kitchen_obj
            order.item = MenuItem.objects.get(id=obj.item.id)
            order.item_price = order.item.item_price
            order.quantity = obj.quantity
            order.total = order.item.item_price * order.quantity
            order.save()
            order_item_ids.append(order.id)
        order_total = OrderTotal()
        order_total.payment_request_id = response['payment_request']['id']
        order_total.user = request.user
        order_total.kitchen = kitchen_obj
        order_total.total = total_order_cost_with_delivery
        order_total.save()
        order_items = Order.objects.filter(pk__in=order_item_ids)
        for item in order_items:
            order_total.item_order.add(item)
            total_order_cost_with_delivery += (item.total)
        total_order_cost_with_delivery += 40    
        order_total.total = total_order_cost_with_delivery    
        order_total.save()
        return Response(response, status=status.HTTP_201_CREATED)


def contact(request):
    message = ""
    if request.method == "POST":
        contact = Contact()
        contact.full_name = request.POST["name"]
        contact.email = request.POST["email"]
        contact.subject = request.POST["subject"]
        contact.message = request.POST["body"]
        contact.save()
        message = "Your message has been successfully sent. We will contact you very soon!"
        return render(request, "contact.html", {"message": message})
    return render(request, "contact.html")


def terms(request):
    return render(request, "terms.html")


def privacy(request):
    return render(request, "privacy.html")


@login_required(login_url="/")
def order_history(request):
    orders = OrderTotal.objects.filter(user=request.user).order_by('-created_at')
    context = {
        "orders": orders
    }
    return render(request, "order_history.html", context)


class EditOrder(generics.CreateAPIView):
    lookup_field = 'id'
    serializer_class = CreateOrderSerializer
    queryset = Order.objects.all()
    def post(self, request, format=None):
        payment_request_id = request.data.get("payment_request_id")
        order = OrderTotal.objects.get(payment_request_id=payment_request_id)
        order.status = "Pending"
        order.payment_id = request.data.get("payment_id")
        order.save()
        response = {}
        response['payment_id'] = order.payment_id
        response['payment_request_id'] = order.payment_request_id
        cart_items = Cart.objects.filter(user=request.user)
        cart_items.delete()
        return Response(response, status=status.HTTP_201_CREATED)
