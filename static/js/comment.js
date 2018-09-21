var apiWeiboCommentAll = function(weiboId, callback) {
    var path = `/weibo/comment/all?weibo_id=${weiboId}`
    ajax('GET', path, '', callback)
}

var apiWeiboCommentAdd = function(form, callback) {
    var path = '/weibo/comment/add'
    ajax('POST', path, form, callback)
}

var apiWeiboCommentDelete = function(commentId, callback) {
    var path = `/weibo/comment/delete?id=${commentId}`
    ajax('GET', path, '', callback)
}

var apiWeiboCommentUpdate = function(form, callback) {
    var path = '/weibo/comment/update'
    ajax('POST', path, form, callback)
}

var commentTemplate = function(comment, username) {
    created_time = fromNow(comment.created_time)
    var button = ''
    if (username == comment.username) {
        var button = `
        <a href="javascript:void(0);" class="weibo-comment-delete" style="font-size: xx-small">删除</a>
        `
    }
    var t = `
        <div class="weibo-comment-cell" data-id="${comment.id}">
            <div style="margin-left: 12px; margin-bottom: 10px;">
                <span style="color: rgb(61, 146, 201); font-weight: bolder;">${comment.username}</span>
                ${button}
                <span style="float: right; color: #8590a6; margin-right: 10px;">${created_time}</span>
            </div>
            <div style="margin-left: 12px;">
                ${comment.content}
            </div>
            <h1 class="content-subhead update-form"> </h1>
        </div>
    `
    return t
}

var weiboCommentUpdateTemplate = function(content) {
    var t = `
        <div class="weibo-comment-update-form">
            <input class="weibo-comment-update-input" value="${content}">
            <button class="weibo-comment-update">更新</button>
        </div>
    `
    return t
}

var insertWeiboComment = function(comment, username, weiboCommentList) {
    var commentCell = commentTemplate(comment, username)
    weiboCommentList.insertAdjacentHTML('afterbegin', commentCell)
}

var insertWeiboCommentList = function(weiboCommentList, weiboCell) {
    var weiboComments = `
    <div class="weibo-comment-list">
        ${weiboCommentList}
        <div class="weibo-comment-add-form pure-form" style="margin: 10px;">
            <input class="weibo-comment-input" placeholder="写下你的评论..." style="width: 80%; height: 30px;">
            <button class="weibo-comment-add pure-button pure-button-primary">评论</button>
        </div>
    </div>
    `
    weiboCell.insertAdjacentHTML('beforeend', weiboComments)
}

var insertCommentUpdateForm = function(content, weiboCommentCell) {
    var updateForm = weiboCommentUpdateTemplate(content)
    weiboCommentCell.insertAdjacentHTML('beforeend', updateForm)
}

var bindEventWeiboCommentAll = function() {
    var weiboList = e('#id-weibo-list')
    weiboList.addEventListener('click', function(event) {
        log(event)
        var self = event.target
        log('被点击的元素', self)
        log(self.classList)
        if (self.classList.contains('active')) {
            self.classList.remove('active')
            var weiboCell = self.closest('.weibo-cell')
            var weiboCommentList = e('.weibo-comment-list')
            weiboCommentList.remove()
        } else if (self.classList.contains('weibo-comment-all')) {
            log('显示该 weibo 的所有评论')
            self.classList.add('active')
            var weiboCell = self.closest('.weibo-cell')
            var weiboId = weiboCell.dataset['id']
            apiWeiboCommentAll(weiboId, function(comments) {
                log('load this weibo commnets', comments)
                // 循环添加到页面中
                var username = comments.pop(-1).username
                var weiboCommentList = ''
                for(var i = 0; i < comments.length; i++) {
                    var comment = comments[i]
                    weiboCommentList += commentTemplate(comment, username)
                }
                insertWeiboCommentList(weiboCommentList, weiboCell)
            })
        }
    })
}


var bindEventWeiboCommentAdd = function() {
    var weiboList = e('#id-weibo-list')
    // 事件响应函数会传入一个参数 就是事件本身
    weiboList.addEventListener('click', function(event) {
        log(event)
        // 我们可以通过 event.target 来得到被点击的对象
        var self = event.target
        log('被点击的元素', self)
        // 通过比较被点击元素的 class
        // 来判断元素是否是我们想要的
        // classList 属性保存了元素所有的 class
        log(self.classList)
        if (self.classList.contains('weibo-comment-add')) {
            log('点到了添加评论按钮')
            weiboCell = self.closest('.weibo-cell')
            weiboId = weiboCell.dataset['id']
            var weiboCommentList = e('.weibo-comment-list', weiboCell)
            var input = e('.weibo-comment-input', weiboCell)
            var content = input.value
            log('添加评论', content)
            var form = {
                weibo_id: weiboId,
                content: content,
            }
            apiWeiboCommentAdd(form, function(comment) {
                // 收到返回的数据, 插入到页面中
                insertWeiboComment(comment, comment.username, weiboCommentList)
                input.value = ''
                weiboCommentCount = e('.weibo-comment-count', weiboCell)
                var count = Number(weiboCommentCount.innerText) + 1
                weiboCommentCount.innerText = count
            })
        } else {
            log('点到了 weibo cell')
        }
    })
}

var bindEventWeiboCommentDelete = function() {
    var weiboList = e('#id-weibo-list')
    // 事件响应函数会传入一个参数 就是事件本身
    weiboList.addEventListener('click', function(event) {
        log(event)
        // 我们可以通过 event.target 来得到被点击的对象
        var self = event.target
        log('被点击的元素', self)
        // 通过比较被点击元素的 class
        // 来判断元素是否是我们想要的
        // classList 属性保存了元素所有的 class
        log(self.classList)
        if (self.classList.contains('weibo-comment-delete')) {
            log('点到了 comment 删除按钮')
            weiboCommentCell = self.closest('.weibo-comment-cell')
            commentId = weiboCommentCell.dataset['id']
            apiWeiboCommentDelete(commentId, function(r) {
                log('apiWeiboCommentDelete', r.message)
                weiboCell = self.closest('.weibo-cell')
                weiboCommentCell.remove()
                weiboCommentCount = e('.weibo-comment-count', weiboCell)
                var count = Number(weiboCommentCount.innerText) - 1
                weiboCommentCount.innerText = count
                alert(r.message)
            })
        } else {
            log('点到了 weibo cell')
        }
    })
}

var bindEventWeiboCommentEdit = function() {
    var weiboList = e('#id-weibo-list')
    // 事件响应函数会传入一个参数 就是事件本身
    weiboList.addEventListener('click', function(event) {
        log(event)
        // 我们可以通过 event.target 来得到被点击的对象
        var self = event.target
        log('被点击的元素', self)
        // 通过比较被点击元素的 class
        // 来判断元素是否是我们想要的
        // classList 属性保存了元素所有的 class
        log(self.classList)
        if (self.classList.contains('weibo-comment-edit')) {
            log('点到了 comment 编辑按钮')
            weiboCommentCell = self.closest('.weibo-comment-cell')
            commentId = weiboCommentCell.dataset['id']
            var commentSpan = e('.weibo-comment-content', weiboCommentCell)
            var content = commentSpan.innerText
            // 插入编辑输入框
            insertCommentUpdateForm(content, weiboCommentCell)
        } else {
            log('点到了 weibo cell')
        }
    })
}

var bindEventWeiboCommentUpdate = function() {
    var weiboList = e('#id-weibo-list')
    // 事件响应函数会传入一个参数 就是事件本身
    weiboList.addEventListener('click', function(event) {
        log(event)
        // 我们可以通过 event.target 来得到被点击的对象
        var self = event.target
        log('被点击的元素', self)
        // 通过比较被点击元素的 class
        // 来判断元素是否是我们想要的
        // classList 属性保存了元素所有的 class
        log(self.classList)
        if (self.classList.contains('weibo-comment-update')) {
            log('点到了 comment 更新按钮')
            weiboCommentCell = self.closest('.weibo-comment-cell')
            commentId = weiboCommentCell.dataset['id']
            log('update weibo comment id', commentId)
            input = e('.weibo-comment-update-input', weiboCommentCell)
            content = input.value
            var form = {
                id: commentId,
                content: content,
            }

            apiWeiboCommentUpdate(form, function(comment) {
                // 收到返回的数据, 插入到页面中
                log('apiWeiboCommentUpdate', comment)

                var commentSpan = e('.weibo-comment-content', weiboCommentCell)
                commentSpan.innerText = comment.content

                var updateForm = e('.weibo-comment-update-form', weiboCommentCell)
                updateForm.remove()
            })
        } else {
            log('点到了 weibo cell')
        }
    })
}

var __main = function() {
    bindEventWeiboCommentAll()
    bindEventWeiboCommentAdd()
    bindEventWeiboCommentDelete()
    bindEventWeiboCommentEdit()
    bindEventWeiboCommentUpdate()
}

__main()
