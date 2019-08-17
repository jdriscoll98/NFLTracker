from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView

# Application Views


# Home Page
class HomePageView(TemplateView):
    template_name = "website/home_page.html"


# Profile Page
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "website/profile.html"
