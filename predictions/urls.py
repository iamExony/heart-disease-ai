from django.urls import path
from .views import predict_clinical
from .api_views import UserPredictionListView, PredictionDetailView, UserListView

urlpatterns = [
    path('predict/clinical/', predict_clinical, name='predict_clinical'),
    path('predictions/', UserPredictionListView.as_view(), name='user-predictions'),
    path('predictions/<int:pk>/', PredictionDetailView.as_view(), name='prediction-detail'),
    path('users/', UserListView.as_view(), name='user-list'),
]
