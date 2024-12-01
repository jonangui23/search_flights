from django.urls import path
from members import views  # Import the views from the 'members' app

urlpatterns = [
    path('', views.user_input, name='home'),  
    path('results', views.flight_search, name='results')  
]
