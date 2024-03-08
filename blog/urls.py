from django.urls import path
from . import views

urlpatterns = [
    # path(URL, 関数またはクラス, name=URL名称)
    path('', views.post_list, name='post_list'),
    
    # post/ はURLが post に続けて / で始まることを意味します。
    # <int:pk> – この部分はDjangoは整数の値を期待し、その値がpkという名前の変数でビューに渡されることを意味しています。
    # / – それからURLの最後に再び / が必要です。  
    # つまり'http://127.0.0.1:8000/post/5/'を入力すると、Djangoはpost_detailというビューを探していると理解します。  
    # そしてpkが5という情報をそのビューに転送します。
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    
    path('post/new/', views.post_new, name='post_new'),
    
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    
    path('post/<pk>/publish/', views.post_publish, name='post_publish'),
    
    path('post/<pk>/remove/', views.post_remove, name='post_remove'),
    
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    
    path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
    
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
    
    path('signup/', views.signup, name='signup'),
    
    path('', views.todo_list, name='todo_list'),
    path('create/', views.todo_create, name='todo_create'),  # ToDo追加用のURL
    
    path('todo/<int:pk>/', views.todo_detail, name='todo_detail'),
    
    path('todo/<int:pk>/edit/', views.todo_edit, name='todo_edit'),
    
    path('todo/<int:pk>/delete/', views.todo_delete, name='todo_delete'),
    
    path('note/', views.note_list, name='note_list'),
    path('note/<int:pk>/', views.note_detail, name='note_detail'),
    path('note/new/', views.note_create, name='note_create'),
    path('note/<int:pk>/edit/', views.note_update, name='note_update'),
    path('note/<int:pk>/delete/', views.note_delete, name='note_delete'),
    
    path('group/', views.group_list, name='group_list'),
    path('group/<int:pk>/', views.group_detail, name='group_detail'),
    path('group/create/', views.group_create, name='group_create'),
    path('note/<int:pk>/edit/', views.group_update, name='group_update'),
    path('note/<int:pk>/delete/', views.group_delete, name='group_delete'),
]