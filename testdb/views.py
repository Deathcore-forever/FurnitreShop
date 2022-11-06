from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from .forms import *
from django.contrib.auth import login, logout


def index(request):
    return render(request, 'testdb/index.html', {'title': 'Главная'})


def view_catalog(request):
    furnitures = Furniture.objects.all()
    return render(request, 'testdb/catalog.html', {'furnitures': furnitures, 'title': 'Список товаров'})


def view_login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()

    return render(request, 'testdb/login.html', {'form': form})


def view_logout(request):
    logout(request)
    return redirect('login')


def view_signup(request):
    if request.method == "POST":
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация прошла успешно.")
            return redirect('home')
        else:
            messages.error(request, "Ошибка регистрации.")
    else:
        form = UserSignUpForm()
    return render(request, 'testdb/signup.html', {'form': form})


def view_basket(request):
    basket = Basket.objects.get(client=request.user)
    basket_content = BasketContent.objects.filter(basket=basket)

    sum_row = Furniture.objects.raw("""SELECT fr.id,SUM(fr.price * bsc.quantity) itog FROM testdb_furniture fr 
    inner join testdb_basketcontent bsc on fr.id = bsc.fur_id
    where bsc.basket_id = (SELECT id from testdb_basket where client_id= """+str(request.user.id)+")")
    amount = sum_row[0].itog

    client_id = request.user.id
    basket = Basket.objects.get(client_id=client_id).id

    if request.method == 'POST':
        form = AddressOfOrder(request.POST)
        address = form.data["address"]
        order = Order(order_address=address, amount=amount, paid_for=1, basket_id=basket, client_id=client_id)
        order.save()
        return redirect('profile')
    else:
        form = AddressOfOrder()

    return render(request, 'testdb/basket.html', {'basket': basket_content, 'amount': amount, 'form': form})


def view_basket_delete(request, rec_id):
    BasketContent.objects.filter(id=rec_id).delete()
    return redirect('basket')


def get_product_card(request, fur_id):
    client_id = request.user.id
    User.objects.filter(id=3)

    fur = Furniture.objects.filter(id=fur_id)

    for item in fur:
        maker = Maker.objects.filter(id=item.maker_id)

    if Basket.objects.filter(client=client_id).count() == 0:
        basket = Basket.objects.create(client=request.user)

    fur2 = Furniture.objects.get(id=fur_id)
    bs = Basket.objects.get(client=client_id)

    is_available = True

    if request.method == 'POST':
        form = QuantityOfProduct(request.POST)

        quantity = QuantityOfProduct.check_quantity_value(form, fur2.on_storage)
        if str(quantity) == "None":
            is_available = False
        elif int(quantity) == 0:
            pass
        else:
            bs_content = BasketContent(basket=bs, fur=fur2, quantity=quantity)
            bs_content.save()
            return redirect('basket')
    else:
        form = QuantityOfProduct()
        quantity = None

    return render(request, 'testdb/product-card.html', context={'furniture': fur, 'maker': maker, 'form': form,
                                                                'is_available': is_available, 'quantity': quantity})


def view_user_profile(request):
    return render(request, 'testdb/user-profile.html')
