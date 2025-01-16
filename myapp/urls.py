from django.urls import path
from . import views

urlpatterns = [
    path('', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('trains/', views.train_list, name='train_list'),
    path('book/<int:train_id>/', views.book_train, name='book_train'),
    path('my_bookings/', views.my_bookings, name='my_bookings'),
    path('cancel_booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
