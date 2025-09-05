from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponseBadRequest
from datetime import datetime, timedelta
from .models import Client, Member, Sport, Reservation, CartItem, Product


def signup_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        birthday = request.POST.get('birthday')
        
        birthday_date = datetime.strptime(birthday, '%Y-%m-%d').date()
        
        if birthday_date >= datetime.now().date():
            messages.error(request, 'Birthday must be before today.')
            return render(request, "signup.html", {})
        
        client = Client(name=name, email=email, password=password, birthday=birthday_date)
        client.save()

        request.session['client_id'] = client.id
        request.session['client_name'] = client.name
        request.session['client_email'] = client.email
        request.session['client_phone'] = client.phone
        
        return render(request, "home.html", {})
    else:
        return render(request, "signup.html", {})




def login_view(request):
    if request.session.get('client_id'):
        client_id = request.session['client_id']
        client_name = request.session.get('client_name', '')
        client_email = request.session.get('client_email', '')
        client_phone = request.session.get('client_phone', '')
        
        context = {
            'client_id': client_id,
            'client_name': client_name,
            'client_email': client_email,
            'client_phone': client_phone,
        }
        return render(request, "client_info.html", context)
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            client = Client.objects.get(email=email)

            if client.password == password:
                request.session['client_id'] = client.id
                request.session['client_name'] = client.name
                request.session['client_email'] = client.email
                request.session['client_phone'] = client.phone
                return render(request, "home.html", {})
            else:
                return render(request, "login.html", {'error_message': 'Incorrect email or password.'})
        except Client.DoesNotExist:
            return render(request, "login.html", {'error_message': 'Incorrect email or password.'})
    else:
        return render(request, "login.html", {})




def logout_view(request):
    logout(request)
    return redirect('login')




def home_view(request):
    return render(request, "home.html", {})




def yoga_view(request):
    return render(request, "yoga.html", {})




def reservation_view(request):
    if request.method == 'POST':
        client_email = request.POST.get('email', None)
        age_range = request.POST.get('age_range', None)
        client_name = request.POST.get('name', None)
        selected_sport = request.POST.get('selectedSport', None)
        hours = request.POST.get('hours', None)
        selected_day = request.POST.get('day', None)
        price = request.POST.get('price', None)
        client_id = request.session.get('client_id')
        client = Client.objects.get(pk=client_id)
        today = datetime.now().date()
        if selected_day:
            days_mapping = {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4}
            selected_day_index = days_mapping.get(selected_day.lower())
            next_day_date = next_weekday(today, selected_day_index)
        try:
            selectedsport = Sport.objects.get(SportName=selected_sport)
        except Sport.DoesNotExist:
            selectedsport = None
            if age_range == 'adult':
                return render(request, 'reservation_adult.html')
            elif age_range == 'kid':
                return render(request, 'reservation_kid.html')
            else:
                return render(request, 'reservation.html')
        if selectedsport:
            selectedsport.nbClients += 1
            selectedsport.save()
            reservation = Reservation(client=client, reserved_sport=selectedsport, reservation_date=next_day_date, price=price)
            reservation.save()
            return render(request, "home.html")
    else:
        return render(request, 'reservation.html')





def membership_view(request):
    if request.method == 'POST':
        Mname = request.POST.get('Mname')
        Memail = request.POST.get('Memail')
        Mphone = request.POST.get('Mphone')
        membership_type = request.POST.get('membership_type')
        
        client_id = request.session.get('client_id')
        client = Client.objects.get(pk=client_id)
        
        member = Member(client=client, Mname=Mname, Memail=Memail, Mphone=Mphone, membership_type=membership_type)
        member.save()

        context = {
            'member': member
        }
        
        return render(request, 'membership_card.html', context)
    else:
        return render(request, 'membership.html', {})





def membership_card_view(request):
    member = Member.objects.last()  
    context = {
        'member': member
    }
    return render(request, 'membership_card.html', context)





def yoga_membership_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        membership_option = request.POST.get('option')

        membership_prices = {
            'year': 499,
            'month': 200,
            'week': 85,
        }

        price = membership_prices.get(membership_option)

        date_options = {
            'year': 'year',
            'month': 'month',
            'week': 'week',
        }

        date_option = date_options.get(membership_option)

        selected_sport = 'yoga'
        reservation_date = datetime.now().date()

        client_id = request.session.get('client_id')
        client = Client.objects.get(pk=client_id)
        try:
            selected_sport_obj = Sport.objects.get(SportName=selected_sport)
        except Sport.DoesNotExist:
            selected_sport_obj = None
        if selected_sport_obj:
            selected_sport_obj.nbClients += 1
            selected_sport_obj.save()
            reservation = Reservation(
                client=client,
                reserved_sport=selected_sport_obj,
                reservation_date=reservation_date,
                price=price,
                date_option=date_option
            )
            reservation.save()

        return render(request, 'yoga.html', {})
    else:
        return render(request, 'yoga_membership.html', {})





def gym_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        membership_option = request.POST.get('membership')

        membership_prices = {
            'yearly': 500,
            'monthly': 50,
            'weekly': 10,
        }

        price = membership_prices.get(membership_option)

        date_options = {
            'yearly': 'year',
            'monthly': 'month',
            'weekly': 'week',
        }

        date_option = date_options.get(membership_option)

        selected_sport = 'gym'
        reservation_date = datetime.now().date()

        client_id = request.session.get('client_id')
        client = Client.objects.get(pk=client_id)
        try:
            selected_sport_obj = Sport.objects.get(SportName=selected_sport)
        except Sport.DoesNotExist:
            selected_sport_obj = None
        if selected_sport_obj:
            selected_sport_obj.nbClients += 1
            selected_sport_obj.save()
            reservation = Reservation(
                client=client,
                reserved_sport=selected_sport_obj,
                reservation_date=reservation_date,
                price=price,
                date_option=date_option
            )
            reservation.save()

        return render(request, 'home.html', {})
    else:
        return render(request, 'gym.html', {})





def next_weekday(d, weekday):
    days_until_next_day = (weekday - d.weekday()) % 7
    if days_until_next_day == 0:
        days_until_next_day = 7
    return d + timedelta(days=days_until_next_day)






def product_list(request):
    products = Product.objects.all()
    cart_item_count = CartItem.objects.count()
    return render(request, 'product_list.html', {'products': products})






def detail(request, pk):
    item = get_object_or_404(Product, pk=pk)
    return render(request, 'detail.html', {'item': item})






def cart(request):
    client_id = request.session.get('client_id')
    if not client_id:
        messages.error(request, 'You need to log in to view the cart.')
        return redirect('login')
    client = get_object_or_404(Client, pk=client_id)
    cart_items = CartItem.objects.filter(client=client)
    total_cart_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_cart_price': total_cart_price})





@require_POST
def checkout(request):
    client_id = request.session.get('client_id')
    if not client_id:
        return JsonResponse({'message': 'You need to log in to checkout.'}, status=403)
    
    client = get_object_or_404(Client, pk=client_id)
    cart_items = CartItem.objects.filter(client=client)

    for cart_item in cart_items:
        product = cart_item.product
        product.quantity -= cart_item.quantity
        product.save()

    CartItem.objects.filter(client=client).delete()

    return JsonResponse({'message': 'Checkout successful'})





def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, pk=item_id)
    cart_item.delete()
    return redirect('cart')






def update_cart(request, item_id):
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        cart_item = get_object_or_404(CartItem, pk=item_id)
        if quantity:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated successfully.')
        else:
            messages.error(request, 'Invalid quantity.')
    
    return redirect('cart')




@require_POST
def add_to_cart(request, pk):
    client_id = request.session.get('client_id')
    if not client_id:
        messages.error(request, 'You need to log in to add items to the cart.')
        return redirect('login')
    client = get_object_or_404(Client, pk=client_id)
    product = get_object_or_404(Product, pk=pk)
    quantity = int(request.POST.get('quantity', 1))
    cart_item, created = CartItem.objects.get_or_create(product=product, client=client)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity

    cart_item.save()
    return redirect('cart')






def swimming_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        membership_option = request.POST.get('membership')
        coach = request.POST.get('instructor')
        price = request.POST.get('price')

        date_options = {
            'yearly': 'year',
            'monthly': 'month',
            'weekly': 'week',
        }

        date_option = date_options.get(membership_option)
        selected_sport = 'swimming'
        reservation_date = datetime.now().date()

        client_id = request.session.get('client_id')
        client = Client.objects.get(pk=client_id)
        try:
            selected_sport_obj = Sport.objects.get(SportName=selected_sport)
        except Sport.DoesNotExist:
            selected_sport_obj = None
        if selected_sport_obj:
            selected_sport_obj.nbClients += 1
            selected_sport_obj.save()
            reservation = Reservation(
                client=client,
                reserved_sport=selected_sport_obj,
                reservation_date=reservation_date,
                price=price,
                date_option=date_option,
                coach=coach
            )
            reservation.save()

        return render(request, 'swimming.html', {})
    else:
        return render(request, 'swimming.html', {})
