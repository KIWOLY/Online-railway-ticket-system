from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Train, Booking
from django.contrib import messages
from django.contrib.auth.models import User


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Validate the inputs
        if not username or not email or not password1 or not password2:
            messages.error(request, "All fields are required.")
            return redirect('signup')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('signup')

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        messages.success(request, "Signup successful! Please log in.")
        return redirect('login')

    return render(request, 'signup.html')





def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def train_list(request):
    if request.method == 'POST':
        source = request.POST['source']
        destination = request.POST['destination']
        trains = Train.objects.filter(source=source, destination=destination)
    else:
        trains = Train.objects.all()
    return render(request, 'train_list.html', {'trains': trains})

@login_required
def book_train(request, train_id):
    train = get_object_or_404(Train, id=train_id)
    if request.method == 'POST':
        seats = int(request.POST['seats'])
        if train.seats_available >= seats:
            Booking.objects.create(user=request.user, train=train, seats_booked=seats)
            train.seats_available -= seats
            train.save()
            messages.success(request, "Booking successful!")
            return redirect('my_bookings')
        else:
            messages.error(request, "Not enough seats available.")
    return render(request, 'book_train.html', {'train': train})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'my_bookings.html', {'bookings': bookings})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    train = booking.train
    train.seats_available += booking.seats_booked
    train.save()
    booking.delete()
    messages.success(request, "Booking cancelled successfully.")
    return redirect('my_bookings')

