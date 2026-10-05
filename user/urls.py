from rest_framework.routers import DefaultRouter
from django.urls import path
from user.views import JWTLoginView, UserViewSet

router = DefaultRouter()

router.register(
    'users',
    UserViewSet,
    basename='users'
)

urlpatterns = [
    path('login/', JWTLoginView.as_view(), name='login'),
    *router.urls,
]
