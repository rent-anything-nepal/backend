from django.urls import path
from utils.views import ApprovalView, PinView, ContentTypesView, BookingView

urlpatterns = [
    path("approve/", ApprovalView.as_view(), name="approve"),
    path("pin/", PinView.as_view(), name="pin"),
    path("booking/", BookingView.as_view(), name="booking"),
    path("content-types/", ContentTypesView.as_view(), name="content-types"),
]
