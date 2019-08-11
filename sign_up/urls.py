from django.conf.urls import url
from django.views.generic import TemplateView, RedirectView
from sign_up.views import *

urlpatterns = [
  # url(r'^sign-up/', TemplateView.as_view(template_name="sign_up/sign_up.html"), name='sign_up'),
]
