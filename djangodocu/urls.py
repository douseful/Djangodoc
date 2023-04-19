from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

import article.views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', article.views.article_list),
    path('comment/', include('comment.urls', namespace='comment')),
    path('article/', include('article.urls', namespace='article')),
    path('userprofile/', include('userprofile.urls', namespace='userprofile')),
]

urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
