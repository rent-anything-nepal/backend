from rest_framework.routers import DefaultRouter
from location.views import ProvinceViewSet, DistrictViewSet, MunicipalityViewSet, WardViewSet


router = DefaultRouter()

router.register(r"province", ProvinceViewSet, basename="province")
router.register(r"district", DistrictViewSet, basename="district")
router.register(r"municipality", MunicipalityViewSet, basename="municipality")
router.register(r"ward", WardViewSet, basename="ward")
router.register(r"public/province", ProvinceViewSet, basename="public_province")
router.register(r"public/district", DistrictViewSet, basename="public_district")
router.register(r"public/municipality", MunicipalityViewSet, basename="public_municipality")
router.register(r"public/ward", WardViewSet, basename="public_ward")
