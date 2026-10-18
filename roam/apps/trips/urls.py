from django.urls import path

from . import views

app_name = 'trips'

urlpatterns = [
    path('', views.TripIndexView.as_view(), name='index'),
    path('create/', views.TripCreateView.as_view(), name='create'),
    path('<int:pk>/', views.TripDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.TripUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.TripDeleteView.as_view(), name='delete'),
    path("map/", views.map_page, name="map"),
    path("map/data/", views.map_data, name="map_data"),
]
