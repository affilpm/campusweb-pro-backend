from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import status
from .models import AdmissionSettings, AdmissionStep
from django.shortcuts import get_object_or_404

from apps.school_info.models import SiteSettings, QuickLink
from apps.school_info.serializers import SiteSettingsPublicSerializer, QuickLinkPublicSerializer
from .serializers import (
    AdmissionSettingsPublicSerializer, AdmissionSettingsAdminSerializer,
    AdmissionStepAdminSerializer
)

# ==================== PUBLIC VIEWS ====================

class AdmissionsPagePublicView(APIView):
    """
    GET /api/public/admissions/
    """
    permission_classes = [AllowAny]

    def get(self, request):
        settings = AdmissionSettings.load()
        site_settings = SiteSettings.load()
        quick_links = QuickLink.objects.filter(is_active=True).order_by('order')
        
        data = AdmissionSettingsPublicSerializer(settings, context={'request': request}).data
        data['site_settings'] = SiteSettingsPublicSerializer(site_settings, context={'request': request}).data
        data['quick_links'] = QuickLinkPublicSerializer(quick_links, many=True, context={'request': request}).data
        
        return Response(data)

class AdmissionStatusPublicView(APIView):
    """
    GET /api/public/admissions/status/
    Returns only simple status
    """
    permission_classes = [AllowAny]

    def get(self, request):
        settings = AdmissionSettings.load()
        return Response({'is_open': settings.is_open})

# ==================== ADMIN VIEWS ====================

class AdmissionSettingsAdminView(APIView):
    """
    GET/PUT /api/admin/admissions/settings/
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        settings = AdmissionSettings.load()
        return Response(AdmissionSettingsAdminSerializer(settings, context={'request': request}).data)

    def put(self, request):
        settings = AdmissionSettings.load()
        serializer = AdmissionSettingsAdminSerializer(settings, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        return self.put(request)

class AdmissionStepAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        steps = AdmissionStep.objects.all().order_by('order')
        return Response(AdmissionStepAdminSerializer(steps, many=True, context={'request': request}).data)
        
    def post(self, request):
        serializer = AdmissionStepAdminSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdmissionStepDetailAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get_object(self, pk):
        return get_object_or_404(AdmissionStep, pk=pk)
    
    def put(self, request, pk):
        step = self.get_object(pk)
        serializer = AdmissionStepAdminSerializer(step, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        return self.put(request, pk)
        
    def delete(self, request, pk):
        step = self.get_object(pk)
        step.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
