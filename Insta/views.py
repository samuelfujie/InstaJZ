from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse, reverse_lazy
from Insta.models import Post

# static content
class HelloWorld(TemplateView):
    template_name = 'test.html'

# contain an object_list
class PostsView(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'   # change for name access in 'index.html'

# contain an object
class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

# contain a form
class PostCreateView(CreateView):
    model = Post
    template_name = 'post_create.html'
    fields = '__all__'

# contain a form
class PostUpdateView(UpdateView):
    model = Post
    template_name = 'post_update.html'
    fields = ['title']

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy("posts")