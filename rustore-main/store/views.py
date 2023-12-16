import django
from django.contrib.auth.models import User
from store.models import Address, Cart, Category, Order, Product
from django.shortcuts import redirect, render, get_object_or_404
from .forms import RegistrationForm, AddressForm
from django.contrib import messages
from django.views import View
import decimal
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


def home(request):  # получаем категории и товары на главной странице
    categories = Category.objects.filter(is_active=True, is_featured=True)[:3]
    products = Product.objects.filter(is_active=True, is_featured=True)[:8]
    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, 'store/index.html', context)


def about_company(request):
    return render(request, 'store/about_company.html')


def detail(request, slug):  # получаем инфу о товаре и похожий товар
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.exclude(id=product.id).filter(is_active=True, category=product.category)
    context = {
        'product': product,
        'related_products': related_products,

    }
    return render(request, 'store/detail.html', context)


def all_categories(request):  # получаем все категории
    categories = Category.objects.filter(is_active=True)
    return render(request, 'store/categories.html', {'categories': categories})


def category_products(request, slug):  # получаем категории
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(is_active=True, category=category)
    categories = Category.objects.filter(is_active=True)
    context = {
        'category': category,
        'products': products,
        'categories': categories,
    }
    return render(request, 'store/category_products.html', context)


# Authentication Starts Here

class RegistrationView(View):  # получаем форму регистрации
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'account/register.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, "Регистрация прошла успешно!")
            form.save()
        return render(request, 'account/register.html', {'form': form})


@login_required  # Декоратор для представлений, который проверяет, что пользователь вошел в систему, перенаправляя
# на страницу входа, если это необходимо.
def profile(request):  # профиль пользователя, вывод адреса и заказов
    addresses = Address.objects.filter(user=request.user)
    orders = Order.objects.filter(user=request.user)
    return render(request, 'account/profile.html', {'addresses': addresses, 'orders': orders})


@method_decorator(login_required, name='dispatch')
class AddressView(View):  # добавление адреса
    def get(self, request):
        form = AddressForm()
        return render(request, 'account/add_address.html', {'form': form})

    def post(self, request):
        form = AddressForm(request.POST)
        if form.is_valid():
            user = request.user
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            reg = Address(user=user, locality=locality, city=city, state=state)
            reg.save()
            messages.success(request, "Адрес упешно добавлен.")
        return redirect('store:profile')


@login_required  # Декоратор для представлений, который проверяет, что пользователь вошел в систему, перенаправляя
# на страницу входа, если это необходимо.
def remove_address(request, id):  # удаление адреса
    a = get_object_or_404(Address, user=request.user, id=id)
    a.delete()
    messages.success(request, "Адрес удален.")
    return redirect('store:profile')


@login_required  # Декоратор для представлений, который проверяет, что пользователь вошел в систему, перенаправляя
# на страницу входа, если это необходимо.
def add_to_cart(request):  # добавление товара в корзину
    user = request.user
    product_id = request.GET.get('prod_id')
    product = get_object_or_404(Product, id=product_id)

    # Проверка, есть ли товар в корзине или нет
    item_already_in_cart = Cart.objects.filter(product=product_id, user=user)
    if item_already_in_cart:
        cp = get_object_or_404(Cart, product=product_id, user=user)
        cp.quantity += 1
        cp.save()
    else:
        Cart(user=user, product=product).save()

    return redirect('store:cart')


@login_required  # Декоратор для представлений, который проверяет, что пользователь вошел в систему, перенаправляя
# на страницу входа, если это необходимо.
def cart(request):  # корзина
    user = request.user
    cart_products = Cart.objects.filter(user=user)

    # Показывает итог на странице корзины
    amount = decimal.Decimal(0)
    shipping_amount = decimal.Decimal(250)
    # список для расчета общей суммы на основе количества и стоимости
    cp = [p for p in Cart.objects.all() if p.user == user]
    if cp:
        for p in cp:
            temp_amount = (p.quantity * p.product.price)
            amount += temp_amount

    # Customer Addresses
    addresses = Address.objects.filter(user=user)

    context = {
        'cart_products': cart_products,
        'amount': amount,
        'shipping_amount': shipping_amount,
        'total_amount': amount + shipping_amount,
        'addresses': addresses,
    }
    return render(request, 'store/cart.html', context)


@login_required  # Декоратор для представлений, который проверяет, что пользователь вошел в систему, перенаправляя
# на страницу входа, если это необходимо.
def remove_cart(request, cart_id):  # удаление товара из корзины
    if request.method == 'GET':
        c = get_object_or_404(Cart, id=cart_id)
        c.delete()
        messages.success(request, "Товар удален из корзины.")
    return redirect('store:cart')


@login_required  # Декоратор для представлений, который проверяет, что пользователь вошел в систему, перенаправляя
# на страницу входа, если это необходимо.
def plus_cart(request, cart_id):  # прибавление 1 товар в количество в корзине
    if request.method == 'GET':
        cp = get_object_or_404(Cart, id=cart_id)
        cp.quantity += 1
        cp.save()
    return redirect('store:cart')


@login_required  # Декоратор для представлений, который проверяет, что пользователь вошел в систему, перенаправляя
# на страницу входа, если это необходимо.
def minus_cart(request, cart_id):  # удаляет 1 товар в количество в корзине
    if request.method == 'GET':
        cp = get_object_or_404(Cart, id=cart_id)
        # удаляет товар если количество = 1
        if cp.quantity == 1:
            cp.delete()
        else:
            cp.quantity -= 1
            cp.save()
    return redirect('store:cart')


@login_required  # Декоратор для представлений, который проверяет, что пользователь вошел в систему, перенаправляя
# на страницу входа, если это необходимо.
def checkout(request):  # оформление заказа
    user = request.user
    address_id = request.GET.get('address')

    address = get_object_or_404(Address, id=address_id)
    # получаем все товары пользователя в корзине
    cart = Cart.objects.filter(user=user)
    for c in cart:
        # сохраняет все товары из корзины в заказ
        Order(user=user, address=address, product=c.product, quantity=c.quantity).save()
        # удаляет из корзины
        c.delete()
    return redirect('store:orders')


@login_required  # Декоратор для представлений, который проверяет, что пользователь вошел в систему, перенаправляя
# на страницу входа, если это необходимо.
def orders(request):  # заказ
    all_orders = Order.objects.filter(user=request.user).order_by('-ordered_date')
    return render(request, 'store/orders.html', {'orders': all_orders})