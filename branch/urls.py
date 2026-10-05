from django.urls import path

from .views import BranchView,BranchDetailView


urlpatterns = [
    path('branches/', BranchView.as_view()),
    path('branches/<int:id>/', BranchDetailView.as_view()),
]