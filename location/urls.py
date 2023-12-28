from rest_framework.routers import DefaultRouter
from location.views import ProvinceViewSet, DistrictViewSet, MunicipalityViewSet, WardViewSet, \
    PublicProvinceViewSet, PublicDistrictViewSet, PublicMunicipalityViewSet, PublicWardViewSet


router = DefaultRouter()

router.register(r"province", ProvinceViewSet, basename="province")
router.register(r"district", DistrictViewSet, basename="district")
router.register(r"municipality", MunicipalityViewSet, basename="municipality")
router.register(r"ward", WardViewSet, basename="ward")
router.register(r"public/province", PublicProvinceViewSet, basename="public_province")
router.register(r"public/district", PublicDistrictViewSet, basename="public_district")
router.register(r"public/municipality", PublicMunicipalityViewSet, basename="public_municipality")
router.register(r"public/ward", PublicWardViewSet, basename="public_ward")

urlpatterns = router.urls
