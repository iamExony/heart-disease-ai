from rest_framework import generics, permissions
from .models import Prediction
from .serializers import PredictionSerializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

User = get_user_model()

class UserPredictionListView(generics.ListAPIView):
    serializer_class = PredictionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Prediction.objects.all().order_by('-created_at')
        elif user.role == 'clinician':
            # Clinician can see all patients' predictions
            return Prediction.objects.filter(user__role='patient').order_by('-created_at')
        else:
            # Patient sees only their own
            return Prediction.objects.filter(user=user).order_by('-created_at')

class PredictionDetailView(generics.RetrieveAPIView):
    serializer_class = PredictionSerializer
    permission_classes = [IsAuthenticated]
    queryset = Prediction.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Prediction.objects.all()
        elif user.role == 'clinician':
            return Prediction.objects.filter(user__role='patient')
        else:
            return Prediction.objects.filter(user=user)

class UserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role == 'admin':
            clinicians = User.objects.filter(role='clinician').values('id', 'full_name', 'email')
            patients = User.objects.filter(role='patient').values('id', 'full_name', 'email')
            return Response({
                'clinicians': list(clinicians),
                'patients': list(patients)
            })
        elif user.role == 'clinician':
            patients = User.objects.filter(role='patient').values('id', 'full_name', 'email')
            return Response({'patients': list(patients)})
        else:
            return Response({'detail': 'Not allowed'}, status=403)
