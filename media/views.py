from media.models import Media
from media.serializer import MediaSerializer
from utils.abstracts import BaseViewSet


class MediaViewSet(BaseViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
