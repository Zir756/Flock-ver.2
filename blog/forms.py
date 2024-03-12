# 最初にDjangoのformsをインポート
# formsモジュールをインポートすることで、フォームを作成してユーザーからの入力を処理するためのツールや機能を利用できるようになる。
from django import forms
# Postモデルをインポート
# commentモデルもインポート
from .models import Post, Comment
# Djangoの認証システムに関連するフォームを提供するUserCreationFormをインポート
from django.contrib.auth.forms import UserCreationForm
# Djangoの組み込みユーザーモデルであるUserをインポート(ユーザーの認証情報を格納する。)
from django.contrib.auth.models import User
# カレントディレクトリ内のmodels.pyファイルからToDoモデルをインポート
# アプリケーションで定義されたToDoモデルを使用することを意味する。
from .models import ToDo
# カレントディレクトリ内のmodels.pyファイルからNoteモデルをインポート
# アプリケーションで定義されたNoteモデルを使用することを意味する。
from .models import Note
# カレントディレクトリ内のmodels.pyファイルからGroupモデルをインポート
# アプリケーションで定義されたGroupモデルを使用することを意味する。
from .models import Group

from .models import Question

from .models import Message

# 保留機能
# from .join_group_form import JoinGroupForm

# forms.ModelFormを継承してPostFormクラスを定義している。
class PostForm(forms.ModelForm):

    # Djangoにフォームを作るときにどのモデルを使えばいいか (model = Post) を伝える。
    class Meta:
        # Postモデルを基にしてフォームが作成される。
        model = Post
        # フォームに表示するフィールドを指定する。('title', 'text',)というフィールドがフォームに含まれる。
        fields = ('title', 'text',)
        
# forms.ModelFormを継承してCommentFormクラスを定義している。
class CommentForm(forms.ModelForm):

    # Djangoにフォームを作るときにどのモデルを使えばいいか (model = Comment) を伝える。
    class Meta:
        # Commentモデルを基にしてフォームが作成される。
        model = Comment
        # フォームに表示するフィールドを指定する。('author', 'text',)というフィールドがフォームに含まれる。
        fields = ('author', 'text',)
        
# UserCreationFormを継承してSignUpFormクラスを定義している。
class SignUpForm(UserCreationForm):
    
    # emailという名前のEmailFieldを定義している。
    # ユーザーがメールアドレスを入力するためのフィールド
    email = forms.EmailField(max_length=254, help_text='有効なメールアドレスを記入してください。')

    # Djangoにフォームを作るときにどのモデルを使えばいいか (model = User) を伝える。
    class Meta:
        # Userモデルを基にしてフォームが作成される。
        model = User
        # フォームに表示するフィールドを指定する。('username', 'email', 'password1', 'password2')というフィールドがフォームに含まれる。
        # password1とpassword2は、パスワードの入力と確認のためのフィールド
        fields = ('username', 'email', 'password1', 'password2')
        
# forms.ModelFormを継承してToDoFormクラスを定義している。
class ToDoForm(forms.ModelForm):
    
    # Djangoにフォームを作るときにどのモデルを使えばいいか (model = ToDo) を伝える。
    class Meta:
        # ToDoモデルを基にしてフォームが作成される。
        model = ToDo
        # フォームに表示するフィールドを指定する。('title', 'deadline')というフィールドがフォームに含まれる。
        fields = ('title', 'deadline')
        # フォームの特定のフィールドに対してウィジェットをカスタマイズしている。
        # deadlineフィールドに対してDateInputウィジェットを設定しており、そのウィジェットの属性としてtypeがdateと指定されている。
        # ブラウザはdeadlineフィールドを日付入力フィールドとして表示する。
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'})
        }
        
# forms.ModelFormを継承してNoteFormクラスを定義している。
class NoteForm(forms.ModelForm):
    
    # Djangoにフォームを作るときにどのモデルを使えばいいか (model = Note) を伝える。
    class Meta:
        # Noteモデルを基にしてフォームが作成される。
        model = Note
        # フォームに表示するフィールドを指定する。('title', 'content')というフィールドがフォームに含まれる。
        fields = ('title', 'content')
        # フォームの特定のフィールドに対してウィジェットをカスタマイズしている。
        # deadlineフィールドに対してDateInputウィジェットを設定しており、そのウィジェットの属性としてtypeがdateと指定されている。
        # ブラウザはdeadlineフィールドを日付入力フィールドとして表示する。
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'})
        }
        
# forms.ModelFormを継承してGroupFormクラスを定義している。
class GroupForm(forms.ModelForm):
    
    # Djangoにフォームを作るときにどのモデルを使えばいいか (model = Group) を伝える。
    class Meta:
        # membersフィールド。グループのメンバーを選択するためのチェックボックスを表示するためのModelMultipleChoiceField
        members = forms.ModelMultipleChoiceField(queryset=User.objects.all(), widget=forms.CheckboxSelectMultiple)
        # Groupモデルを基にしてフォームが作成される。
        model = Group
        # フォームに表示するフィールドを指定する。('name', 'members')というフィールドがフォームに含まれる。
        fields = ('name', 'members')
        
# forms.Formを継承している。そのため、このフォームはモデルフォームではなく、単純なフォームとして定義されている。
class JoinGroupForm(forms.Form):
        # group_codeフィールド。
        group_code = forms.CharField(max_length=100)
        
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'content']
        
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']