// メッセージを追加する関数
function addMessage(author, content) {
    var messageContainer = document.getElementById('message-container');
    var messageElement = document.createElement('div');
    messageElement.classList.add('message');
    messageElement.innerHTML = '<strong>' + author + '</strong>: ' + content;
    messageContainer.appendChild(messageElement);
}

// フォームを取得
var form = document.querySelector('.qa-section form');

// フォームが取得されたことを確認してからイベントリスナーを追加
if (form) {
    form.addEventListener('submit', function(event) {
        event.preventDefault(); // デフォルトの送信を防止

        var titleInput = document.querySelector('.qa-section form input[name="title"]');
        var contentInput = document.querySelector('.qa-section form textarea[name="content"]');
        var title = titleInput.value;
        var content = contentInput.value;

        // 新しいメッセージを追加
        addMessage(title, content);

        // フォームをクリア
        titleInput.value = '';
        contentInput.value = '';
    });
}