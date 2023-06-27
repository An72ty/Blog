from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import BlogPost, Comment
from .forms import PostForm, CommentForm
from django.http import Http404


def index(request):
    """Домашняя страница приложения Blog."""
    if request.method == 'POST':
        BlogPost.objects.filter(id=request.POST.get('post_id')).delete()

    posts = BlogPost.objects.order_by('-date_added')
    context = {'posts': posts, 'user': request.user}
    return render(request, 'blogs/index.html', context)


@login_required
def new_post(request):
    """Определяет новую запись."""
    if request.method != 'POST':
        # Данные не отправлялись; создается пустая форма.
        form = PostForm()
    else:
        # Отправлены данные POST; обработать данные.
        form = PostForm(data=request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.owner = request.user
            new_post.save()
            return redirect('blogs:view_post', new_post.id)
    
    # Вывести пустую или недействительную форму.
    context = {'form': form}
    return render(request, 'blogs/new_post.html', context)


@login_required
def edit_post(request, post_id):
    """Редактирование записи."""
    post = BlogPost.objects.get(id=post_id)
    check_post_owner(request, post)
    
    if request.method != 'POST':
        # Исходный запрос; форма заполняется данными текущей записи.
        form = PostForm(instance=post)
    else:
        # Отправка данных POST; обработать данные.
        form = PostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogs:view_post', post.id)
    
    context = {'post': post, 'form': form}
    return render(request, 'blogs/edit_post.html', context)


def check_post_owner(request, post: BlogPost):
    """Проверка того, что запись принадлежит текущему пользователю."""
    if post.owner != request.user:
        raise Http404
    

def view_post(request, post_id):
    """Просмотр записи."""
    post = BlogPost.objects.get(id=post_id)
    form = CommentForm()    # Это строка нужна была чтобы передать форму в render()
    if request.method != 'POST':
        # Данные не отправлялись.
        pass
    else:
        # Данные для создания нового комментария были переданы.
        form = CommentForm(data=request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.owner = request.user
            new_comment.post = post
            new_comment.save()
            return redirect('blogs:view_post', post.id)

    comments = Comment.objects.filter(post=post).order_by('-date_added')
    context = {'post': post, 'comments': comments}
    return render(request, 'blogs/view_post.html', context)
    
    
