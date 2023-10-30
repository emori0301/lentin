from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, PermissionsMixin, Group, Permission,BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.urls import reverse
from stdimage.models import StdImageField 
from django.utils import timezone
from django.conf import settings

class UserManager(BaseUserManager):
    def _create_user(self, email, account_id, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, account_id=account_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, account_id, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(
            email=email,
            account_id=account_id,
            password=password,
            **extra_fields,
        )

    def create_superuser(self, email, account_id, password, **extra_fields):
        extra_fields['is_active'] = True
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        return self._create_user(
            email=email,
            account_id=account_id,
            password=password,
            **extra_fields,
        )

class User(AbstractBaseUser, PermissionsMixin):
    account_id = models.CharField(
        verbose_name=_("ユーザーID"),
        unique=True,
        max_length=10
    )
    first_name = models.CharField(
        verbose_name=_("ユーザー名"),
        max_length=150,
        null=True,
        blank=False
    )
    email = models.EmailField(
        verbose_name=_("メールアドレス"),
        unique=True
    )
    birth_date = models.DateField(
        verbose_name=_("誕生日"),
        blank=True,
        null=True
    )
    is_superuser = models.BooleanField(
        verbose_name=_("is_superuer"),
        default=False
    )
    is_staff = models.BooleanField(
        verbose_name=_('staff status'),
        default=False,
    )
    is_active = models.BooleanField(
        verbose_name=_('active'),
        default=True
    )
    created_at = models.DateTimeField(
        verbose_name=_("created_at"),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name=_("updated_at"),
        auto_now=True
    )

    objects = UserManager()

    USERNAME_FIELD = 'account_id' # ログイン時、ユーザー名の代わりにaccount_idを使用
    REQUIRED_FIELDS = ['email']  # スーパーユーザー作成時にemailも設定する

    def __str__(self):
        return self.account_id

class Article(models.Model):
    author = models.ForeignKey(User,on_delete = models.CASCADE)
    image = StdImageField('【料理画像】',upload_to='', blank=True, variations={
        'large': (450, 300),
        'thumbnail': (100, 100, True),
        'medium': (300, 200),
    })
    title = models.CharField('【タイトル】', max_length = 200)
    description = models.TextField('【サムネイル用の説明（50文字まで）】', max_length=50, null=True)
    ingredients = models.TextField('【材料】', max_length=1000, null=True)
    content = models.TextField('【調理手順】', max_length=1000, null=True)
    created_at = models.DateTimeField('作成日', auto_now_add=True)
    updated_at = models.DateTimeField('更新日', auto_now=True)
 
    def __str__(self):
        return self.content
 
    def get_absolute_url(self):
        return reverse('app:detail', kwargs={'pk': self.pk})
    
    def average_rating(self):
        ratings = Rating.objects.filter(article=self)
        return ratings.aggregate(models.Avg('stars'))['stars__avg']

# 星評価モデル
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    stars = models.IntegerField()

# コメントモデル
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, default=1)
    content = models.TextField('内容')
    created_at = models.DateTimeField(auto_now_add=True)



