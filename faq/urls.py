from django.urls import path
from .views import FAQListView

urlpatterns = [
    path('api/v1/faqs/', FAQListView.as_view(), name='faq-list-v1'),
]
