from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .models import Notice, Event
from .serializers import (
    NoticePublicSerializer, EventPublicSerializer,
    NoticeAdminSerializer, EventAdminSerializer
)

# --- Public Views ---

class NoticesPublicView(APIView):
    """
    GET /api/public/notices/
    """
    permission_classes = [AllowAny]

    def get(self, request):
        notices = Notice.objects.filter(status=Notice.Status.PUBLISHED).order_by('-is_important', '-publish_date')
        return Response(NoticePublicSerializer(notices, many=True).data)

class NoticeDetailPublicView(APIView):
    """
    GET /api/public/notices/<slug>/
    """
    permission_classes = [AllowAny]

    def get(self, request, slug):
        notice = get_object_or_404(Notice, slug=slug, status=Notice.Status.PUBLISHED)
        return Response(NoticePublicSerializer(notice).data)

class EventsPublicView(APIView):
    """
    GET /api/public/events/
    """
    permission_classes = [AllowAny]

    def get(self, request):
        events = Event.objects.filter(status=Event.Status.PUBLISHED).order_by('-event_date')
        return Response(EventPublicSerializer(events, many=True).data)

class EventDetailPublicView(APIView):
    """
    GET /api/public/events/<slug>/
    """
    permission_classes = [AllowAny]

    def get(self, request, slug):
        event = get_object_or_404(Event, slug=slug, status=Event.Status.PUBLISHED)
        return Response(EventPublicSerializer(event).data)

# --- Admin Views ---
# (Skipping full admin CRUD for brevity unless requested, but scaffolding simple ones)

class NoticeAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get(self, request):
        notices = Notice.objects.all()
        return Response(NoticeAdminSerializer(notices, many=True, context={'request': request}).data)
        
    def post(self, request):
        serializer = NoticeAdminSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NoticeDetailAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request, pk):
        notice = get_object_or_404(Notice, pk=pk)
        return Response(NoticeAdminSerializer(notice, context={'request': request}).data)

    def put(self, request, pk):
        notice = get_object_or_404(Notice, pk=pk)
        serializer = NoticeAdminSerializer(notice, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        return self.put(request, pk)

    def delete(self, request, pk):
        notice = get_object_or_404(Notice, pk=pk)
        notice.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class EventAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request):
        events = Event.objects.all()
        return Response(EventAdminSerializer(events, many=True, context={'request': request}).data)

    def post(self, request):
        serializer = EventAdminSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EventDetailAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        return Response(EventAdminSerializer(event, context={'request': request}).data)

    def put(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        serializer = EventAdminSerializer(event, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        return self.put(request, pk)

    def delete(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
