// 編集ボタンをクリックしたときの処理
document.querySelector('.edit-button').addEventListener('click', function(event) {
    event.preventDefault(); // デフォルトのリンクの挙動をキャンセル

    // モーダルを表示
    document.getElementById('editModal').style.display = 'block';
});

// モーダルの閉じるボタンをクリックしたときの処理
document.querySelector('.close').addEventListener('click', function() {
    // モーダルを非表示
    document.getElementById('editModal').style.display = 'none';
});