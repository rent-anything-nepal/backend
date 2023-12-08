from django.contrib.contenttypes.models import ContentType
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from util.models import Media
from util.serializer import MediaSerializer, ContentTypeSerializer


class ContentTypesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content_types = ContentType.objects.all()
        serializer = ContentTypeSerializer(content_types, many=True)
        return Response(serializer.data)


class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
