# django.shortcutsモジュールからrender関数とget_object_or_404関数をインポート
# render：テンプレートをロードしてレンダリングし、HTTPレスポンスを返すための関数
# get_object_or_404：データベースから特定のモデルのオブジェクトを取得するための関数。オブジェクトが存在しない場合は404エラーを返す。
from django.shortcuts import render, get_object_or_404
# アプリケーション内のmodels.pyからPostとCommentモデルをインポート
from .models import Post, Comment
# Djangoのタイムゾーンユーティリティをインポート
from django.utils import timezone
# アプリケーション内のforms.pyからPostFormとCommentFormフォームをインポート
from .forms import PostForm, CommentForm
# リダイレクト機能を提供するredirect関数をインポート
from django.shortcuts import redirect
# ログインが必要なビューにデコレータを適用するためのlogin_requiredデコレータをインポート
from django.contrib.auth.decorators import login_required
# Djangoの認証機能に関連するlogin関数とauthenticate関数をインポート
from django.contrib.auth import login, authenticate
# アプリケーション内のforms.pyからSignUpFormフォームをインポート
from .forms import SignUpForm
# アプリケーション内のmodels.pyからToDoモデルをインポート
from .models import ToDo
# アプリケーション内のforms.pyからToDoFormフォームをインポート
from .forms import ToDoForm 
# アプリケーション内のmodels.pyからNoteモデルをインポート
from .models import Note
# アプリケーション内のforms.pyからNoteFormフォームをインポート
from .forms import NoteForm
# アプリケーション内のmodels.pyからGroupモデルをインポート
from .models import Group
# アプリケーション内のforms.pyからGroupFormとJoinGroupFormフォームをインポート
from .forms import GroupForm, JoinGroupForm

from .models import Question, Message

from .forms import QuestionForm, MessageForm

from django.http import HttpResponse, HttpResponseRedirect

from django.urls import reverse


# @login_requiredデコレータにより、このビューはログインしているユーザーのみがアクセスできるようになる。
@login_required
# post_list関数
def post_list(request):
    # Postモデルから公開日時が現在時刻以下の投稿を取得し、公開日時の降順でソートされたクエリセットが代入される。
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    # ToDoモデルのすべてのオブジェクトが代入される。
    todos = ToDo.objects.all()
    # 作成したTodoを表示する。
    print(todos) 
    # ToDoFormのインスタンスが代入されます。これにより、ToDoを追加するためのフォームがビューに渡される。
    form = ToDoForm() 
    # リクエストされたユーザーオブジェクトが代入される。
    user = request.user
    # リクエストされたユーザーが所属するすべてのグループが代入される。
    groups = user.groups.all()
    # render関数を使用して、blog/post_list.htmlテンプレートをレンダリングする。
    # このとき、posts、todos、form、groupsという変数をテンプレートに渡す。
    # {}の中に指定した情報をテンプレートが表示してくれる。中身は'名前'と'値'
    return render(request, 'blog/post_list.html', {'posts': posts, 'todos': todos, 'form': form, 'groups': groups})
    
# @login_requiredデコレータにより、このビューはログインしているユーザーのみがアクセスできるようになる。
@login_required
# post_detail関数：requestオブジェクトとpk（プライマリーキー）が渡される。
# pkはURLから取得され、表示する投稿の特定の識別子を示す。
def post_detail(request, pk):
    # get_object_or_404関数を使用して、Postモデルからpkに対応する投稿を取得する。
    # 投稿が存在しない場合、HTTP 404 エラーが発生
    post = get_object_or_404(Post, pk=pk)
    # blog/post_detail.htmlテンプレートをレンダリングする。
    # このとき、postという名前の変数をテンプレートに渡す。
    return render(request, 'blog/post_detail.html', {'post': post})
    
# @login_requiredデコレータにより、このビューはログインしているユーザーのみがアクセスできるようになる。
@login_required
# post_new関数
def post_new(request):
    
    # 最初に、HTTP リクエストが POST メソッドであるかどうかをチェックする。
    # POST メソッドであれば、ユーザーがフォームを送信したことを意味する。
    if request.method == "POST":
        # POST メソッドの場合、送信されたフォームデータを使って PostForm を初期化する。
        form = PostForm(request.POST)
        # フォームのバリデーションを行う。
        # フォームが正しいデータで満たされている場合、新しい投稿を作成する。
        if form.is_valid():
            # commit=False を使って、まだ保存されていない新しい投稿オブジェクトを取得する。
            post = form.save(commit=False)
            # 現在のログインユーザーを投稿の著者として設定する。
            post.author = request.user
            # 現在の日時を投稿の公開日時として設定する。
            post.published_date = timezone.now()
            # 新しい投稿を保存する。
            post.save()
            # 新しい投稿が保存されたら、投稿の詳細ページにリダイレクトする。
            return redirect('post_detail', pk=post.pk)
            
    # POST メソッドでない場合（つまり、最初のページアクセス時）、新しい空の PostForm オブジェクトを生成する。
    else:
        form = PostForm()
    # フォームを含んだ blog/post_edit.html テンプレートをレンダリングし、ユーザーが新しい投稿を作成するためのフォームを表示する。
    return render(request, 'blog/post_edit.html', {'form': form})
    
# @login_requiredデコレータにより、このビューはログインしているユーザーのみがアクセスできるようになる。
@login_required
# post_edit関数：requestオブジェクトとpk（プライマリーキー）が渡される。
def post_edit(request, pk):
    # 最初に、get_object_or_404 関数を使用して、編集対象の投稿を取得する。
    # 投稿が存在しない場合、HTTP 404 エラーが発生する。
    post = get_object_or_404(Post, pk=pk)
    # HTTP リクエストが POST メソッドであるかどうかをチェックする。
    # POST メソッドであれば、ユーザーがフォームを送信したことを意味する。
    if request.method == "POST":
        # POST メソッドの場合、フォームを初期化する。
        # instance=post を指定して、編集対象の投稿データをフォームにプリロードする。
        form = PostForm(request.POST, instance=post)
        # フォームのバリデーションを行う。
        # フォームが正しいデータで満たされている場合、編集を保存する。
        if form.is_valid():
            # まだ保存されていない編集された投稿オブジェクトを取得する。
            post = form.save(commit=False)
            # 現在のログインユーザーを投稿の著者として設定する。
            post.author = request.user
            # 現在の日時を投稿の公開日時として設定する。
            post.published_date = timezone.now()
            # 編集された投稿を保存する。
            post.save()
            # 編集された投稿が保存されたら、その投稿の詳細ページにリダイレクトする。
            return redirect('post_detail', pk=post.pk)
    # POST メソッドでない場合（つまり、最初のページアクセス時）、編集対象の投稿データをプリロードしたフォームを生成する。
    else:
        form = PostForm(instance=post)
    # フォームを含んだ blog/post_edit.html テンプレートをレンダリングし、ユーザーが投稿を編集するためのフォームを表示する。
    return render(request, 'blog/post_edit.html', {'form': form})

# @login_requiredデコレータにより、このビューはログインしているユーザーのみがアクセスできるようになる。
@login_required
# post_publish関数：requestオブジェクトとpk（プライマリーキー）が渡される。
def post_publish(request, pk):
    # 最初に、get_object_or_404 関数を使用して、公開する投稿を取得する。
    # 投稿が存在しない場合、HTTP 404 エラーが発生する。
    post = get_object_or_404(Post, pk=pk)
    # 取得した投稿に対して、publish() メソッドを呼び出して投稿を公開する。
    # このメソッドは、投稿オブジェクトの状態を更新し、公開日時を現在時刻に設定することが想定される。
    post.publish()
    # 公開が完了したら、公開された投稿の詳細ページにリダイレクトする。
    return redirect('post_detail', pk=pk)
    
# @login_requiredデコレータにより、このビューはログインしているユーザーのみがアクセスできるようになる。
@login_required
# post_remove関数：requestオブジェクトとpk（プライマリーキー）が渡される。
def post_remove(request, pk):
    # 最初に、get_object_or_404 関数を使用して、削除する投稿を取得する。
    # 投稿が存在しない場合、HTTP 404 エラーが発生する。
    post = get_object_or_404(Post, pk=pk)
    # 取得した投稿に対して、delete() メソッドを呼び出して投稿を削除する。
    post.delete()
    # 削除が完了したら、投稿一覧ページにリダイレクトする。
    return redirect('post_list')
    
# @login_requiredデコレータにより、このビューはログインしているユーザーのみがアクセスできるようになる。
@login_required
# add_comment_to_post関数：requestオブジェクトとpk（プライマリーキー）が渡される。
def add_comment_to_post(request, pk):
    # 最初に、get_object_or_404 関数を使用して、コメントを追加する対象の投稿を取得する。
    # もし投稿が存在しない場合、HTTP 404 エラーが発生する。
    post = get_object_or_404(Post, pk=pk)
    # HTTP リクエストが POST メソッドであるかどうかをチェックする。
    # POST メソッドであれば、ユーザーがコメントを送信したことを意味する。
    if request.method == "POST":
        # POST メソッドの場合、CommentFormを使ってコメントフォームを初期化する。
        # request.POSTを使って、ユーザーが送信したフォームデータを取得する。
        form = CommentForm(request.POST)
        # フォームのバリデーションを行う。
        # フォームが正しいデータで満たされている場合、コメントを保存する。
        if form.is_valid():
            # まだ保存されていない新しいコメントオブジェクトを取得する。
            comment = form.save(commit=False)
            # コメントの関連付けられる投稿を設定する。
            comment.post = post
            # 新しいコメントを保存する。
            comment.save()
            # コメントが保存されたら、その投稿の詳細ページにリダイレクトする。
            return redirect('post_detail', pk=post.pk)
    # POST メソッドでない場合（つまり、最初のページアクセス時）、空の CommentForm オブジェクトを生成する。
    else:
        form = CommentForm()
    # フォームを含んだ blog/add_comment_to_post.html テンプレートをレンダリングし、ユーザーがコメントを追加するためのフォームを表示する。
    return render(request, 'blog/add_comment_to_post.html', {'form': form})
    
# @login_requiredデコレータにより、このビューはログインしているユーザーのみがアクセスできるようになる。
@login_required
# comment_approve関数：requestオブジェクトとpk（プライマリーキー）が渡される。
def comment_approve(request, pk):
    # 最初に、get_object_or_404 関数を使用して、承認するコメントを取得する。
    # もしコメントが存在しない場合、HTTP 404 エラーが発生する。
    comment = get_object_or_404(Comment, pk=pk)
    # 取得したコメントに対して、approve() メソッドを呼び出してコメントを承認する。
    # このメソッドは、コメントオブジェクトの状態を更新し、コメントを承認済み状態に変更することが想定される。
    comment.approve()
    # コメントが承認されたら、そのコメントが関連付けられている投稿の詳細ページにリダイレクトする。
    return redirect('post_detail', pk=comment.post.pk)

# @login_requiredデコレータにより、このビューはログインしているユーザーのみがアクセスできるようになる。
@login_required
# comment_remove関数：requestオブジェクトとpk（プライマリーキー）が渡される。
def comment_remove(request, pk):
    # 最初に、get_object_or_404 関数を使用して、削除するコメントを取得する。
    # もしコメントが存在しない場合、HTTP 404 エラーが発生する。
    comment = get_object_or_404(Comment, pk=pk)
    # 取得したコメントに対して、delete() メソッドを呼び出してコメントを削除する。
    comment.delete()
    # コメントが削除されたら、そのコメントが関連付けられている投稿の詳細ページにリダイレクトする。
    return redirect('post_detail', pk=comment.post.pk)
    
# signup関数：requestオブジェクトが渡される。
def signup(request):
    # 最初に、HTTP リクエストが POST メソッドであるかどうかをチェックする。
    # POST メソッドであれば、ユーザーが登録フォームを送信したことを意味する。
    if request.method == 'POST':
        # POST メソッドの場合、フォームを初期化する。
        # request.POST を使って、ユーザーが送信したデータを取得し、そのデータを使ってフォームを満たす。
        form = SignUpForm(request.POST)
        # フォームのバリデーションを行う。
        # フォームが正しいデータで満たされている場合、新しいユーザーをデータベースに保存する。
        if form.is_valid():
            # 新しいユーザーをデータベースに保存する。
            form.save()
            # ユーザー名とパスワードを取得する。
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            # ユーザーを認証します。認証が成功した場合、login() 関数を使ってユーザーをログイン状態にする。
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            # ユーザーが正常に登録され、ログインされたら、投稿一覧ページにリダイレクトする。
            return redirect('post_list')
    # POST メソッドでない場合（つまり、最初のページアクセス時）、新しい空の SignUpForm オブジェクトを生成する。
    else:
        form = SignUpForm()
    # フォームを含んだ registration/signup.html テンプレートをレンダリングし、ユーザーが登録フォームを入力するためのフォームを表示する。
    return render(request, 'registration/signup.html', {'form': form})

# @login_requiredデコレータにより、このビューはログインしているユーザーのみがアクセスできるようになる。
@login_required
# todo_list関数：requestオブジェクトが渡される。
def todo_list(request):
    # ToDoモデルのすべてのオブジェクトを取得する。
    todos = ToDo.objects.all()
    # ToDoを追加するためのフォームを作成する。
    # ユーザーが新しいToDoを入力するためのフォーム
    form = ToDoForm()
    # todo/todo_list.html テンプレートをレンダリングする。レンダリングする際に、ToDoリストとToDo追加フォームをテンプレートに渡す。
    return render(request, 'todo/todo_list.html', {'todos': todos, 'form': form})
   
# @login_requiredデコレータにより、このビューはログインしているユーザーのみがアクセスできるようになる。
@login_required
# todo_create関数：requestオブジェクトが渡される。
def todo_create(request):
    # HTTPリクエストがPOSTメソッドであるかどうかをチェックする。
    # POSTメソッドであれば、ユーザーがToDoを作成するためにフォームを送信したことを意味する。
    if request.method == 'POST':
        # POSTメソッドの場合、ToDoForm を初期化する。
        # 送信されたデータを使ってフォームを満たす。
        form = ToDoForm(request.POST)
        # フォームのバリデーションを行う。
        # フォームが正しいデータで満たされている場合、新しいToDoをデータベースに保存する。
        if form.is_valid():
            # 新しいToDoをデータベースに保存する。
            form.save()
            # ToDoが正常に作成されたら、投稿一覧ページにリダイレクトする。
            return redirect('post_list')
    # POSTメソッドでない場合（つまり、最初のページアクセス時）、新しい空のToDoFormオブジェクトを生成する。
    else:
        form = ToDoForm()
    # フォームを含んだtodo/todo_create.htmlテンプレートをレンダリングし、ユーザーがToDoを作成するためのフォームを表示する。
    return render(request, 'todo/todo_create.html', {'form': form})

# @login_requiredデコレータにより、このビューはログインしているユーザーのみがアクセスできるようになる。
@login_required
# todo_detail関数：requestオブジェクトとpk（プライマリーキー）が渡される。
# 指定されたプライマリーキー（pk）に対応する ToDo オブジェクトを取得する。ToDo オブジェクトが存在しない場合、HTTP 404 エラーが発生する。
def todo_detail(request, pk):
    # 取得した ToDo オブジェクトを 'todo' という名前の変数として、todo/todo_detail.html テンプレートに渡す。
    todo = get_object_or_404(ToDo, pk=pk)
    # render 関数を使用して、todo/todo_detail.html テンプレートをレンダリングする。
    # ToDo オブジェクトをテンプレートに渡すことで、ToDo の詳細情報を表示する。
    return render(request, 'todo/todo_detail.html', {'todo': todo})

# @login_requiredデコレータにより、このビューはログインしているユーザーのみがアクセスできるようになる。
@login_required
# todo_detail関数：requestオブジェクトとpk（プライマリーキー）が渡される。
def todo_edit(request, pk):
    # 最初に、get_object_or_404 関数を使用して、編集するToDoオブジェクトを取得する。
    # ToDoオブジェクトが存在しない場合、HTTP 404 エラーが発生する。
    todo = get_object_or_404(ToDo, pk=pk)
    # HTTPリクエストがPOSTメソッドであるかどうかをチェックする。
    # POSTメソッドであれば、ユーザーがToDoを編集するためのフォームを送信したことを意味する。
    if request.method == 'POST':
        # POSTメソッドの場合、ToDoForm を初期化する。
        # 送信されたデータと編集対象のToDoオブジェクトを使ってフォームを満たす。
        form = ToDoForm(request.POST, instance=todo)
        # フォームのバリデーションを行う。
        # フォームが正しいデータで満たされている場合、編集内容をデータベースに保存する。
        if form.is_valid():
            # 編集されたToDoをデータベースに保存する。
            form.save()
            # ToDoが正常に編集されたら、投稿一覧ページにリダイレクトする。
            return redirect('post_list')
    # POSTメソッドでない場合（つまり、最初のページアクセス時）、編集対象のToDoオブジェクトを使ってフォームを初期化する。
    else:
        form = ToDoForm(instance=todo)
    # フォームを含んだtodo/todo_edit.htmlテンプレートをレンダリングし、ユーザーがToDoを編集するためのフォームを表示する。
    return render(request, 'todo/todo_edit.html', {'form': form})

# @login_requiredデコレータにより、このビューはログインしているユーザーのみがアクセスできるようになる。
@login_required
# todo_delete関数：requestオブジェクトとpk（プライマリーキー）が渡される。
def todo_delete(request, pk):
    # 最初に、get_object_or_404 関数を使用して、削除するToDoオブジェクトを取得する。
    # ToDoオブジェクトが存在しない場合、HTTP 404 エラーが発生する。
    todo = get_object_or_404(ToDo, pk=pk)
    # 取得したToDoオブジェクトに対して、delete() メソッドを呼び出してToDoを削除する。
    todo.delete()
    # ToDoが削除されたら、ToDoリストページにリダイレクトする。
    return redirect('todo_list')
 
 # @login_requiredデコレータにより、このビューはログインしているユーザーのみがアクセスできるようになる。
@login_required
# note_list関数：requestオブジェクトが渡される。
def note_list(request):
    # すべてのノートオブジェクトを取得する。
    notes = Note.objects.all()
    # render 関数を使用して、note/note_list.html テンプレートをレンダリングする。
    # レンダリングする際に、ノートリストをテンプレートに渡す。
    return render(request, 'note/note_list.html', {'notes': notes})

# @login_requiredデコレータにより、このビューはログインしているユーザーのみがアクセスできるようになる。
@login_required
# note_detail関数：requestオブジェクトとpk（プライマリーキー）が渡される。
def note_detail(request, pk):
    # 指定されたプライマリーキー（pk）に対応するノートオブジェクトを取得する。
    # 指定されたノートが存在しない場合、DoesNotExist 例外が発生する。
    note = Note.objects.get(pk=pk)
    # テンプレート note/note_detail.html をレンダリングする際に、取得したノートオブジェクトをテンプレートに渡す。
    return render(request, 'note/note_detail.html', {'note': note})

# @login_requiredデコレータにより、このビューはログインしているユーザーのみがアクセスできるようになる。
@login_required
# note_create関数：requestオブジェクトが渡される。
def note_create(request):
    # HTTPリクエストがPOSTメソッドであるかどうかをチェックする。
    # POSTメソッドであれば、ユーザーがノートを作成するためのフォームを送信したことを意味する。
    if request.method == 'POST':
        # POSTメソッドの場合、NoteForm を初期化する。
        # 送信されたデータを使ってフォームを満たす。
        form = NoteForm(request.POST)
        # フォームのバリデーションを行う。
        # フォームが正しいデータで満たされている場合、新しいノートをデータベースに保存する。
        if form.is_valid():
            # 新しいノートをデータベースに保存する。
            form.save()
            # ノートが正常に作成されたら、投稿一覧ページにリダイレクトする。
            return redirect('post_list')
    # POSTメソッドでない場合（つまり、最初のページアクセス時）、新しい空のNoteFormオブジェクトを生成する。
    else:
        form = NoteForm()
    # フォームを含んだnote/note_create.htmlテンプレートをレンダリングし、ユーザーがノートを作成するためのフォームを表示する。
    return render(request, 'note/note_create.html', {'form': form})

# @login_requiredデコレータにより、このビューはログインしているユーザーのみがアクセスできるようになる。
@login_required
# note_detail関数：requestオブジェクトとpk（プライマリーキー）が渡される。
def note_update(request, pk):
    # 指定されたプライマリーキー（pk）に対応するノートオブジェクトを取得する。
    # 指定されたノートが存在しない場合、DoesNotExist 例外が発生する。
    note = Note.objects.get(pk=pk)
    # HTTPリクエストがPOSTメソッドであるかどうかをチェックする。
    # POSTメソッドであれば、ユーザーがノートを更新するためのフォームを送信したことを意味する。
    if request.method == 'POST':
        # POSTメソッドの場合、NoteForm を初期化する。
        # 送信されたデータと編集対象のノートオブジェクトを使ってフォームを満たす。
        form = NoteForm(request.POST, instance=note)
        # フォームのバリデーションを行う。
        # フォームが正しいデータで満たされている場合、編集内容をデータベースに保存する。
        if form.is_valid():
            # 更新されたノートをデータベースに保存する。
            form.save()
            # ノートが正常に更新されたら、ノートリストページにリダイレクトする。
            return redirect('note_list')
    # POSTメソッドでない場合（つまり、最初のページアクセス時）、編集対象のノートオブジェクトを使ってフォームを初期化する。
    else:
        form = NoteForm(instance=note)
    # フォームを含んだnote/note_form.htmlテンプレートをレンダリングし、ユーザーがノートを更新するためのフォームを表示する。
    return render(request, 'note/note_form.html', {'form': form})

# @login_requiredデコレータにより、このビューはログインしているユーザーのみがアクセスできるようになる。
@login_required
# note_delete関数：requestオブジェクトとpk（プライマリーキー）が渡される。
def note_delete(request, pk):
    # 削除するノートオブジェクトを取得する。
    # ノートオブジェクトが存在しない場合、HTTP 404 エラーが発生する。
    note = get_object_or_404(Note, pk=pk)
    # 取得したノートオブジェクトに対して、delete() メソッドを呼び出してノートを削除する。
    note = Note.objects.get(pk=pk)
    # ノートが削除されたら、ノートリストページにリダイレクトする。
    note.delete()
    return redirect('note_list')
    
# @login_requiredデコレータにより、このビューはログインしているユーザーのみがアクセスできるようになる。
@login_required
# group_list関数：requestオブジェクトが渡される。
def group_list(request):
    # すべてのグループオブジェクトを取得する。
    groups = Group.objects.all()
    # render 関数を使用して、group/group_list.html テンプレートをレンダリングする。
    # レンダリングする際に、グループリストをテンプレートに渡す。
    return render(request, 'group/group_list.html', {'groups': groups})

# @login_requiredデコレータにより、このビューはログインしているユーザーのみがアクセスできるようになる。
@login_required
# group_detail関数：requestオブジェクトとpk（プライマリーキー）が渡される。
def group_detail(request, pk):
    # 指定されたプライマリーキー（pk）に対応するグループオブジェクトを取得する。
    # 指定されたグループが存在しない場合、DoesNotExist 例外が発生する。
    group = Group.objects.get(pk=pk)
    # テンプレート group/group_detail.html をレンダリングする際に、取得したグループオブジェクトをテンプレートに渡す。
    return render(request, 'group/group_detail.html', {'group': group})

# @login_requiredデコレータにより、このビューはログインしているユーザーのみがアクセスできるようになる。
@login_required
# group_create関数：requestオブジェクトが渡される。
def group_create(request):
    # HTTPリクエストがPOSTメソッドであるかどうかをチェックする。
    # POSTメソッドであれば、ユーザーがグループを作成するためのフォームを送信したことを意味する。
    if request.method == 'POST':
        # POSTメソッドの場合、GroupForm を初期化する。
        # 送信されたデータを使ってフォームを満たす。
        form = GroupForm(request.POST)
        # フォームのバリデーションを行う。
        # フォームが正しいデータで満たされている場合、新しいグループをデータベースに保存する。
        if form.is_valid():
            # 新しいグループをデータベースに保存する。
            # 同時に、group.members.add(request.user) を使って、グループのメンバーとしてリクエストを送信したユーザーを追加する。
            group = form.save()
            group.members.add(request.user)
            # グループが正常に作成されたら、そのグループの詳細ページにリダイレクトする。
            return redirect('group_detail', pk=group.pk)
    # POSTメソッドでない場合（つまり、最初のページアクセス時）、新しい空のGroupFormオブジェクトを生成する。
    else:
        form = GroupForm()
    # フォームを含んだgroup/group_create.htmlテンプレートをレンダリングし、ユーザーがグループを作成するためのフォームを表示する。
    return render(request, 'group/group_create.html', {'form': form})

# @login_requiredデコレータにより、このビューはログインしているユーザーのみがアクセスできるようになる。
@login_required
# group_update関数：requestオブジェクトとpk（プライマリーキー）が渡される。
def group_update(request, pk):
    # 指定されたプライマリーキー（pk）に対応するグループオブジェクトを取得する。
    # 指定されたグループが存在しない場合、DoesNotExist 例外が発生する。
    group = Group.objects.get(pk=pk)
    # HTTPリクエストがPOSTメソッドであるかどうかをチェックする。
    # POSTメソッドであれば、ユーザーがグループを更新するためのフォームを送信したことを意味する。
    if request.method == 'POST':
        # POSTメソッドの場合、GroupForm を初期化する。
        # 送信されたデータと編集対象のグループオブジェクトを使ってフォームを満たす。
        form = GroupForm(request.POST, instance=group)
        # フォームのバリデーションを行う。
        # フォームが正しいデータで満たされている場合、編集内容をデータベースに保存する。
        if form.is_valid():
            # 更新されたグループをデータベースに保存する。
            form.save()
            # グループが正常に更新されたら、投稿一覧ページにリダイレクトする。
            return redirect('post_list')
    # POSTメソッドでない場合（つまり、最初のページアクセス時）、編集対象のグループオブジェクトを使ってフォームを初期化する。
    else:
        form = GroupForm(instance=group)
    # フォームを含んだgroup/group_update.htmlテンプレートをレンダリングし、ユーザーがグループを更新するためのフォームを表示する。
    return render(request, 'group/group_update.html', {'form': form})

# @login_requiredデコレータにより、このビューはログインしているユーザーのみがアクセスできるようになる。
@login_required
# group_delete関数：requestオブジェクトとpk（プライマリーキー）が渡される。
def group_delete(request, pk):
    # 削除するグループオブジェクトを取得する。
    # グループオブジェクトが存在しない場合、HTTP 404 エラーが発生する。
    group = get_object_or_404(Group, pk=pk)
    group = Group.objects.get(pk=pk)
    # 取得したグループオブジェクトに対して、delete() メソッドを呼び出してグループを削除する。
    group.delete()
    # グループが削除されたら、グループリストページにリダイレクトする。
    return redirect('group_list')

# @login_requiredデコレータにより、このビューはログインしているユーザーのみがアクセスできるようになる。
@login_required
def qa_chat_page(request):
    questions = Question.objects.all()
    messages = Message.objects.all()
    return render(request, 'qa/qa_chat_page.html', {'questions': questions, 'messages': messages})

@login_required
def post_question(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        # 質問をデータベースに保存
        message = Message.objects.create(author=request.user, content=content)
        # リダイレクト先を指定せずに、チャットエリアに即座に表示させる
        return redirect('qa_chat_page')

@login_required
def post_chat_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('qa_chat_page')
    else:
        form = MessageForm()
    return render(request, 'qa_chat_page', {'form': form})
    
@login_required
def edit_message(request, message_id):
    # メッセージの編集ロジックを実装する
    return HttpResponse("Edit message")

def delete_message(request, message_id):
    # メッセージの削除ロジックを実装する
    message = Message.objects.get(pk=message_id)
    message.delete()
    # メッセージを削除した後、リダイレクトする
    return HttpResponseRedirect(reverse('qa_chat_page'))