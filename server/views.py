from django.contrib.auth import get_user_model
from django.views.generic import TemplateView

User = get_user_model()


class HomePageView(TemplateView):
    template_name = 'chat/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Example: Add current user information to context
        context['user_count'] = User.objects.count()  # Number of users
        context['user'] = self.request.user  # Current logged-in user
        return context


class ChatGroupView(TemplateView):
    template_name = 'chat/chat-group.html'


class ChatDirectView(TemplateView):
    template_name = 'chat/chat-direct.html'


class ChatEmptyView(TemplateView):
    template_name = 'chat/chat-empty.html'


class ChatSignInView(TemplateView):
    template_name = 'chat/signin.html'


class ChatSignUpView(TemplateView):
    template_name = 'chat/signup.html'


class ChatPasswordResetView(TemplateView):
    template_name = 'chat/password-reset.html'


class ChatLockScreenView(TemplateView):
    template_name = 'chat/lockscreen.html'
