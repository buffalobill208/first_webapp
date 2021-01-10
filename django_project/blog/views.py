# python first
# django second
# your apps
# local directory
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.core.mail import send_mail
from django_project.settings import EMAIL_HOST_USER
from .models import Post    # local directory


# Create your views here.
# function-based view
def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


# class-based view
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'    # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'    # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    # method
    def get_queryset(self):
        # get object from the User model (imported above).  The user we want to get is the user w/ the username equal to from the url.  If that user doesn't exist, it will just return a 404 message.
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        # limit the post query
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        subject = 'A user has created a new post!'
        message = 'http: // 127.0.0.1: 8000/'
        recepient = EMAIL_HOST_USER
        # Next is to add a link of the new post in the email message
        send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently=False)
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# Function to prevent other users from updating posts of other users
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
# Function to prevent other users from deleting posts of other users

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
