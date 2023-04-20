from django.shortcuts import render, redirect, HttpResponse, reverse
import markdown
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q

from .models import ArticlePost
from .forms import ArticlePostForm
from comment.models import Comment
from comment.forms import CommentForm
from django.views.generic import DetailView
from django.views.generic.edit import CreateView


class ArticleDetailView(DetailView):
    queryset = ArticlePost.objects.all()
    context_object_name = 'article'
    template_name = 'article/detail.html'

    def get_object(self, queryset=None):
        obj = super(ArticleDetailView, self).get_object()
        obj.total_views += 1
        obj.save(update_fields=['total_views'])
        return obj


class ArticleCreateView(CreateView):
    model = ArticlePost
    fields = '__all__'
    template_name = 'article/create_by_class_view.html'


def article_list(request):
    search = request.GET.get('search')
    order = request.GET.get('order')
    column = request.GET.get('column')
    tag = request.GET.get('tag')

    articles_list = ArticlePost.objects.all()

    if search:
        if order == 'total_views':
            articles_list = articles_list.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            ).order_by('-total_views')
        else:
            articles_list = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            )
    else:
        search = ''
        if order == 'total_views':
            articles_list = ArticlePost.objects.all().order_by('-total_views')
        else:
            articles_list = ArticlePost.objects.all()

    if column is not None and column.isdigit():
        articles_list = articles_list.filter(column=column)

    if tag and tag is not None:
        articles_list = articles_list.filter(tags__name__in=[tag])

    paginator = Paginator(articles_list, 4)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    context = {'articles': articles, 'order': order, 'search': search}
    return render(request, 'article/list.html', context)


def article_detail(request, id):
    article = ArticlePost.objects.get(id=id)
    comment_form = CommentForm()
    # filter could get multi objects, while get will only get one
    comments = Comment.objects.filter(article=id)

    # 浏览量+1
    article.total_views += 1
    article.save(update_fields=['total_views'])

    md = markdown.Markdown(
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',  # 代码高亮扩展
            'markdown.extensions.toc',
            'markdown.extensions.tables',
            'markdown.extensions.fenced_code',
        ]
    )

    article.body = md.convert(article.body)

    context = {'article': article, 'toc': md.toc, 'comments': comments,
               'comment_form': comment_form}
    return render(request, 'article/detail.html', context)


@login_required(login_url='/userprofile/login/')
# @login_required(login_url=reverse('userprofile:login'))
def article_create(request):
    if request.method == "POST":
        article_post_form = ArticlePostForm(request.POST, request.FILES)
        if article_post_form.is_valid():
            new_article = article_post_form.save(commit=False)
            new_article.author = User.objects.get(id=request.user.id)
            new_article.save()
            article_post_form.save_m2m()
            return redirect("article:article_list")
        else:
            return HttpResponse('填写有误，请重新填写。')
    else:
        article_post_form = ArticlePostForm()
        context = {'article_post_form': article_post_form}
        # return render(request, 'article/create.html', context)
        return render(request, 'article/create.html', context)


def article_delete(request, id):
    # if user != request.user:
    #

    article = ArticlePost.objects.get(id=id)
    if request.user.id != article.author_id:
        return HttpResponse('不是您写的文章,无法进行删除')

    article.delete()
    return redirect("article:article_list")


def article_update(request, id):
    article = ArticlePost.objects.get(id=id)
    if request.user.id != article.author_id:
        return HttpResponse('不是您写的文章,无法进行修改')

    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()
            return redirect("article:article_detail", id=id)
        else:
            return HttpResponse('输入不合法')
    else:
        article_post_form = ArticlePostForm()
        context = {
            'article': article,
            'article_post_form': article_post_form
        }
        return render(request, 'article/update.html', context)
