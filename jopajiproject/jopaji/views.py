import uuid

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from .models import Banner, user_client, category_master, tbl_product, ProfileVerification, Cart, OrderPlaced, address
from .forms import ContactForm, FranchiseForm, CustomerRegistration, CustomerLogin, UserAddress
from django.views import View
from django.contrib import messages
from django.db.models import Count, Q
from django.contrib.auth import authenticate, login
from .utils import generate_otp, send_otp_email, OTP_EXPIRY_DURATION, send_email_token
import time

# Create your views here.
def index(request):
    category_data = category_master.objects.all()
    client_data = user_client.objects.all()
    banner_data = Banner.objects.filter(page_name='homepage')
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


def get_pro_details(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        product = tbl_product.objects.get(id=prod_id)
        data = {
            "product_id": product.id,
            "product_name": product.productname,
            "product_short_description": product.short_description,
            "product_mrp": product.mrp,
            "product_image": product.image1.url
        }
    return JsonResponse(data)


@login_required(login_url="/login/")
def add_to_cart(request):
    if request.method == 'POST':
        user = request.user
        pro_id = request.POST.get("pro_id")
        product = tbl_product.objects.get(id=pro_id)
        pro_qty = request.POST.get("pro_qty")
        print(user, pro_id, pro_qty, product)

        # check product existance
        def product_in_cart(user, product):
            # Query the Cart model to check if the product exists for the user
            return Cart.objects.filter(user=user, product=product).exists()

        # user is the user instance and product is the product instance you want to check
        if product_in_cart(user, product):
            messages.warning(request, 'The product already exists. You can increase their quantity.')
        else:
            Cart(user=user, product=product, quantity=pro_qty).save()
        return redirect("cart")

@login_required(login_url="/login/")
def cart(request):
    # get product details
    cart_data = Cart.objects.filter(user=request.user)
    amount = 0.0
    shipping_amount = 40.0
    total_amt = 0.0
    cart_product = [p for p in cart_data]
    if cart_product:
        for product_amt in cart_product:
            tempamt = round(float(product_amt.quantity) * float(product_amt.product.mrp), 2)
            amount += tempamt
            total_amt = amount + shipping_amount
    context = {
        'datas': cart_data,
        'amount': amount,
        'shipping_amount': shipping_amount,
        'total_amt': total_amt
    }
    return render(request, 'addtocart.html', context)


def pluscart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 40.0
        total_amt = 0.0
        cart_product = [p for p in Cart.objects.filter(user=request.user)]
        if cart_product:
            for product_amt in cart_product:
                tempamt = round(float(product_amt.quantity) * float(product_amt.product.mrp), 2)
                amount += tempamt
                total_amt = amount + shipping_amount
            data = {
                'quantity': c.quantity,
                'amount': amount,
                'shipping_amount': shipping_amount,
                'total_amt': total_amt
            }
            return JsonResponse(data)


def minuscart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping_amount = 40.0
        total_amt = 0.0
        cart_product = [p for p in Cart.objects.filter(user=request.user)]
        if cart_product:
            for product_amt in cart_product:
                tempamt = round(float(product_amt.quantity) * float(product_amt.product.mrp), 2)
                amount += tempamt
                total_amt = amount + shipping_amount
            data = {
                'quantity': c.quantity,
                'amount': amount,
                'shipping_amount': shipping_amount,
                'total_amt': total_amt
            }
            return JsonResponse(data)


def removecart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 40.0
        total_amt = 0.0
        cart_product = [p for p in Cart.objects.filter(user=request.user)]
        if cart_product:
            for product_amt in cart_product:
                tempamt = round(float(product_amt.quantity) * float(product_amt.product.mrp), 2)
                amount += tempamt
                total_amt = amount + shipping_amount
            data = {
                'cart_len': len(cart_product),
                'amount': amount,
                'shipping_amount': shipping_amount,
                'total_amt': total_amt
            }
        else:
            data = {
                'cart_len': len(cart_product),
                "HTML": '<div class="text-center mb-5"><h1 class="mb-3 text-dark">Cart is empty.</h1><p>Please add some products in cart.</p><a href="/product/" class="btn btn-primary">Shop Now</a></div>'
            }
        return JsonResponse(data)


@login_required(login_url="/login/")
def checkout(request):
    add = address.objects.filter(admin_name=request.user)
    cart_list = [p for p in Cart.objects.filter(user=request.user)]
    amount = 0.0
    shipping_charge = 40.0
    total_amt = 0.0
    print(cart_list)
    if cart_list:
        for x in cart_list:
            temp_amt = round(float(x.quantity) * float(x.product.mrp), 2)
            amount += temp_amt
            total_amt = amount + shipping_charge
        context = {
            'add': add,
            'total_amt': total_amt,
            'cart_lists': cart_list
        }
        return render(request, 'checkout.html', context)
    else:
        return redirect("product")



@login_required(login_url="/login/")
def payment_done(request):
    user = request.user
    cust_id = request.GET.get('address')
    if cust_id is not None:
        customer = address.objects.get(id=cust_id)
        print(cust_id, customer)
        cart_item = Cart.objects.filter(user=user)
        for product_item in cart_item:
            OrderPlaced(user=user, customer=customer, product=product_item.product, quantity=product_item.quantity, status='pending').save()
            product_item.delete()
        return redirect('orders')
    else:
        messages.warning(request, 'You need add at least one address.')
        return redirect('address')


def orders(request):
    order_data = OrderPlaced.objects.all()
    order_len = len([p for p in order_data])
    if request.method == 'POST':
        order_id = request.POST['order_id']
        order = OrderPlaced.objects.get(id=order_id)
        print(order, order.status)
        order.status = 'cancelled'
        order.save()
        return redirect('order cancelled')
    data = {
        'datas': order_len,
        'order_datas': order_data,
    }
    return render(request, 'orders.html', data)


def order_cancelled(request):
    return render(request, 'order-cancelled.html')

# Contact Us page.
class book_order(View):
    def get(self, request):
        banner_data = Banner.objects.filter(page_name='book_order')
        form = CustomerRegistration()
        formLogin = CustomerLogin()
        data = {
            'sub_banners': banner_data,
            'form': form,
            'formLogins': formLogin
        }
        return render(request, 'book-order.html', data)

    def post(self, request):
        banner_data = Banner.objects.filter(page_name='book_order')
        form = CustomerRegistration(request.POST)
        formLogin = CustomerLogin(request, request.POST)
        formName = request.POST['form_name']
        print(formLogin.errors, formName)
        if formName == 'signup_form' and form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Your account has been created, please verify your email first to login your account.')

            return HttpResponseRedirect('/book-order')
        elif formName == 'login_form' and formLogin.is_valid():
            username = formLogin.cleaned_data['username']
            password = formLogin.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                request.session['username'] = username
                request.session['password'] = password
                # login(request, user)
                return HttpResponseRedirect('/email-otp')
        data = {
            'sub_banners': banner_data,
            'form': form,
            'formLogins': formLogin
        }
        return render(request, 'book-order.html', data)


def email_sent(request):
    username = request.session.get('username')
    # Generate OTP with timestamp
    otp, timestamp = generate_otp()

    # Send OTP via email
    send_otp_email(username, otp)
    request.session['otp'] = otp
    request.session['otp_expiry'] = timestamp + OTP_EXPIRY_DURATION
    return redirect('verify otp')


def verify_otp(request):
    ses_username = request.session.get('username')
    ses_password = request.session.get('password')
    # if ses_username:
    if request.method == 'POST':
        otp = request.POST.get('otp')
        print(otp)
        if otp:
            otp_entered = request.POST.get('otp')
            ses_otp = request.session.get('otp')
            ses_otp_expiry = request.session.get('otp_expiry')
            if ses_otp == otp_entered and time.time() < ses_otp_expiry:
                # OTP is valid and within the expiry time
                # Proceed with password reset logic

                # Clear OTP-related session data
                del request.session['otp']
                del request.session['otp_expiry']
                user = authenticate(username=ses_username, password=ses_password)
                login(request, user)
                return HttpResponseRedirect('/profile-user')
            else:
                messages.add_message(request, messages.WARNING, 'Invalid OTP. Please enter OTP again.')
        # else:
        #     return redirect('/')
    data = {
        'ses_username': ses_username
    }
    return render(request, 'verify-otp.html', data)


def profile_user(request):
    user = request.user
    email = user.email
    try:
        ProfileID = ProfileVerification.objects.get(user=user)
        ProfileEmail = ProfileID.email
        print(ProfileID, ProfileEmail, ProfileVerification.objects.get(user=user).email)
    except:
        form = ProfileVerification(user=user, email=email)
        print('email registered.')
        form.save()
    return redirect("/dashboard")


def dashboard(request):
    return render(request, 'dashboard.html')


@method_decorator(login_required, name='dispatch')
class AddAddress(View):
    def get(self, request, id=None):
        form = UserAddress(instance=get_object_or_404(address, pk=id, admin_name=request.user) if id else None)
        return render(request, 'address.html', {'form': form, 'id': id})

    def post(self, request, id=None):
        form = UserAddress(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.admin_name = request.user
            instance.save()
            messages.success(request, 'New address has been created...' if id is None else 'Your Address has been updated...')
            return redirect('address view')
        return render(request, 'address.html', {'form': form})


def addressShow(request):
    address_data = address.objects.all()
    data = {
        'address_data': address_data
    }
    print(address_data)
    if request.method == 'POST':
        add_id = request.POST.get('add_id')
        print(add_id)
        address(admin_name=request.user, id=add_id).delete()
        messages.success(request, 'Address has been deleted...')
        return redirect('address view')
    return render(request, 'address-view.html', data)


def user_verification(request):
    user = request.user
    instance = ProfileVerification.objects.get(user=user)
    email = instance.email
    check_token = instance.email_token
    check_ver = instance.email_verified
    # print(user, email, check_ver, check_token)
    if request.method == 'POST':
        email_token = str(uuid.uuid4())
        send_email_token(email, email_token)
        instance.email_token = email_token
        instance.save()
        return redirect('email sent')
    data = {
        'email': email,
        'check_ver': check_ver,
        'check_token': check_token,
    }
    return render(request, 'user-verification.html', data)


def ver_email_sent(request):
    return render(request, 'ver-email-sent.html')


def email_verification(request, slug):
    instance = get_object_or_404(ProfileVerification, email_token=slug)
    if not instance.email_verified:
        instance.email_verified = True
        instance.save()
        print(slug, instance)
        return redirect('user verification')
    else:
        return HttpResponse("<h1>Invalid Link</h1>")