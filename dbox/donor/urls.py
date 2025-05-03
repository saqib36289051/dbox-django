from django.urls import path
from .views import DonorListCreateView, DonorRetrieveUpdateDestroyView
urlpatterns = [
    path('donor/', DonorListCreateView.as_view()),
    path('donor/<int:pk>/', DonorRetrieveUpdateDestroyView.as_view()),
]