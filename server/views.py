from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

User = get_user_model()


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'chat/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_count'] = User.objects.count()
        context['user'] = self.request.user
        return context


class ChatGroupView(LoginRequiredMixin, TemplateView):
    template_name = 'chat/chat-group.html'


class ChatDirectView(LoginRequiredMixin, TemplateView):
    template_name = 'chat/chat-direct.html'


class ChatEmptyView(LoginRequiredMixin, TemplateView):
    template_name = 'chat/chat-empty.html'


class ChatSignInView(TemplateView):
    template_name = 'auth/signin.html'


class ChatSignUpView(TemplateView):
    template_name = 'auth/signup.html'


class ChatPasswordResetView(TemplateView):
    template_name = 'auth/password-reset.html'


class ChatLockScreenView(TemplateView):
    template_name = 'auth/lockscreen.html'
