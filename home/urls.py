from django.urls import path
from . import views

urlpatterns = [
    path('view/',views.BlogView.as_view(), name='blogview'),


    path('<int:pk>/', views.BlogDetailAPIView.as_view(), name='BlogDetailAPIView'),


    path('list/', views.BlogListView.as_view(), name='list-view'),


]
