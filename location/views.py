from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from location.serializers import *


class ProvinceViewSet(ModelViewSet):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer
    search_fields = ("name", "nepali_name",)


class DistrictViewSet(ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    search_fields = ("name", "nepali_name",)
    filterset_fields = ("province",)


class MunicipalityViewSet(ModelViewSet):
    queryset = Municipality.objects.all()
    serializer_class = MunicipalitySerializer
    search_fields = ("name", "nepali_name",)
    filterset_fields = ("district", "district__province")


class WardViewSet(ModelViewSet):
    queryset = Ward.objects.all()
    serializer_class = WardSerializer
    search_fields = ("name", "nepali_name",)
    filterset_fields = ("municipality", "municipality__district", "municipality__district__province")


class BasePublicListViewSet(ReadOnlyModelViewSet):
    authentication_classes = []
    permission_classes = []
    search_fields = ("name", "nepali_name",)

    class Meta:
        abstract = True


class PublicProvinceViewSet(BasePublicListViewSet):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer


class PublicDistrictViewSet(BasePublicListViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer


class PublicMunicipalityViewSet(BasePublicListViewSet):
    queryset = Municipality.objects.all()
    serializer_class = MunicipalityAutoCompleteSerializer


class PublicWardViewSet(BasePublicListViewSet):
    queryset = Ward.objects.all()
    serializer_class = WardSerializer
