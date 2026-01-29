from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.shortcuts import get_object_or_404
from .models import GalleryCategory, GalleryImage

from .serializers import (
    GalleryCategoryPublicSerializer, GalleryImagePublicSerializer,
    GalleryCategoryAdminSerializer, GalleryImageAdminSerializer
)

# ==================== PUBLIC VIEWS ====================

class GalleryPublicView(APIView):
    """
    GET /api/public/gallery/
    Query params: limit, category (slug)
    """
    permission_classes = [AllowAny]

    def get(self, request):
        limit = int(request.query_params.get('limit', 20))
        category_slug = request.query_params.get('category')
        
        images = GalleryImage.objects.all().order_by('-created_at')
        
        if category_slug:
            images = images.filter(category__slug=category_slug)
            
        images = images[:limit]
        categories = GalleryCategory.objects.all()
        
        data = {
            'images': GalleryImagePublicSerializer(images, many=True, context={'request': request}).data,
            'categories': GalleryCategoryPublicSerializer(categories, many=True, context={'request': request}).data
        }
        return Response(data)

class GalleryCategoryDetailView(APIView):
    """
    GET /api/public/gallery/category/<slug>/
    """
    permission_classes = [AllowAny]

    def get(self, request, slug):
        category = get_object_or_404(GalleryCategory, slug=slug)
        images = GalleryImage.objects.filter(category=category).order_by('-created_at')
        
        data = {
            'category': GalleryCategoryPublicSerializer(category, context={'request': request}).data,
            'images': GalleryImagePublicSerializer(images, many=True, context={'request': request}).data
        }
        return Response(data)

# ==================== ADMIN VIEWS ====================

class GalleryAdminView(APIView):
    """
    GET /api/admin/gallery/
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        categories = GalleryCategory.objects.all()
        images = GalleryImage.objects.all().order_by('-created_at')
        
        return Response({
            'categories': GalleryCategoryAdminSerializer(categories, many=True, context={'request': request}).data,
            'images': GalleryImageAdminSerializer(images, many=True, context={'request': request}).data
        })

class GalleryCategoryAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        categories = GalleryCategory.objects.all()
        return Response(GalleryCategoryAdminSerializer(categories, many=True, context={'request': request}).data)

    def post(self, request):
        serializer = GalleryCategoryAdminSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GalleryCategoryDetailAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def put(self, request, pk):
        category = get_object_or_404(GalleryCategory, pk=pk)
        serializer = GalleryCategoryAdminSerializer(category, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        return self.put(request, pk)

    def delete(self, request, pk):
        category = get_object_or_404(GalleryCategory, pk=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class GalleryImageAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get(self, request):
        images = GalleryImage.objects.all().order_by('-created_at')
        return Response(GalleryImageAdminSerializer(images, many=True, context={'request': request}).data)

    def post(self, request):
        serializer = GalleryImageAdminSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GalleryImageDetailAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def put(self, request, pk):
        image = get_object_or_404(GalleryImage, pk=pk)
        serializer = GalleryImageAdminSerializer(image, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        return self.put(request, pk)

    def delete(self, request, pk):
        image = get_object_or_404(GalleryImage, pk=pk)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
