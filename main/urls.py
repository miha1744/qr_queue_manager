from django.urls import path, include
from django.views.generic import RedirectView, TemplateView
from django.urls import reverse
from django.conf import settings




web_urls = [

]



api_urls = [
]


urlpatterns = web_urls + api_urls

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
