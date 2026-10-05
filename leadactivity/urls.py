from rest_framework.routers import DefaultRouter
from .views import LeadActivityViewSet
router = DefaultRouter()

router.register('leadactivities',LeadActivityViewSet,basename="leadactivities")

urlpatterns = router.urls