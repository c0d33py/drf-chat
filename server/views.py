from django.contrib.auth import get_user_model
from django.views.generic import TemplateView

User = get_user_model()


class HomePageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Example: Add current user information to context
        context['user_count'] = User.objects.count()  # Number of users
        context['user'] = self.request.user  # Current logged-in user
        return context
