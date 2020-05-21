from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User, AnonymousUser
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView
from .models import Post
from .forms import CommentForm


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'my_blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'my_blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'my_blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class SciencePostListView(ListView):
    model = Post
    template_name = 'my_blog/post_science.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(label='ciencia').order_by('-date_posted')


class FictionPostListView(ListView):
    model = Post
    template_name = 'my_blog/post_fiction.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(label='ficción').order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostLikeToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs.get("pk"))
        user = self.request.user
        url_ = post.get_absolute_url()
        if user.id != AnonymousUser.id:
            if user in post.likes.all():
                post.likes.remove(user)
            else:
                post.likes.add(user)
        return url_


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'label', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'label', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'my_blog/about.html', {'title': 'About'})


def PostCommentView(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.name = request.user
            comment.save()
            return redirect('post-detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'my_blog/post_comment.html', {'form': form})
