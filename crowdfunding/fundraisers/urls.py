from django.urls import path
from .import views

urlpatterns= [
    path('fundraisers/', views.FundraiserList.as_view()),
    path('fundraisers/<int:pk>/', views.FundraiserDetail.as_view()),
    path('pledges/',views.PledgeList.as_view()),
    path('pledges/<int:pk>/',views.PledgeDetail.as_view()),
    path('Bookings/', views.BookingTimeList.as_view()),
    path('Bookings/<int:pk>/', views.BookingTimeDetail.as_view())
]   