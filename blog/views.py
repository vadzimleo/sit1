from collections.abc import Sequence
from typing import Any
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import (ListView,
DetailView, CreateView, 
UpdateView, DeleteView)
from django.core.paginator import Paginator
from django.urls import reverse_lazy
# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin 
#def home(request):
    #return HttpResponse('<doctype>...')

posts = [
    {"author": "Vadzim", 
     "date_posted": "21 of August 2023",
     "title": "Something about me", 
     "content": "I am a  mentally strong person" 
     }, 
         {"author": "Meteo", 
     "date_posted": "21 of August 2023",
     "title": "UV index ", 
     "content": "Today sun is much active : 6"}
]



def home(request):
    context = {"posts": posts and Post.objects.all()}
    return render(request, 'blog\home.html', context)

#def about(request):
    #return HttpResponse('<h1>Blog About in development<h1/>')

class Posts_view(ListView):
    model = Post
    # the same as: 
    #queryset = Post.objects.all()
#conventionally browser looks for template:
#<app>/<model>_<viewtype>.html
#blog/post_list.html
    template_name = 'blog/home.html'   #<app>/<model>_<viewtype>.html
#conventionally object_list is transfered to the template.Not posts as in function home
#so we need to create variable:
    context_object_name = 'posts' 
    #if not set: <model>_list or object_list
    def get_ordering(self) -> Sequence[str]:
        ordering = self.request.GET.get('ordering', '-date_posted')
        return ordering
    # may be: ordering = '-date_posted' 
    #ordering = ['-date_posted']
    #ordering = ['-id']
    #substitute for p = Paginator(posts_query_set, 2) in command line:
    paginate_by = 5
    #p.page(1) passed into template as page_obj

    #manually: http://127.0.0.1:8000/?page=2
    #? means that we want to put in a parameter.
    #Url query parameter of page=2 got passed into view. otherwis:e Page not found (404)
    #And view handles that &gives us the 2nd page

#default class:
class Post_view(DetailView):
    model = Post
    #expecting blog/post_detail.html    #<app>/<model>_<viewtype>.html
    #conventionally object is transfered to the template.Not post


def User_posts_view(request, name): 
    #category_posts = Categorie.objects.filter(name=cs.replace('-', ' ')) 
    #user_posts = Post.objects.filter(author=User.objects.get(username=name)).order_by('-date_posted')
    #!!! Huraaa
    #But error(if entered inexistent name) would be: 
    # DoesNotExist at /user/Vładisław/
    # User matching query does not exist.
    user = get_object_or_404(User, username=name)
    user_posts = Post.objects.filter(author=user).order_by('-date_posted')

    paginator = Paginator(user_posts, 5) # 5 users per page
    # We don't need to handle the case where the `page` parameter
    # is not an integer because our URL only accepts integers
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    #page_obj wouldn't transfer to the template - if not defined specifically 
    return render(request, 'blog/user_posts.html',{'user' : user,
    'name': name.title(), 'user_posts': user_posts,
    'page_obj' : page_obj, 'paginator' : paginator
    })
    #<h2> {{ name }} or {{ user_posts.first.author }}' blog posts </h2>    in the template
    #or {{ view.kwargs.username }} to get user name from url  if directed from class-based view


# def User_posts_pag(request, page=1):
#     user_posts = Post.objects.filter(author=User.objects.get(username='Vadzim'))
#     paginator = Paginator(user_posts, 5) # 5 users per page
    
#     # We don't need to handle the case where the `page` parameter
#     # is not an integer because our URL only accepts integers
#     try:
#         user_posts = paginator.page(page)
#     except EmptyPage:
#         # if we exceed the page limit we return the last page 
#         user_posts = paginator.page(paginator.num_pages)
            
#     return render(request, 'blog/user_posts.html', {'user_posts': user_posts})

# class User_posts_view(ListView):
#     model = Post
#     template_name = 'blog/user_posts.html'
#     context_object_name = 'posts'
#     ordering = ['-date_posted']
#     paginate_by = 5

#     def get_queryset(self) -> QuerySet[Any]: #Get the list of items for this view. 
#             #This must be an iterable and may be a queryset 
              # self is this view
#         user = get_object_or_404(User, username=self.kwargs.get('name'))
#             #user = User.objects.filter(username=name)
#             #keywords for User:
#             #.date_joined, email, first_name, groups, id, is_active, is_staff,
#             #is_superuser, last_login, last_name, logentry, password, post, 
#             #profile, user_permissions, username
              #<h2> {{ view.kwargs.username }}' blog posts </h2>    in the template
              #to get user name from url  if directed from class-based view
#         return Post.objects.filter(author=user).order_by('-date_posted')
    

def about(request):
    context = {"title": "Blog--About"}
    return render(request, 'blog\describe.html', context)

#not possible decorator @login_required, because this is a class
#only logged-in users can create post
class Create_post(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    #expected template:    <model>_form.html

    #IntegrityError at /post/new/
    #NOT NULL constraint failed: blog_post.author_id
    #we must tell that current user is creating a post. For this reason we override
    # form_valid method:
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.author = self.request.user #we set author of the form 
        #we are trying to submit equal to current logged-in user
        return super().form_valid(form)
    
    # instead of method get_absolute_url in models.Post
    #success_url = reverse_lazy('blog-home')

class Update_post(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    #template is mutual for Update & Create views: <model>_form.html 
    #So we don't need to create new one
    fields = ['title', 'content']
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        #form.instance.author = self.request.user
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    #or: {% if user.is_authenticated %}
  # {% if user.id == p.author.id %}


class Delete_post(UserPassesTestMixin, DeleteView):
    model = Post
    #blog/post_confirm_delete.html
    #ImproperlyConfigured at /post/11/delete/
    #No URL to redirect to. Provide a success_url.
    #success_url = reverse_lazy('blog-home')
    success_url = ('/')
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False