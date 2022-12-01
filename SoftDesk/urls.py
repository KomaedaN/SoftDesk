from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from authentication.views import SignupViewset
from projects.views import ProjectViewset

router = routers.SimpleRouter()

""" Authentication route """
router.register('signup', SignupViewset, basename='signup')

""" Project route """
router.register('projects', ProjectViewset, basename='projects')

""" Contributors route """

""" Issue route """

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('rest_framework.urls')),
    path('token/', TokenObtainPairView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
