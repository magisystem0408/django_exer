from django.contrib import admin
from django.urls import path

from . import views

# 重複しないように解決
app_name = 'polls'
urlpatterns = [

    path('admin/', admin.site.urls),

    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
