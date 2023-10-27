from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Article, Comment, User
from django import forms

# 新規登録フォーム
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "account_id",
            "email",
            "first_name",
            "birth_date",
        )

# ログインフォーム
class LoginFrom(AuthenticationForm):
    class Meta:
        model = User

# 記事作成フォーム
class ArticleCreateForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            'title',
            'image',
            'description', 
            'ingredients',
            'content',
            'author',
        ]

# コメント投稿のフォーム
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'author',
            'content',
        ]