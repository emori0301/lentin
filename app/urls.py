from django.urls import path
# from app import views
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

app_name = "app"

# accounts/ の後のURL
urlpatterns = [
    path("", views.IndexView.as_view(), name="hello"), # ログイン選択ページ
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', views.SignupView.as_view(), name="signup"), # 新規登録ページ
    path('login/', views.LoginView.as_view(), name="login"), # ログインページ
    path('home/', views.HomeView.as_view(), name='home'), #ホーム

    path('logout/', views.LogoutView.as_view(), name="logout"), # ログアウトページ
    path('my_page/', views.my_page, name='my_page'), # マイページ
    path('<int:article_id>/edit_article/', views.edit_article, name='edit_article'), # 記事編集ページ
    path('<int:article_id>/delete_article/', views.delete_article, name='delete_article'), # 記事削除ページ

    path('article/<int:pk>/', views.DetailView.as_view(), name='detail'), # 記事詳細ページ
    path('article/<int:article_id>/create_comment/', views.create_comment, name='create_comment'), # コメント投稿ページ
    path('create_form/', views.ArticleCreateView.as_view(), name='create_form'), # 記事投稿ページ
    path('like_for_article/', views.like_for_article, name='like_for_article'), # 記事のいいねページ
    path('like_for_comment/', views.like_for_comment, name='like_for_comment'), # コメントのいいねページ
    path('search/', views.search_articles, name='search_articles'), # 記事検索ページ
    path('rate_article/<int:pk>/', views.rate_article, name='rate_article'),
    # path('article_ranking/', views.article_ranking, name='article_ranking'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)