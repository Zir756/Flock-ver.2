from django.conf import settings
from django.db import models
from django.utils import timezone

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