from annoying.decorators import ajax_request
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse, reverse_lazy
from Insta.models import Post, Like, InstaUser, UserConnection
from Insta.forms import CustomUserCreationForm

from django.contrib.auth.mixins import LoginRequiredMixin


# static content
class HelloWorld(TemplateView):
    template_name = 'test.html'

# contain an object_list
class PostsView(ListView):
    model = Post
    template_name = 'index.html'
    # change for name access in 'index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        current_user = self.request.user
        following = set()
        for conn in UserConnection.objects.filter(creator=current_user).select_related('following'):
            following.add(conn.following)
        return Post.objects.filter(author__in=following)

# contain an object
class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

class UserDetailView(LoginRequiredMixin, DetailView):
    model = InstaUser
    template_name = 'user_detail.html'
    # login_url = 'login'

# contain a form
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post_create.html'
    fields = '__all__'
    login_url = 'login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# contain a form
class PostUpdateView(UpdateView):
    model = Post
    template_name = 'post_update.html'
    fields = ['title']

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy("posts")

class SignUp(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy("login")

@ajax_request
def addLike(request):
    # get pk from AJAX request
    post_pk = request.POST.get('post_pk')
    # get the post object by id
    post = Post.objects.get(pk=post_pk)
    try:
        # create a like object
        like = Like(post=post, user=request.user)
        # it's possible that the like alreay exists
        like.save()
        result = 1
    except Exception as e:
        # get the like object by post, user (unique)
        like = Like.objects.get(post=post, user=request.user)
        like.delete()
        result = 0
    # return Json data
    return {
        'result': result,
        'post_pk': post_pk
    }