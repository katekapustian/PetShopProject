from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.core.paginator import Paginator
from .models import Post, Category, Tag, Comment
from .forms import CommentForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def blog(request):
    query = request.GET.get('q')
    category_slug = request.GET.get('category')
    tag_slug = request.GET.get('tag')

    posts = Post.objects.all().order_by('-published_date')

    if query:
        posts = posts.filter(title__icontains=query) | posts.filter(content__icontains=query)

    if category_slug:
        posts = posts.filter(category__slug=category_slug)

    if tag_slug:
        posts = posts.filter(tags__slug=tag_slug)

    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    tags = Tag.objects.all()
    recent_posts = Post.objects.order_by('-published_date')[:3]

    context = {
        'posts': page_obj,
        'page_obj': page_obj,
        'categories': categories,
        'tags': tags,
        'recent_posts': recent_posts,
    }
    return render(request, 'blog/blog-leftsidebar.html', context)


def blog_details(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    categories = Category.objects.all()
    tags = Tag.objects.all()
    recent_posts = Post.objects.order_by('-published_date')[:3]

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.author_name = request.user.first_name
                comment.author_email = request.user.email
                comment.save()
                messages.success(request, 'Your comment has been posted!')
                return redirect('blog:blog_details', post_id=post.id)
        else:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.save()
                messages.success(request, 'Your comment has been posted!')
                return redirect('blog:blog_details', post_id=post.id)
    else:
        form = CommentForm()

    context = {
        'post': post,
        'categories': categories,
        'tags': tags,
        'recent_posts': recent_posts,
        'form': form,
    }
    return render(request, 'blog/blog-details.html', context)


def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        if request.user.is_authenticated:
            author_name = request.user.first_name
            author_last_name = request.user.last_name
            author_email = request.user.email
            avatar_url = request.user.profile.avatar.url if request.user.profile.avatar else None
        else:
            author_name = request.POST.get('author_name')
            author_last_name = request.POST.get('author_last_name')
            author_email = request.POST.get('author_email')
            avatar_url = None

        content = request.POST.get('content')

        if not content:
            messages.error(request, "Comment content cannot be empty.")
            return redirect('blog:blog_details', post_id=post.id)

        if not author_name or not author_last_name or not author_email:
            messages.error(request, "Please provide your full name and email.")
            return redirect('blog:blog_details', post_id=post.id)

        full_author_name = f"{author_name} {author_last_name}"

        Comment.objects.create(
            post=post,
            author_name=full_author_name,
            author_email=author_email,
            content=content,
            avatar_url=avatar_url
        )

        messages.success(request, "Your comment has been posted.")
        return redirect('blog:blog_details', post_id=post.id)

    return redirect('blog:blog_details', post_id=post.id)


def blog_by_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    posts = Post.objects.filter(category=category)
    return render(request, 'blog/blog.html', {'posts': posts, 'selected_category': category})


def blog_by_tag(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags=tag)
    return render(request, 'blog/blog.html', {'posts': posts, 'selected_tag': tag})
