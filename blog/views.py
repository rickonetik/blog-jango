from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import  login_required
from .models import Post
from .forms import PostForm, CommentForm

@login_required
def delete_post(request, id):
    queryset = Post.objects.filter(author=request.user)
    post = get_object_or_404(queryset, pk=id)
    context = {'post': post}    
    
    if request.method == 'GET':
        return render(request, 'blog/post_confirm_delete.html',context)
    elif request.method == 'POST':
        post.delete()
        messages.success(request,  'The post has been deleted successfully.')
        return redirect('posts')        

@login_required    
def edit_post(request, id):
    queryset = Post.objects.filter(author=request.user)
    post = get_object_or_404(queryset, pk=id)

    if request.method == 'GET':
        context = {'form': PostForm(instance=post), 'id': id}
        return render(request,'blog/post_form.html',context)
    
    elif request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'The post has been updated successfully.')
            return redirect('posts')
        else:
            messages.error(request, 'Please correct the following errors:')
            return render(request,'blog/post_form.html',{'form':form})

@login_required
def create_post(request):
    if request.method == 'GET':
        context = {'form': PostForm()}
        return render(request,'blog/post_form.html',context)
    elif request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.author = request.user
            user.save()
            messages.success(request, 'The post has been created successfully.')
            return redirect('posts')
        else:
            messages.error(request, 'Please correct the following errors:')
            return render(request,'blog/post_form.html',{'form':form})  
        
    
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user  # Используйте текущего пользователя для авторства комментария
            comment.save()
            return redirect('post-detail', pk=post.pk)  # Перенаправление на страницу поста после добавления комментария
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


def home(request):
    posts = Post.objects.all()
    context = {'posts': posts  }
    return render(request,'blog/home.html', context)   



def about(request):
    return render(request, 'blog/about.html')
