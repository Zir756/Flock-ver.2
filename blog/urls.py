# path 関数を使用して、特定のURLパターンに対してどのビューを呼び出すかを指定する。
from django.urls import path
# 現在のディレクトリ（アプリケーション）を示し、views モジュールからビューをインポートする。
from . import views

# URLconfのリストであり、Djangoアプリケーション内のURLパターンを定義する。
urlpatterns = [
    # path(URL, 関数またはクラス, name=URL名称)
    # ルートURL（空の文字列）に対応している。
    # 具体的には、views.post_list ビューを呼び出して、投稿のリストを表示する。
    # これにより、アプリケーションのホームページやエントリーポイントとして機能する。
    path('', views.post_list, name='post_list'),
    
    # post/<int:pk>/: pk という整数値を持つ投稿の詳細を表示するためのパス
    # 例えば、'/post/1/' のようなURLは、IDが1の投稿の詳細を表示する。
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    
    # 新しい投稿を作成するためのフォームを表示するためのパス
    path('post/new/', views.post_new, name='post_new'),
    
    # 特定のIDを持つ投稿を編集するためのフォームを表示するためのパス
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    
    # 特定のIDを持つ投稿を公開するためのアクションを実行するためのパス
    path('post/<pk>/publish/', views.post_publish, name='post_publish'),
    
    # 特定のIDを持つ投稿を削除するためのアクションを実行するためのパス
    path('post/<pk>/remove/', views.post_remove, name='post_remove'),
    
    # 特定の投稿にコメントを追加するためのパス
    # pk は投稿のプライマリーキーを表す。
    # views.add_comment_to_post ビューにマッピングされ、コメントの追加フォームを表示する。
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    
    # 特定のコメントを承認するためのパス
    # pk はコメントのプライマリーキーを表す。
    # views.comment_approve ビューにマッピングされ、コメントを承認するアクションを実行する。
    path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
    
    # 特定のコメントを削除するためのパス
    # pk はコメントのプライマリーキーを表す。
    # views.comment_remove ビューにマッピングされ、コメントを削除するアクションを実行する。
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
    
    # 新しいユーザーを登録するためのパス
    # /signup/ というURLにアクセスされたときに、views.signup ビューが呼び出される。
    # このビューは、ユーザー登録フォームを提供し、ユーザーがフォームを送信すると、新しいユーザーアカウントが作成される。
    path('signup/', views.signup, name='signup'),
    
    # ToDoリストを表示するためのパス
    # views.todo_list ビューにマッピングされている。
    path('', views.todo_list, name='todo_list'),
    
    # 新しいToDoを作成するためのパス
    # views.todo_create ビューにマッピングされている。
    path('create/', views.todo_create, name='todo_create'),
    
    # 特定のToDoの詳細を表示するためのパス
    # <int:pk> はToDoのプライマリーキーを表す。
    # views.todo_detail ビューにマッピングされている。
    path('todo/<int:pk>/', views.todo_detail, name='todo_detail'),
    
    # 特定のToDoを編集するためのパス
    # views.todo_edit ビューにマッピングされている。
    path('todo/<int:pk>/edit/', views.todo_edit, name='todo_edit'),
    
    # 特定のToDoを削除するためのパス
    # views.todo_delete ビューにマッピングされている。
    path('todo/<int:pk>/delete/', views.todo_delete, name='todo_delete'),
    
    # note(memo)のリストを表示するためのパス
    # views.note_list ビューにマッピングされている。
    path('note/', views.note_list, name='note_list'),
    
    # 特定のnote(memo)の詳細を表示するためのパス
    # <int:pk> はノートのプライマリーキーを表す。
    # views.note_detail ビューにマッピングされている。
    path('note/<int:pk>/', views.note_detail, name='note_detail'),
    
    # 新しいnote(memo)を作成するためのパス
    # views.note_create ビューにマッピングされている。
    path('note/new/', views.note_create, name='note_create'),
    
    # 特定のnote(memo)を編集するためのパス
    # views.note_update ビューにマッピングされている。
    path('note/<int:pk>/edit/', views.note_update, name='note_update'),
    
    # 特定のnote(memo)を削除するためのパス
    # views.note_delete ビューにマッピングされている。
    path('note/<int:pk>/delete/', views.note_delete, name='note_delete'),
    
    # グループのリストを表示するためのパス
    # views.group_list ビューにマッピングされている。
    path('group/', views.group_list, name='group_list'),
    
    # 特定のグループの詳細を表示するためのパス
    # <int:pk> はグループのプライマリーキーを表す。
    # views.group_detail ビューにマッピングされている。
    path('group/<int:pk>/', views.group_detail, name='group_detail'),
    
    # 新しいグループを作成するためのパス
    # views.group_create ビューにマッピングされている。
    path('group/create/', views.group_create, name='group_create'),
    
    # 特定のグループを編集するためのパス
    # views.group_update ビューにマッピングされている。
    path('group/<int:pk>/edit/', views.group_update, name='group_update'),
    
    # 特定のグループを削除するためのパス
    # views.group_delete ビューにマッピングされている。
    path('group/<int:pk>/delete/', views.group_delete, name='group_delete'),
    
    
    path('qa_chat_page/', views.qa_chat_page, name='qa_chat_page'),
    path('post_question/', views.post_question, name='post_question'),
    path('post_chat_message/', views.post_chat_message, name='post_chat_message'),
    path('delete_message/<int:message_id>/', views.delete_message, name='delete_message'),
]