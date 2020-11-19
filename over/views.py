from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Post, PostView, Comment
from .forms import PostForm, CommentForm

def home(request):

  post_list = Post.objects.all().order_by('-date_created')

  query = request.GET.get('page')
  paginator = Paginator(post_list, 4)

  try:
    posts = paginator.page(query)
  except PageNotAnInteger:
    posts = paginator.page(1)
  except EmptyPage:
    posts = paginator.page(paginator.num_pages)  
    

  context = {'posts':posts}
  return render(request, 'over/home.html', context)

def post_detail(request, pk):

  post = get_object_or_404(Post, pk=pk)

  post_comments = Comment.objects.filter(post=post, reply=None) 

  if request.method == 'POST':

    comment_form = CommentForm(request.POST)

    if comment_form.is_valid():

      content = comment_form.cleaned_data.get('content')
      reply_id = request.POST.get('reply_id')

      comment_reply = None
      if reply_id:
        comment_reply = Comment.objects.get(id=reply_id)
        
      commented = Comment.objects.create(user=request.user, post=post, content=content, reply=comment_reply)
      commented.save()
      return redirect(post.get_absolute_url())

  else:
    comment_form = CommentForm()    

  PostView.objects.get_or_create(user=request.user, post=post)
  
  context = {'post': post, 'post_comments': post_comments, 'comment_form':comment_form}
  return render(request, 'over/post_detail.html', context)

def create_post(request):

  if request.method == 'POST':
    postform = PostForm(request.POST, request.FILES)

    if postform.is_valid():
      post = postform.save(commit=False)
      post.author = request.user
      print(post)
      post.save()
      return redirect('home')

  else:
    postform = PostForm()   

  context = {'form': postform}
  return render(request, 'over/createPost.html', context)

def post_update(request, pk):
  post = get_object_or_404(Post, id=pk)

  if request.method == 'POST':
    form = PostForm(request.POST, request.FILES, instance=post)
    if form.is_valid():
      form.save()
      return redirect(post.get_absolute_url())

  else:
    form = PostForm(instance=post)    

  context = {'form': form}
  return render(request, 'over/createPost.html', context)  

def post_delete(request, pk):
  todo = get_object_or_404(Post, id=pk)
  todo.delete()

  return redirect('home')

def featured(request):

  post = Post.objects.get(featured=True)

  context = {'post': post}
  return render(request, 'over/featured.html', context)   