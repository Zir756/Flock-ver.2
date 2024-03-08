from django.shortcuts import render, get_object_or_404

# '.models'=１つ上がカレントアプリケーションの為 . とファイル名だけで記述することができる。  
# そして"Post"モデルを指定してインポートする。  
from .models import Post, Comment

from django.utils import timezone

from .forms import PostForm, CommentForm

from django.shortcuts import redirect

from django.contrib.auth.decorators import login_required

from django.contrib.auth import login, authenticate

from .forms import SignUpForm

from .models import ToDo

from .forms import ToDoForm  # ToDoフォームをインポート

from .models import Note

from .forms import NoteForm

from .models import Group

from .forms import GroupForm, JoinGroupForm

# post_list関数  
@login_required
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    todos = ToDo.objects.all()  # ToDoリストを取得
    print(todos)  # ToDoリストが正しく取得されているかを確認するためのデバッグ出力
    form = ToDoForm()  # ToDo追加フォームを作成  
    user = request.user
    groups = user.groups.all()
    return render(request, 'blog/post_list.html', {'posts': posts, 'todos': todos, 'form': form, 'groups': groups})
    
    # # 投稿をtimezoneを参照して並べ替える。  
    # posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    # # request引数 'blog/post_list.html'を組み立てる。  
    # # renderという関数を呼び出して得た値をreturnする。 
    # # {}の中に指定した情報をテンプレートが表示してくれる。中身は'名前'と'値'
    # return render(request, 'blog/post_list.html', {'posts': posts})
    
# post_detail関数  
@login_required
def post_detail(request, pk):
  
    # 与えられたpkのPostがない場合、Page Not Found 404 ページが表示されます。
    post = get_object_or_404(Post, pk=pk)
    # request引数 'blog/post_detail.html'を組み立てる。  
    # renderという関数を呼び出して得た値をreturnする。 
    # {}の中に指定した情報をテンプレートが表示してくれる。中身は'名前'と'値'
    return render(request, 'blog/post_detail.html', {'post': post})
    
# post_new関数
@login_required
def post_new(request):
    
    # 最初にページにアクセスしてきた時で空白のフォームが必要な場合。
    if request.method == "POST":
        # methodがPOSTの場合、フォームのデータを使ってPostFormを構築します。
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
            
    # すべてのフォームデータが入力された状態でビューに戻ってくる場合。  
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})
    
# post_edit関数
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
   
#  post_publish関数
@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)
    
@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')
    
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})
    
@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)
    
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('post_list')  # 登録後のリダイレクト先を設定
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required    
def todo_list(request):
    todos = ToDo.objects.all()  # ToDoモデルのオブジェクトを取得
    form = ToDoForm()  # ToDo追加フォームを作成
    return render(request, 'todo/todo_list.html', {'todos': todos, 'form': form})
   
@login_required 
def todo_create(request):
    if request.method == 'POST':
        form = ToDoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')  # Todoを作成した後、post_listページにリダイレクト
    else:
        form = ToDoForm()
    return render(request, 'todo/todo_create.html', {'form': form})

@login_required    
def todo_detail(request, pk):
    todo = get_object_or_404(ToDo, pk=pk)
    return render(request, 'todo/todo_detail.html', {'todo': todo})

@login_required    
def todo_edit(request, pk):
    todo = get_object_or_404(ToDo, pk=pk)
    if request.method == 'POST':
        form = ToDoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('post_list')  # Todoを編集した後、post_listページにリダイレクト
    else:
        form = ToDoForm(instance=todo)
    return render(request, 'todo/todo_edit.html', {'form': form})

@login_required    
def todo_delete(request, pk):
    todo = get_object_or_404(ToDo, pk=pk)
    todo.delete()
    return redirect('todo_list')  # Todoの一覧ページにリダイレクト
 
@login_required   
def note_list(request):
    notes = Note.objects.all()
    return render(request, 'note/note_list.html', {'notes': notes})

@login_required
def note_detail(request, pk):
    note = Note.objects.get(pk=pk)
    return render(request, 'note/note_detail.html', {'note': note})

@login_required
def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = NoteForm()
    return render(request, 'note/note_create.html', {'form': form})

@login_required
def note_update(request, pk):
    note = Note.objects.get(pk=pk)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('note_list')
    else:
        form = NoteForm(instance=note)
    return render(request, 'note/note_form.html', {'form': form})

@login_required
def note_delete(request, pk):
    note = Note.objects.get(pk=pk)
    note.delete()
    return redirect('note_list')
    
@login_required
def group_list(request):
    groups = Group.objects.all()
    return render(request, 'group/group_list.html', {'groups': groups})

@login_required
def group_detail(request, pk):
    group = Group.objects.get(pk=pk)
    return render(request, 'group/group_detail.html', {'group': group})

@login_required
def group_create(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            group.members.add(request.user)  # グループ作成者をメンバーに追加する
            return redirect('post_list')
    else:
        form = GroupForm()
    return render(request, 'group/group_create.html', {'form': form})

@login_required
def group_update(request, pk):
    group = Group.objects.get(pk=pk)
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = GroupForm(instance=group)
    return render(request, 'group/group_update.html', {'form': form})

@login_required
def group_delete(request, pk):
    group = Group.objects.get(pk=pk)
    group.delete()
    return redirect('group_list')