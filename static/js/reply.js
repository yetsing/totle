var insertReplyInput = function(replyCell, token, link, replyId, topicId) {
    var replyAuthor = e('.reply_author', replyCell)
    var author = replyAuthor.innerText
    var inputItem = `
    <form id="reply_form" action="/club/reply/add?link=${link}&id=${replyId}&token=${token}" method="post">

        <div class="markdown_editor in_editor">
            <div class="markdown_in_editor">
                <textarea class="editor" name="content" rows="8">@${author}</textarea>

                <div class="editor_buttons">
                    <input class="span-primary submit_btn" type="submit" value="回复">
                </div>
            </div>

        </div>
        <input type="hidden" name="topic_id" value="${topicId}">
    </form>
    `
    replyCell.insertAdjacentHTML('beforeend', inputItem)
}

var bindEventReplyInput = function() {
    var b = e('.reply_list')
    b.addEventListener('click', function(event) {
        var self = event.target
        var replyCell = self.closest('.cell')
        var replyId = replyCell.dataset['id']
        if (self.classList.contains('active')) {
            var inputItem = e('.markdown_editor', replyCell)
            inputItem.remove()
            self.classList.remove('active')
        } else if (self.classList.contains('reply_input')) {
            var inputTopicId = e('#topic_id')
            var inputLink = e('#_link')
            var inputToken = e('#_csrf')
            var topicId = inputTopicId.value
            var link = inputLink.value
            var token = inputToken.value
            self.classList.add('active')
            insertReplyInput(replyCell, token, link, replyId, topicId)
        }
    })
}

bindEventReplyInput()
