from django.shortcuts import render, redirect
from .models import Kitchen, Category, Cart, MenuItem, KitchenRatingsAndReviews, KitchenGallery
from .serializers import CartSerializer, KitchenSerializer, CartSerializerWithDepth
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
from .models import Cart, Kitchen
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework import generics, permissions, status

# Create your views here.
def home(request):
    kitchens = Kitchen.objects.all()
    context = {'kitchens': kitchens}
    return render(request, 'home.html', context)


def kitchen(request, kitchen):
    kitchen_obj =  Kitchen.objects.get(slug=kitchen)
    category_obj = Category.objects.filter(kitchen=kitchen_obj)
    context = {'kitchen': kitchen_obj, 'categories': category_obj}
    return render(request, 'kitchen.html', context)


@permission_classes((AllowAny,))
class AddItemToCart(viewsets.ViewSet):
    def cart_items(self, request):
        queryset = Cart.objects.all()
        serializer = CartSerializer(queryset, many=True)
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
    context = {
        'items': cart_items,
        "item_word": item_word,
        "total_cost": total_cost,
        "cart_bool": cart_bool
    }
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
