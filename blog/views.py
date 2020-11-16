from django.shortcuts import render, get_object_or_404
from .models import Post

#for class based views
from django.views.generic import (
	ListView, 
	DetailView,
	CreateView,
	UpdateView,
	DeleteView
)
from django.contrib.auth.mixins import (
	LoginRequiredMixin,
	UserPassesTestMixin
)
from django.contrib.auth.models import User


# Create your views here.

def home(request):
	# context is a dictionary
	context = {
		'posts': Post.objects.all()
	}
	return render(request,'blog/home.html', context)

class PostListView(ListView):
	model = Post
	# PostListView is looking for a template at 
	# <app>/<model>_<viewtype>.html
	# blog/post_list.html
	template_name = 'blog/home.html'
	context_object_name = 'posts' # list will loop over this variable context_object_name
	ordering = ['-date_posted'] 
	# date_posted -(old to new ordering of posts)
	# -date_posted -(new to old ordering of posts)
	paginate_by = 5


class UserPostListView(ListView):
	model = Post
	# PostListView is looking for a template at 
	# <app>/<model>_<viewtype>.html
	# blog/post_list.html
	template_name = 'blog/user_posts.html'
	context_object_name = 'posts' # list will loop over this variable context_object_name
	paginate_by = 5

	# we are overiding this fx so ordering should be done in the query
	# else if we write ordering = ['-date_posted'] above this fx
	# then that will also be overide
	def get_queryset(self):
		# if user/object exist in DB then get it, else get a 404 page
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Post.objects.filter(author = user).order_by('-date_posted')


class PostDetailView(DetailView):
	model = Post	


class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title','content']

	# we will overwrite the form_valid()
	def form_valid(self,form):
		form.instance.author = self.request.user
		return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title','content']

	# we will overwrite the form_valid()
	def form_valid(self,form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	# to check the current user is the author of the post
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = '/'

	# to check the current user is the author of the post
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False
 

def about(request):
	return render(request,'blog/about.html',{'title': 'About'})