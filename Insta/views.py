from django.views.generic import TemplateView, ListView, DetailView

from Insta.models import Post

class HelloWorld(TemplateView):
    template_name = 'test.html'

class PostsView(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'   # change for name access in 'index.html'

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'