from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse


from carts.models import Cart, CartItem
from orders.models import Order, OrderItem
from users.forms import ProfileForm, UserLoginForm, UserRegistrationForm

def login(request):
    """Логинелка"""

    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            
            # Обработка сессионного ключа для того чтобы карзина не потерялась при авторизации
            session_key = request.session.session_key

            if user:
                auth.login(request, user)
                messages.success(request, f"{username}, Вы вошли в аккаунт")

                # Перезапись ключа сессии на авторизовавшегося пользователя
                if session_key:
                    # Проверяем нет ли у пользователя корзины
                    user_cart = Cart.objects.filter(user=request.user).first()
                    if user_cart:
                        cart_items_session = CartItem.objects.filter(session_key=session_key)
                        if cart_items_session.exists():
                            # Получаем первую строку корзины из сессии чтобы найти её корзину
                            cart_item = cart_items_session.first()
                            old_cart = Cart.objects.filter(id=cart_item.cart.id).first()

                            # Берём товары в корзине на аккаунте
                            cart_items_user = CartItem.objects.filter(cart=user_cart)

                            # Если есть эоементы корзины с одинаковыми продуктами соединяем их в одну пользовательскую корзину после авторизации
                            for cart_item_user in cart_items_user:
                                for cart_item_session in cart_items_session:
                                    if cart_item_user.product == cart_item_session.product:
                                        cart_item_user.quantity = cart_item_user.quantity + cart_item_session.quantity
                                        cart_item_user.save()

                            for cart_item_user in cart_items_user:
                                for cart_item_session in cart_items_session:
                                    if cart_item_user.product == cart_item_session.product:
                                        cart_item_session.delete()

                            cart_items_session.update(cart=user_cart)
                            old_cart.delete()

                                
                    else:
                        # Ищем все элементы корзины
                        cart_items = CartItem.objects.filter(session_key=session_key)
                        if cart_items.exists():
                            cart_item = cart_items.first()
                            cart = Cart.objects.filter(id=cart_item.cart.id).first()
                            #Обновляем пользователя для корзины (тут она должна быть одна в списке)
                            cart.user = user
                            cart.save()

                redirect_page = request.POST.get('next', None)
                if redirect_page and redirect_page != reverse('user:logout'):
                    return HttpResponseRedirect(request.POST.get('next'))
                
                return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserLoginForm()
    
    context={
        'title':'Asia - Авторизация',
        'form': form,
    }
    return render(request,'users/login.html',context)

def registration(request):
    """Регистраци"""
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()

            # Обработка сессионного ключа для того чтобы карзина не потерялась при авторизации
            session_key = request.session.session_key

            user = form.instance
            auth.login(request, user)

            # Перезапись ключа сессии на авторизовавшегося пользователя
            if session_key:
                    # Ищем все элементы корзины
                cart_items = CartItem.objects.filter(session_key=session_key)
                if cart_items.exists():
                    cart_item = cart_items.first()
                    cart = Cart.objects.filter(id=cart_item.cart.id).first()
                    #Обновляем пользователя для корзины (тут она должна быть одна в списке)
                    cart.user = user
                    cart.save()

            messages.success(request, f"{user.username}, Вы успешно зарегистрированы и вошли в аккаунт")
            return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserRegistrationForm()

    context={
        'title':'Регистрация',
        'form': form
    }
    return render(request,'users/registration.html',context)


@login_required # Декоратор для запрета доступа к контроллеру БЕЗ авторизации
def profile(request):
    """Профиль"""
    if request.method == 'POST':
        form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль успешно обновлён")
            return HttpResponseRedirect(reverse('user:profile'))
    else:
        form = ProfileForm(instance=request.user)

    # prefetch_related 
    orders = Order.objects.filter(user=request.user).prefetch_related(
                Prefetch(
                    "orderitem_set",
                    queryset=OrderItem.objects.select_related("product"),
                )
            ).select_related('order_status').order_by("-id")

    context={
        'title':'Личный кабинет',
        'form': form,
        'orders': orders
    }
    return render(request,'users/profile.html',context)

def users_cart(request):
        
    context={
        'title':'Корзина'
    }
    return render(request, 'users/users_cart.html', context)

@login_required
def logout(request):
    messages.success(request, f"{request.user.username}, Вы вышли из аккаунта")
    auth.logout(request)
    return redirect(reverse('main:index'))