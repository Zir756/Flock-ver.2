from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

# postクラス(Djangoのモデルとして機能する)
class Post(models.Model):
    
    # モデルのフィールドを定義する  
    
    # 作者：関係データベースにおいてデータの整合性を保つための制約  
    # 多対一のリレーションシップ。2つの位置引数を必要とします: モデルが関連するクラスと on_delete オプション
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # タイトル：文字列の為のフィールド(文字列200字を設定　※最大255字)  
    title = models.CharField(max_length=200)
    # テキスト：CharFieldより長い文字列を記載するためのフィールド(文字数の設定は不要)  
    text = models.TextField()
    # 作成時：日付と時間のためのフィールド(作成時の時刻を既定としている)
    created_date = models.DateTimeField(default=timezone.now)
    # 公開日：日付と時間のためのフィールド(フォーム入力時に入力が必須かどうか,データベースのNot Null制約(空の値を入れてはいけない))
    published_date = models.DateTimeField(blank=True, null=True)

    # postを公開するメソッド
    def publish(self):
        # postのインスタンスが'published_date'を呼び出す。  
        self.published_date = timezone.now()
        # Djangoのモデルインスタンスのメソッド。データベースにそのインスタンスの変更を保存する。  
        self.save()

    # postオブジェクトを文字列として表現するために使われる。
    def __str__(self):
        # メソッド内で'self.title'を返すことで、タイトルの中身を文字列として返す。  
        return self.title
        
# objectsマネージャーを追加する。  
    objects = models.Manager()
    
# commentクラス(Djangoのモデルとして機能する)
class Comment(models.Model):
    
    # モデルのフィールドを定義する
    
    # 投稿：関係データベースにおいてデータの整合性を保つための制約  
    # 多対一のリレーションシップ。2つの位置引数を必要とします: モデルが関連するクラスと on_delete オプション
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    # 作者：文字列の為のフィールド(文字列200字を設定　※最大255字)   
    author = models.CharField(max_length=200)
    # テキスト：CharFieldより長い文字列を記載するためのフィールド(文字数の設定は不要)  
    text = models.TextField()
    # 作成時：日付と時間のためのフィールド(作成時の時刻を既定としている)  
    created_date = models.DateTimeField(default=timezone.now)
    # 承認済：コメントが承認されたかどうかを示すTrue/Falseフィールド(既定はFalse)
    approved_comment = models.BooleanField(default=False)

    # コメントを承認するためのメソッド。  
    def approve(self):
        # コメントを承認すると'approve_comment'フィールドがTrueになる。  
        self.approved_comment = True
        # Djangoのモデルインスタンスのメソッド。データベースにそのインスタンスの変更を保存する。
        self.save()

    # postオブジェクトを文字列として表現するために使われる。
    def __str__(self):
        # メソッド内で'self.text'を返すことで、テキストの内容を文字列として返す。  
        return self.text
        
def approved_comments(self):
    return self.comments.filter(approved_comment=True)
    
class ToDo(models.Model):
    title = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    deadline = models.DateField(blank=True, null=True)  # DateTimeFieldからDateFieldに変更
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
        
    # objectsマネージャーを追加する。  
    objects = models.Manager()
    
class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    # objectsマネージャーを追加する。  
    objects = models.Manager()
    
class Group(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
     # objectsマネージャーを追加する。  
    objects = models.Manager()