from django.urls import path
from . import views

# - `{% url '...' %}`是Django规定的模板解耦语法，用它可以根据我们在`urls.py`中设置的名字，反向解析到对应的url中去。
#
# 关于其中的`'article:article_list'`的解释：
#
# - 前面的`article`是在项目根目录的`urls.py`中定义的app的名称
# - 后面的`article_list`是在app中的`urls.py`中定义的具体的路由地址
#
# 通过这样的方法就将链接跳转的指向给配置好了，只要对应url的名称不变，url本身无论怎么变化，Django都可以解析到正确的地址，很灵活。

app_name = 'article'

urlpatterns = [
    path('article-list/', views.article_list, name='article_list'),

    path('detail-view/<int:pk>/', views.ArticleDetailView.as_view(), name='detail_view'),
    path('create-view/', views.ArticleCreateView.as_view(), name='create_view'),


    path('article-create/', views.article_create, name='article_create'),
    path('article-delete/<int:id>/', views.article_delete, name='article_delete'),
    path('article-update/<int:id>/', views.article_update, name='article_update'),
    path('article-detail/<int:id>/', views.article_detail, name='article_detail')
]
