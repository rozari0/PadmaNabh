from django.urls import path
from PadmaNabh.views import courseview, moduleview

urlpatterns = [
    path("course/<str:slug>/", courseview, name="course"),
    path("course/<str:slug>/<str:module>", moduleview, name="module"),
]
