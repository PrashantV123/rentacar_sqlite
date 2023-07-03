from django.shortcuts import render, HttpResponseRedirect
from .forms import ReservationForm, AddReservationForm, VehicleForm, dealer_signup_form, customer_signup_form, user_login_form
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from .models import Reservation, Vehicle, DealerLocation
import datetime
from django.db.models import Q
from django.contrib.auth.models import User

# Create your views here.


def homepage(request):
    return render(request, 'sitemain/index.html')


def fleet(request):
    return render(request, 'sitemain/fleet.html')


def promotion(request):
    return render(request, 'sitemain/promotion.html')


def pricing(request):
    return render(request, 'sitemain/pricing.html')


def protection(request):
    return render(request, 'sitemain/protection.html')


def longterm(request):
    return render(request, 'sitemain/longterm.html')


# Dealer SignUp Page


def dealer_signup(request):
    if request.method == "POST":
        form = dealer_signup_form(request.POST)
        if form.is_valid():
            messages.success(
                request, 'Dealer account created successfully!! You may Sign-in now!!')
            user = form.save(commit=False)
            user.is_staff = True
            user.is_superuser = True
            user.save()  # first create user then add user to group
            group = Group.objects.get(name='Dealer')
            user.groups.add(group)
    else:
        form = dealer_signup_form()
    return render(request, 'sitemain/dealersignup.html', {'form': form})

# Customer SignUp Page


def customer_signup(request):
    if request.method == "POST":
        form = customer_signup_form(request.POST)
        if form.is_valid():
            messages.success(
                request, 'Customer account created successfully!! You may Sign-in now!!')
            form.save()

    else:
        form = customer_signup_form()
    return render(request, 'sitemain/customersignup.html', {'form': form})

# LogIn Page


def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = user_login_form(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    # check if dealer has logged in
                    dealer_list = User.objects.filter(groups__name='Dealer')
                    user = request.user
                    if user in dealer_list:
                        return HttpResponseRedirect('/dealerdashboard')
                    # if log in is done by customer
                return HttpResponseRedirect('/reservation_request')
        else:
            form = user_login_form()
        return render(request, 'sitemain/login.html', {'form': form})
    else:
        return HttpResponseRedirect('/reservation_request')

# Logout Page


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

# Customer Methods
# Reservation Page - search for available vehicle


def reservation_request(request):
    if request.method == 'POST':
        fm = ReservationForm(request.POST)
        if fm.is_valid():
            pd = fm.cleaned_data['pickup_date']
            rd = fm.cleaned_data['return_date']
            pl = fm.cleaned_data['pickup_location']
            rl = fm.cleaned_data['return_location']
            ty = fm.cleaned_data['type']

            # conflicting reservation: If status of reservation is close or canceled then do not include in list. condition 1. look into existing reservation at pick up location and find cars that conflict with pickup or return dates or condition 2. there is a oneway reservation for the car(i.e. NJ to IL) in this case if user has same pickup and return location before the oneway reservation make car available otherwise unavailable add them in list or condition 3. there is a oneway reservation for the car (i.e. NJ to IL) just like condition 2 and user requesting to pick up after the return date at pickup location in this case make vehicle unavailable as it is assumed that vehical will be returned to different location(at IL) at returned date.
            reservation = Reservation.objects.filter(pickup_location=pl)
            list = []
            for item in reservation:
                if item.reservation_status == 'Close' or item.reservation_status == 'Canceled':
                    continue
                if not (rd < item.pickup_date or item.return_date < pd) or (item.pickup_location != item.return_location and pl != rl) or (pd > item.return_date and item.pickup_location != item.return_location):
                    list.append(item.vehicle)

            # now add all cars that don't have conflict to the available car list at pick up location
            available_vehicle = []
            vehicle = Vehicle.objects.filter(available_at=pl, type=ty)
            for item in vehicle:
                if item in list:
                    continue
                available_vehicle.append(item)

            # show alternate choice if no vehicle available at pl
            alt_vehicle = []
            vehicle1 = Vehicle.objects.filter(available_at=pl)
            for item in vehicle1:
                if item in list:
                    continue
                alt_vehicle.append(item)

            # return available vehicle and alternate vehicle to showcars.html
            return render(request, 'sitemain/showcars.html', {'vehicle': available_vehicle, 'alt_vehicle': alt_vehicle, 'pd': pd, 'rd': rd, 'pl': pl, 'rl': rl, 'ty': ty})

    else:
        fm = ReservationForm()
    return render(request, 'sitemain/reservation_request.html', {'form': fm})


def addreservation(request, id, pd, rd, pl, rl, ty):
    if request.user.is_authenticated:
        if request.method == "POST":
            fm = AddReservationForm(request.POST)
            if fm.is_valid():
                fm.save()
            return HttpResponseRedirect('/showreservation')
        else:
            customer = request.user
            vehicle = Vehicle.objects.get(pk=id)

            # strptime() to convert string date to date object
            pd = datetime.datetime.strptime(pd, '%Y-%m-%d')
            rd = datetime.datetime.strptime(rd, '%Y-%m-%d')
            # now calculate the difference in days as integer
            days_rented = (rd - pd).days
            # calculate order total based on vehicle type
            if ty == 'Economy':
                order_total = (days_rented * 40)
            elif ty == 'Standard':
                order_total = (days_rented * 70)
            elif ty == 'SUV':
                order_total = (days_rented * 150)
            elif ty == 'Signature Series':
                order_total = (days_rented * 300)

            # taking only date from datetime object to pass in context
            pd = pd.date()
            rd = rd.date()

            pl = DealerLocation.objects.get(location=pl)
            rl = DealerLocation.objects.get(location=rl)

            fm = AddReservationForm(initial={'customer': customer, 'vehicle': vehicle, 'pickup_date': pd, 'return_date': rd,
                                    'pickup_location': pl, 'return_location': rl, 'type': ty,  'days_rented': days_rented, 'order_total': order_total})

            context = {
                'id': id, 'customer': customer, 'vehicle': vehicle, 'pd': pd, 'rd': rd, 'pl': pl, 'rl': rl, 'ty': ty,  'dr': days_rented, 'ot': order_total, 'fm': fm
            }

            return render(request, 'sitemain/addreservation.html', context)
    else:
        return HttpResponseRedirect('/login')


def showreservation(request):
    if request.user.is_authenticated:
        # if request came from dealerdashboard
        dealer_list = User.objects.filter(groups__name='Dealer')
        user = request.user
        if user in dealer_list:
            return HttpResponseRedirect('/dealerreservation')

        reservation = Reservation.objects.filter(
            Q(customer=request.user, reservation_status='Open') | Q(
                customer=request.user, reservation_status='Paid')
        ).order_by('pickup_date')

        re_closed = Reservation.objects.filter(
            customer=request.user, reservation_status='Close').order_by('-pickup_date')

        re_canceled = Reservation.objects.filter(
            customer=request.user, reservation_status='Canceled').order_by('pickup_date')

        context = {'reservation': reservation,
                   'closed_reservation': re_closed, 'canceled_reservation': re_canceled}

        return render(request, 'sitemain/showreservation.html', context)
    else:
        return HttpResponseRedirect('/login')


# cancel reservation


def deletereservation(request, id):
    if request.user.is_authenticated:
        if request.method == "POST":
            re = Reservation.objects.get(pk=id)
            re.reservation_status = 'Canceled'
            re.save()

            # if post request came from dealerdashboard
            dealer_list = User.objects.filter(groups__name='Dealer')
            user = request.user
            if user in dealer_list:
                return HttpResponseRedirect('/dealerreservation')
        return HttpResponseRedirect('/showreservation')
    else:
        return HttpResponseRedirect('/login')


def payreservation(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            re = Reservation.objects.get(pk=id)
            re.reservation_status = 'Paid'
            re.save()

            # if post request came from dealerdashboard
            dealer_list = User.objects.filter(groups__name='Dealer')
            user = request.user
            if user in dealer_list:
                return HttpResponseRedirect('/dealerreservation')
        return HttpResponseRedirect('/showreservation')
    else:
        return HttpResponseRedirect('/login')

# Dealer methods

# dashboard shows all available vehicles and reservations at delership


def dealerdashboard(request):
    if request.user.groups.filter(name__in=['Dealer']).exists():
        if request.method == 'POST':
            fm = VehicleForm(data=request.POST)
            if fm.is_valid():
                fm.save()
                fm = VehicleForm(initial={'customer': request.user, })
        else:
            fm = VehicleForm(initial={'customer': request.user, })

        l = DealerLocation.objects.get(customer=request.user)

        ve = Vehicle.objects.filter(
            customer=request.user) | Vehicle.objects.filter(available_at=l).order_by('type')

        return render(request, 'sitemain/dealerdashboard.html', {'fm': fm, 'vehicle': ve})
    else:
        return HttpResponseRedirect('/logout')


def editvehicle(request, id):
    if request.user.groups.filter(name__in=['Dealer']).exists():
        if request.method == 'POST':
            ve = Vehicle.objects.get(pk=id)
            fm = VehicleForm(request.POST, instance=ve)
            if fm.is_valid():
                fm.save()
            return HttpResponseRedirect('/dealerdashboard')
        else:
            ve = Vehicle.objects.get(pk=id)
            fm = VehicleForm(instance=ve)
        return render(request, 'sitemain/editvehicle.html', {'form': fm})
    else:
        return HttpResponseRedirect('/logout')


def deletevehicle(request, id):
    if request.user.groups.filter(name__in=['Dealer']).exists():
        if request.method == 'POST':
            ve = Vehicle.objects.get(pk=id)
            ve.delete()
        return HttpResponseRedirect('/dealerdashboard')
    else:
        return HttpResponseRedirect('/logout')


def returnvehicle(request, id):
    if request.user.groups.filter(name__in=['Dealer']).exists():
        if request.method == 'POST':
            # set reservation status to close
            re = Reservation.objects.get(pk=id)
            re.reservation_status = 'Close'
            re.save()

            # set vehicle available at return location
            vid = re.vehicle.id
            ve = Vehicle.objects.get(pk=vid)
            ve.available_at = re.return_location
            ve.save()

        return HttpResponseRedirect('/dealerreservation')
    else:
        return HttpResponseRedirect('/logout')


def dealer_reservation(request):
    if request.user.groups.filter(name__in=['Dealer']).exists():
        l = DealerLocation.objects.get(customer=request.user)

        re = Reservation.objects.filter(
            Q(pickup_location=l, reservation_status='Open') | Q(
                return_location=l, reservation_status='Open') | Q(pickup_location=l, reservation_status='Paid') | Q(
                return_location=l, reservation_status='Paid')
        ).order_by('pickup_date')

        re_closed = Reservation.objects.filter(
            pickup_location=l, reservation_status='Close').order_by('-pickup_date')

        re_canceled = Reservation.objects.filter(
            pickup_location=l, reservation_status='Canceled').order_by('pickup_date')

        context = {'reservation': re, 'closed_reservation': re_closed,
                   'canceled_reservation': re_canceled}
        return render(request, 'sitemain/dealerreservation.html', context)

    else:
        return HttpResponseRedirect('/logout')
