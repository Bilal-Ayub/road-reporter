from django.urls import path
from . import views

app_name = 'reporter'
urlpatterns = [
    path('', views.login_view, name='login'),  # Set the root URL to the login view
    path('index/', views.index, name='index'),  # Add this line for index view
    path('login/', views.login_view, name='login'),  # Login URL
    path('register/', views.register_view, name='register'),
    path('reports/', views.reports, name='reports'),
    path('new_report/', views.new_report, name='new_report'),
    path('map_view/', views.map_view, name='map_view'),
    path('paginated_reports/', views.paginate_reports, name='paginated_reports'),
]