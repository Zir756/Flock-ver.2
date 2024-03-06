# 最初にDjangoのformsをインポート
from django import forms

# Postモデルもインポート
# commentモデルもインポート
from .models import Post, Comment

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import ToDo

from .models import Note

# これはフォームの名前です。 このフォームが ModelForm の一種だとDjangoに伝える必要があります。  
class PostForm(forms.ModelForm):

    # Djangoにフォームを作るときにどのモデルを使えばいいか (model = Post) を伝えます。
    class Meta:
        model = Post
        fields = ('title', 'text',)
        
class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)
        
class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='有効なメールアドレスを記入してください。')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
class ToDoForm(forms.ModelForm):
    class Meta:
        model = ToDo
        fields = ['title', 'deadline']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'})
        }
        
class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'})
        }