from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Banner, user_client, category_master, tbl_product
from .forms import ContactForm, FranchiseForm, RegUser, UserLogin
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db.models import Count

# Create your views here.
def index(request):
    category_data = category_master.objects.all()
    client_data = user_client.objects.all()
    banner_data = Banner.objects.filter(page_name='homepage')
    if request.user.is_authenticated:
        # User is authenticated, get the username
        username = request.user.username
        print("Username:", username)
    else:
        # User is not authenticated
        print("User is not authenticated.")
    data = {
        'banners': banner_data,
        'clients': client_data,
        'categories': category_data
    }
    return render(request, 'index.html', data)


# About Us page.
def about_us(request):
    banner_data = Banner.objects.filter(page_name='about_us')
    data = {
        'sub_banners': banner_data
    }
    return render(request, 'about_us.html', data)


# Franchise page.
def franchise(request):
    banner_data = Banner.objects.filter(page_name='franchise')
    if request.method == 'POST':
        form = FranchiseForm(request.POST)
        if form.is_valid():
            form.save()
            form = FranchiseForm()
            messages.add_message(request, messages.SUCCESS,
                                 "Thank you for contacting us. Our team will shortly call you.")
    else:
        form = FranchiseForm()
    data = {
        'sub_banners': banner_data,
        'form': form
    }
    return render(request, 'franchise.html', data)


# our Menu page.
def our_menu(request):
    banner_data = Banner.objects.filter(page_name='menu')
    category_data = category_master.objects.filter(status=True).order_by('cat_name')
    data = {
        'sub_banners': banner_data,
        'categories': category_data,
    }
    print(category_data)
    return render(request, 'our-menu.html', data)


# Contact Us page.
def contact_us(request):
    banner_data = Banner.objects.filter(page_name='contact_us')
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,
                                 "Thank you for contacting us. Our team will shortly call you.")
    else:
        form = ContactForm()
    data = {
        'sub_banners': banner_data,
        'form': form
    }
    return render(request, 'contact-us.html', data)


# Contact Us page.
def book_order(request):
    banner_data = Banner.objects.filter(page_name='book_order')
    form = RegUser()
    login_form = UserLogin()
    if request.method == "POST":
        if request.POST.get('form_name') == 'signup_form':
            print('worked')
            form = RegUser(request.POST)

            print(form.errors)
            print(form)
            if form.is_valid():
                messages.success(request, 'The user has been created successfully.')
                form.save()
        elif request.POST.get('form_name') == 'login_form':
            login_form = UserLogin(request.POST)
            print("errors", login_form.errors)
            if login_form.is_valid():
                username = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'The user has been created successfully.')
                    return HttpResponseRedirect('/admin/')
    else:
        form = RegUser()
        login_form = UserLogin()
    data = {
        'sub_banners': banner_data,
        'form': form,
        'login_form': login_form
    }
    return render(request, 'book-order.html', data)


def product_list(request, slug):
    category_data_slug = get_object_or_404(category_master, slug=slug)
    product_data = tbl_product.objects.filter(category=category_data_slug)
    category_data = category_master.objects.filter(slug = category_data_slug)
    categories_with_count = category_master.objects.annotate(product_count=Count('tbl_product'))
    data = {
        'slug': slug,
        'prod_data': product_data,
        'categories_with_count': categories_with_count,
        'cat_data': category_data
    }
    print(product_data, category_data)
    return render(request, 'product-list.html', data)
