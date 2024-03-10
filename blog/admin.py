# Djangoの管理サイトにモデルを登録するためのもの
# admin モジュールから ModelAdmin クラスを使用して管理者向けのインターフェースを作成し、それぞれのモデルに対応する管理ページを提供する。
from django.contrib import admin

# カレントディレクトリ（アプリケーション）内の models.py ファイルからモデルをインポート
from .models import Post, Comment
from .models import ToDo
from .models import Note
from .models import Group

# Register your models here.

# それぞれのモデルをDjango管理サイトに登録するためのもの
# admin.site.register(ModelName) を使用して、ModelName モデルを管理サイトに登録する。
# これにより、管理者がDjangoの管理サイトでそれぞれのモデルを編集、作成、削除などの操作を行うことができるようになる。
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(ToDo)
admin.site.register(Note)
admin.site.register(Group)