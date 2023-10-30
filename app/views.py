from django.views.generic import View
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SignUpForm, LoginFrom, ArticleCreateForm, CommentForm
from django.http import HttpResponseForbidden
from .forms import ArticleCreateForm
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from .models import Article, Comment, Rating
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
#==========================================
filter
# ようこそページへの遷移
class IndexView(TemplateView):
    template_name = "app/hello.html"

#==========================================

# ホームへの遷移
class HomeView(TemplateView):
    template_name = "app/home.html"

#==========================================

# 新規登録ページへの遷移
class SignupView(CreateView):
    form_class = SignUpForm
    template_name = "app/signup.html"
    success_url = reverse_lazy("app:hello")

    def form_valid(self, form):
        response = super().form_valid(form)
        account_id = form.cleaned_data.get("account_id")
        password = form.cleaned_data.get("password1")
        user = authenticate(account_id=account_id, password=password)
        login(self.request, user)
        return response
    
#==========================================

# ログインページへの遷移
class LoginView(BaseLoginView):
    form_class = LoginFrom
    template_name = "app/login.html"

#==========================================

# ログアウトページへの遷移
class LogoutView(LoginRequiredMixin, BaseLogoutView):
    success_url = reverse_lazy("app:hello")

#==========================================


# ===================================================================

# ホームの記事一覧ページ
class HomeView(generic.ListView):
    model = Article
    paginate_by = 6

# ===================================================================

class DetailView(generic.DetailView):
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # テンプレートにコメント作成フォームを渡す
        context['comment_form'] = CommentForm
 
        return context

# ===================================================================

def create_comment(request, article_id):
    article = Article.objects.get(pk=article_id)
    # article = get_object_or_404(Article, pk=article_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.article = article
            comment.save()
            return redirect('app:detail', pk=article.pk)
    else:
        form = CommentForm()

    comments = Comment.objects.filter(article=article)

    return render(request, 'article_detail.html', {'article': article, 'form': form, 'comments': comments})

# ===================================================================

def home(request):
    return render(request,'app/home.html')

# ===================================================================

class ArticleCreateView(generic.CreateView):
    model = Article
    form_class = ArticleCreateForm
    template_name = 'app/create_form.html'
    # fields = ['title','description','ingredients','content','author']
    success_url = reverse_lazy('app:home')

    def form_valid(self, form):
       """投稿ユーザーをリクエストユーザーと紐付け"""
       form.instance.user = self.request.user
       return super().form_valid(form)

# ===================================================================

class ArticleList(generic.ListView):
    template_name = 'app/article_list.html'
    model = Article
    paginate_by = 6

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # {'pk':{'count':ポストに対するイイネ数,'is_user_liked_for_article':bool},}という辞書を追加していく
    #     d = {}
    #     for article in self.object_list:
    #         # articleに対するイイね数
    #         like_for_article_count = article.likeforarticle_set.count()
    #         # ログイン中のユーザーがイイねしているかどうか
    #         is_user_liked_for_article = False
    #         if not self.request.user.is_anonymous:
    #             if article.likeforarticle_set.filter(user=self.request.user).exists():
    #                 is_user_liked_for_article = True

    #         d[article.pk] = {'count': like_for_article_count, 'is_user_liked_for_article': is_user_liked_for_article}
    #     context['article_like_data'] = d
    #     return context

# ===================================================================

class ArticleDetail(generic.DetailView):
    template_name = 'app/article_detail.html'
    model = Article

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     like_for_article_count = self.object.likeforarticle_set.count()
    #     # ポストに対するイイね数
    #     context['like_for_article_count'] = like_for_article_count
    #     # ログイン中のユーザーがイイねしているかどうか
    #     is_user_liked_for_article = False
    #     if not self.request.user.is_anonymous:
    #         if self.object.likeforarticle_set.filter(user=self.request.user).exists():
    #             is_user_liked_for_article = True
    #     context['is_user_liked_for_article'] = is_user_liked_for_article

    #     # {'pk':{'count':コメントに対するイイネ数,'is_user_like_for_comment':bool},}という辞書を追加していく
    #     d = {}
    #     for comment in self.object.comment_set.all():
    #         like_for_comment_count = comment.likeforcomment_set.count()
    #         is_user_liked_for_comment = False
    #         if not self.request.user.is_anonymous:
    #             if comment.likeforcomment_set.filter(user=self.request.user).exists():
    #                 is_user_liked_for_comment = True
    #         d[comment.pk] = {'count': like_for_comment_count, 'is_user_liked_for_comment': is_user_liked_for_comment}

    #     context['comment_like_data'] = d

    #     return context
    

# ===================================================================

# def like_for_article(request):
#     article_pk = request.POST.get('article_pk')
#     context = {
#         'user': f'{request.user.first_name}',
#     }
#     article = get_object_or_404(Article, pk=article_pk)
#     like = LikeForArticle.objects.filter(target=article, user=request.user)

#     if like.exists():
#         like.delete()
#         context['method'] = 'delete'
#     else:
#         like.create(target=article, user=request.user)
#         context['method'] = 'create'

#     context['like_for_article_count'] = article.likeforarticle_set.count()

#     return JsonResponse(context)

# # ===================================================================

# def like_for_comment(request):
#     comment_pk = request.POST.get('comment_pk')
#     context = {
#         'user': f'{request.user.first_name}',
#     }
#     comment = get_object_or_404(Comment, pk=comment_pk)
#     like = LikeForComment.objects.filter(target=comment, user=request.user)
#     if like.exists():
#         like.delete()
#         context['method'] = 'delete'
#     else:
#         like.create(target=comment, user=request.user)
#         context['method'] = 'create'

#     context['like_for_comment_count'] = comment.likeforcomment_set.count()

#     return JsonResponse(context)

# ==== 検索機能 =====================================================

def search_articles(request):
    keyword = request.GET.get('keyword')
    if keyword:
        articles = Article.objects.filter(title__icontains=keyword)
    else:
        articles = Article.objects.all()

    return render(request, 'app/search_results.html', {'articles': articles})

# ==== ランキング機能 =====================================================

# ===================================================================

# マイページへの遷移
@login_required
def my_page(request):
    user = request.user
    user_articles = Article.objects.filter(author=user)
    context = {
        'user': user,
        'user_articles': user_articles,
    }
    return render(request, 'app/my_page.html', context)

#==========================================

# 記事編集ページへの遷移
def edit_article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if request.user == article.author: 
        if request.method == 'POST':
            form = ArticleCreateForm(request.POST, instance=article)
            if form.is_valid():
                form.save()
                return redirect('app:detail', pk=article.pk)
        else:
            form = ArticleCreateForm(instance=article)
        return render(request, 'app/edit_article.html', {'form': form,'article': article})
    else:
        return HttpResponseForbidden("このページにアクセスする権限がありません。")
    
#==========================================

# 記事削除ページへの遷移
def delete_article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    # 認可ロジック: ユーザーが記事の作成者であることを確認
    if request.user == article.author:
        if request.method == 'POST':
            article_id = request.POST.get('article_id')
            article.delete()
            return redirect('app:home')
            
        return render(request, 'app/delete_article.html', {'article': article})

    else:
        return HttpResponseForbidden("このページにアクセスする権限がありません。")
    
#==========================================

@login_required
def rate_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    stars = request.POST.get('rating')

    # ユーザーが既に記事を評価したかどうかを確認
    if Rating.objects.filter(user=request.user, article=article).exists():
        # 既に評価している場合は、エラーメッセージを表示
        messages.error(request, 'すでにこの記事へは評価済みです。')
    else:
        # まだ評価していない場合は、新しい評価を作成
        Rating.objects.create(user=request.user, article=article, stars=stars)

    # 評価の存在を確認
    has_rated = Rating.objects.filter(user=request.user, article=article).exists()

    # return render(request, 'app/detail.html')
    return render(request, 'app/article_detail.html', {'article': article, 'has_rated': has_rated})

