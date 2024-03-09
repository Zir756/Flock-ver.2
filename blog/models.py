# Djangoの設定ファイルから設定をインポートする。これには、データベースの接続情報やアプリケーションの設定などが含まれます。
from django.conf import settings
# Djangoのデータベースモデルを定義するための機能を提供するmodelsモジュールをインポートする。
# データベースのテーブルを定義し、それらのテーブル間の関係を定義する。
from django.db import models
#  Djangoのタイムゾーンユーティリティをインポートする。
# タイムゾーンに依存する操作を行うことができる。
from django.utils import timezone
# Djangoの認証システムに関連するUserモデルをインポートする。
# ユーザーの認証情報（ユーザー名、パスワードなど）を保持するために使用される。
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

    # commentオブジェクトを文字列として表現するために使われる。
    def __str__(self):
        # メソッド内で'self.text'を返すことで、テキストの内容を文字列として返す。  
        return self.text
        
# class commentのモデルのメソッドを定義している。
def approved_comments(self):
    # モデルインスタンスに関連付けられたcommentsという関連フィールドに対して、approved_comment=Trueという条件でフィルタリングを行う。
    return self.comments.filter(approved_comment=True)
    
# ToDotクラス(Djangoのモデルとして機能する)
class ToDo(models.Model):
    
    # モデルのフィールドを定義する
    
    # Title：文字列の為のフィールド(文字列200字を設定　※最大255字) 
    title = models.CharField(max_length=200)
    # 作成時：日付と時間のためのフィールド(作成時の時刻を既定としている)
    created_date = models.DateTimeField(default=timezone.now)
    # 期日：締め切り日を表す日付フィールド(blank=Trueとnull=Trueを指定することで、このフィールドが空白またはnullであることを許可している。)
    deadline = models.DateField(blank=True, null=True)  # DateTimeFieldからDateFieldに変更
    # 完了：完了したかどうかを示すブールフィールド(デフォルトでは、ToDoは未完了(False)として設定される。)
    completed = models.BooleanField(default=False)

    # ToDoオブジェクトを文字列として表現するために使われる。
    def __str__(self):
        # メソッド内で'self.title'を返すことで、テキストの内容を文字列として返す。
        return self.title
        
    # objectsマネージャーを追加する。  
    objects = models.Manager()
    
# Note(memo)クラス(Djangoのモデルとして機能する)
class Note(models.Model):
    
    # モデルのフィールドを定義する
    
    # Title:文字列の為のフィールド(文字列100字を設定　※最大255字) 
    title = models.CharField(max_length=100)
    # 内容：短い文字列ではなく、任意の長さのテキストを保存できる。
    content = models.TextField()
    # 作成日時：作成された日時を表す日時フィールド(auto_now_add=Trueパラメーターにより、このフィールドはモデルが作成されたときの時刻で自動的に設定される。)
    created_at = models.DateTimeField(auto_now_add=True)

    # Note(memo)オブジェクトを文字列として表現するために使われる。
    def __str__(self):
        # メソッド内で'self.title'を返すことで、テキストの内容を文字列として返す。
        return self.title
    
    # objectsマネージャーを追加する。  
    objects = models.Manager()
    
# Groupクラス(Djangoのモデルとして機能する)
class Group(models.Model):
    
    # モデルのフィールドを定義する
    
    # 名前：グループの名前を表す文字列フィールド(文字列100字を設定　※最大255字)
    name = models.CharField(max_length=100)
    # メンバー：グループのメンバーを表す多対多の関連フィールド(Userモデルとの多対多の関係を定義)
    # 1つのユーザーが複数のグループに属することができ、1つのグループには複数のユーザーが属することができる。
    members = models.ManyToManyField(User)
    # 作成日時：作成された日時を表す日時フィールド(auto_now_add=Trueパラメーターにより、このフィールドはモデルが作成されたときの時刻で自動的に設定される。)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Groupオブジェクトを文字列として表現するために使われる。
    def __str__(self):
        # メソッド内で'self.name'を返すことで、テキストの内容を文字列として返す。
        return self.name
    
     # objectsマネージャーを追加する。  
    objects = models.Manager()