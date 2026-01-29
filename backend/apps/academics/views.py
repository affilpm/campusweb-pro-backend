from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from apps.school_info.models import SiteSettings, QuickLink
from apps.school_info.serializers import SiteSettingsPublicSerializer, QuickLinkPublicSerializer
from .models import AcademicsPage, ClassCategory, Subject
from .serializers import (
    AcademicsPagePublicSerializer, ClassCategoryPublicSerializer, SubjectPublicSerializer,
    AcademicsPageAdminSerializer, ClassCategoryAdminSerializer, SubjectAdminSerializer
)

class AcademicsPagePublicView(APIView):
    """
    GET /api/public/academics/
    """
    permission_classes = [AllowAny]

    def get(self, request):
        page = AcademicsPage.load()
        categories = ClassCategory.objects.filter(is_active=True).order_by('order')
        site_settings = SiteSettings.load()
        quick_links = QuickLink.objects.filter(is_active=True).order_by('order')
        
        # Structure subjects by category for the frontend
        categories_data = []
        for category in categories:
            cat_serializer = ClassCategoryPublicSerializer(category, context={'request': request})
            subjects = category.subjects.filter(is_active=True).order_by('order')
            subjects_serializer = SubjectPublicSerializer(subjects, many=True, context={'request': request})
            cat_data = cat_serializer.data
            cat_data['subjects'] = subjects_serializer.data
            categories_data.append(cat_data)
        
        # Flatten response: Start with page content and add categories
        data = AcademicsPagePublicSerializer(page, context={'request': request}).data
        data['class_categories'] = categories_data
        data['site_settings'] = SiteSettingsPublicSerializer(site_settings, context={'request': request}).data
        data['quick_links'] = QuickLinkPublicSerializer(quick_links, many=True).data
        
        return Response(data)

# Admin Views
class AcademicsPageAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request):
        page = AcademicsPage.load()
        return Response(AcademicsPageAdminSerializer(page, context={'request': request}).data)

    def put(self, request):
        page = AcademicsPage.load()
        serializer = AcademicsPageAdminSerializer(page, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClassCategoryAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get(self, request):
        items = ClassCategory.objects.all()
        return Response(ClassCategoryAdminSerializer(items, many=True, context={'request': request}).data)

    def post(self, request):
        serializer = ClassCategoryAdminSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClassCategoryDetailAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request, pk):
        item = get_object_or_404(ClassCategory, pk=pk)
        return Response(ClassCategoryAdminSerializer(item, context={'request': request}).data)

    def put(self, request, pk):
        category = get_object_or_404(ClassCategory, pk=pk)
        serializer = ClassCategoryAdminSerializer(category, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        return self.put(request, pk)

    def delete(self, request, pk):
        item = get_object_or_404(ClassCategory, pk=pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SubjectAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get(self, request):
        items = Subject.objects.all()
        return Response(SubjectAdminSerializer(items, many=True, context={'request': request}).data)

    def post(self, request):
        serializer = SubjectAdminSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubjectDetailAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request, pk):
        item = get_object_or_404(Subject, pk=pk)
        return Response(SubjectAdminSerializer(item, context={'request': request}).data)

    def put(self, request, pk):
        item = get_object_or_404(Subject, pk=pk)
        serializer = SubjectAdminSerializer(item, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        return self.put(request, pk)

    def delete(self, request, pk):
        item = get_object_or_404(Subject, pk=pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
