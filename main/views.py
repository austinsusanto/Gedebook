from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.urls import reverse
from django.core import serializers
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from main.forms import ProductForm, GedebookUserCreationForm
from main.models import Product
import datetime


@login_required(login_url='/login')
def show_main(request):
    products = Product.objects.filter(user=request.user)

    for product in products:
        if len(product.description) > 200:
            product.description = product.description[:200] + "..."

    context = {
        'name': request.user.username,
        'products': products,
        'product_count': len(products),
        'last_login': request.COOKIES['last_login'],
    }

    return render(request, "main.html", context)


def create_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        product = form.save(commit=False)
        product.user = request.user
        product.save()
        return HttpResponseRedirect(reverse('main:show_main'))

    context = {'form': form}
    return render(request, "create_product.html", context)


def show_xml(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")


def show_json(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


def show_xml_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")


def show_json_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


def register(request):
    form = GedebookUserCreationForm()

    if request.method == "POST":
        form = GedebookUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Your account has been successfully created!")
            return redirect('main:login')

    context = {'form': form}
    return render(request, 'register.html', context)


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.info(
                request, 'Sorry, incorrect username or password. Please try again.')

    context = {}
    return render(request, 'login.html', context)


def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response


def delete_product(request, id):
    deleted_product = Product.objects.filter(pk=id)
    deleted_product.delete()
    return HttpResponseRedirect(reverse('main:show_main'))


def add_product_by_one(request, id):
    added_product = Product.objects.get(pk=id)
    added_product.amount += 1
    added_product.save()
    return HttpResponseRedirect(reverse('main:show_main'))


def reduce_product_by_one(request, id):
    reduced_product = Product.objects.get(pk=id)
    if reduced_product.amount == 1:
        return delete_product(request, id)

    reduced_product.amount -= 1
    reduced_product.save()
    return HttpResponseRedirect(reverse('main:show_main'))

def edit_product(request, id):
    product = Product.objects.get(pk=id)
    form = ProductForm(request.POST or None, instance=Product)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('main:show_main'))

    context = {'form':form}
    return render(request, "edit_product.html", context)

def get_product_json(request):
    product_item = Product.objects.all()
    print(serializers.serialize('json', product_item))
    return HttpResponse(serializers.serialize('json', product_item))

@csrf_exempt
def add_product_ajax(request):
    if request.method == "POST":
        name = request.POST.get("name")
        amount = request.POST.get("amount")
        description = request.POST.get("description")
        user = request.user

        new_product = Product(name=name, amount=amount, description=description, user=user)
        new_product.save()

        return HttpResponse(b"CREATED", status=201)
    
    return HttpResponseNotFound()