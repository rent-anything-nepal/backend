from django.contrib.contenttypes.models import ContentType
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from media.models import Media
from media.serializer import MediaSerializer, ContentTypeSerializer
from utils.abstracts import BaseViewSet


class ContentTypesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content_types = ContentType.objects.all()
        serializer = ContentTypeSerializer(content_types, many=True)
        return Response(serializer.data)


class MediaViewSet(BaseViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
