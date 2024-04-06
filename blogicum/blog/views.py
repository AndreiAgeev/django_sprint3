from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from blog.models import Post, Category
import datetime


def index(request):
    template_name = 'blog/index.html'
    post_list = Post.objects.select_related(
        'location', 'author', 'category'
    ).filter(
        pub_date__lte=datetime.datetime.now(),
        is_published=True,
        category__is_published=True
    )[0:5]
    context = {'post_list': post_list}
    return render(request, template_name, context)


def post_detail(request, post_id):
    template_name = 'blog/detail.html'
    post = get_object_or_404(
        Post.objects.exclude(
            Q(pub_date__gte=datetime.datetime.now())
            | Q(is_published=False)
            | Q(category__is_published=False)
        ),
        pk=post_id
    )
    context = {'post': post}
    return render(request, template_name, context)


def category_posts(request, category_slug):
    template_name = 'blog/category.html'
    category_data = get_object_or_404(
        Category.objects.filter(
            is_published=True
        ),
        slug=category_slug)
    post_list = Post.objects.select_related(
        'location', 'author', 'category'
    ).filter(
        category__slug=category_slug,
        is_published=True,
        pub_date__lte=datetime.datetime.now()
    )
    context = {
        'category': category_data,
        'post_list': post_list
    }
    return render(request, template_name, context)
