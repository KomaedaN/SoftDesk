from django.contrib import admin
from django.urls import path, include
from rest_framework_nested import routers

from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from authentication.views import SignupViewset
from projects.views import ProjectViewset, ContributorViewset

router = routers.SimpleRouter()

router.register('projects', ProjectViewset, basename='projects')
router.register('users', ContributorViewset, basename='users')
router.register('signup', SignupViewset, basename='signup')


project_router = routers.NestedSimpleRouter(router, r'projects', lookup='project')
project_router.register(r'users', ContributorViewset, basename='user')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('rest_framework.urls')),
    path('token/', TokenObtainPairView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
    path('', include(project_router.urls)),
]
