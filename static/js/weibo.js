// WEIBO API
// 获取所有 weibo
var apiWeiboAll = function(callback) {
    var path = '/weibo/all'
    ajax('GET', path, '', callback)
}

var apiWeiboAdd = function(form, callback) {
    var path = '/weibo/add'
    ajax('POST', path, form, callback)
}

var apiWeiboDelete = function(weiboId, callback) {
    var path = `/weibo/delete?id=${weiboId}`
    ajax('GET', path, '', callback)
}

var apiWeiboUpdate = function(form, callback) {
    var path = '/weibo/update'
    ajax('POST', path, form, callback)
}

var weiboTemplate = function(weibo, username) {
    var created_time = fromNow(weibo.created_time)
    var button = ''
    if (username == weibo.username) {
        var button = `
        <a href="javascript:void(0);" class="weibo-delete" style="font-size: smaller">删除</a>
        <a href="javascript:void(0);" class="weibo-edit" style="font-size: smaller">编辑</a>
        `
    }

    var t = `
        <section class="post weibo-cell" data-id="${weibo.id}">
            <header class="post-header">
                <img width="48" height="48" alt="${weibo.username}" class="post-avatar" src="/static/images/default.jpg">
                <p class="post-meta">
                    <a href="javascript:void(0);" class="post-author" style="font-size: large; font-weight: bolder;">${weibo.username}</a>
                     · 创建于
                    <a href="javascript:void(0);" style="color: #8590a6;">
                        ${created_time}
                    </a>
                    ${button}
                </p>
            </header>
            <div class="post-description">
                <p class="weibo-content">${weibo.content}</p>
            </div>
            <div>
                <a href="javascript:void(0);" class="weibo-comment-all">
                    <span class="weibo-comment-count">${weibo.comment_count}</span>
                    条评论
                </a>
                <span class="weibo-updated-time">编辑于 ${weibo.updated_time}</span>
            </div>
        </section>
        <h1 id="id-line-${weibo.id}" class="content-subhead update-form"> </h1>
    `
    return t
}

var weiboUpdateTemplate = function(content) {
    var t = `
        <div class="weibo-update-form pure-form pure-form-stacked">
            <textarea class="weibo-update-input" rows="5" style="width: 100%">${content}</textarea>
            <button class="weibo-update pure-button pure-button-primary">更新</button>
        </div>
    `
    return t
}

var insertWeibo = function(weibo, username) {
    var weiboCell = weiboTemplate(weibo, username)
    // 插入 weibo-list
    var weiboList = e('#id-weibo-list')
    weiboList.insertAdjacentHTML('afterbegin', weiboCell)
}

var insertUpdateForm = function(content, weiboCell) {
    var updateForm = weiboUpdateTemplate(content)
    weiboCell.insertAdjacentHTML('beforeend', updateForm)
}

var loadWeibos = function() {
    apiWeiboAll(function(weibos) {
        log('load all weibos', weibos)
        // 循环添加到页面中
        var username = weibos.pop(-1).username
        for(var i = 0; i < weibos.length; i++) {
            var weibo = weibos[i]
            insertWeibo(weibo, username)
        }
    })
}

var bindEventWeiboAdd = function() {
    var b = e('#id-button-add')
    // 注意, 第二个参数可以直接给出定义函数
    b.addEventListener('click', function() {
        var input = e('#id-input-weibo')
        var content = input.value
        log('click add', content)
        var form = {
            content: content,
        }
        apiWeiboAdd(form, function(weibo) {
            // 收到返回的数据, 插入到页面中
            insertWeibo(weibo, weibo.username)
            input.value = ''
        })
    })
}


var bindEventWeiboDelete = function() {
    var weiboList = e('#id-weibo-list')
    // 事件响应函数会传入一个参数 就是事件本身
    weiboList.addEventListener('click', function(event) {
        log(event)
        // 我们可以通过 event.target 来得到被点击的对象
        var self = event.target
        // 通过比较被点击元素的 class
        // 来判断元素是否是我们想要的
        // classList 属性保存了元素所有的 class
        log(self.classList)
        if (self.classList.contains('weibo-delete')) {
            log('点到了删除按钮')
            weiboCell = self.closest('.weibo-cell')
            weiboId = weiboCell.dataset['id']
            apiWeiboDelete(weiboId, function(r) {
                log('apiWeiboDelete', r.message)
                var line = e(`#id-line-${weiboId}`)
                weiboCell.remove()
                line.remove()
                alert(r.message)
            })
        }
    })
}

var bindEventWeiboEdit = function() {
    var weiboList = e('#id-weibo-list')
    // 事件响应函数会传入一个参数 就是事件本身
    weiboList.addEventListener('click', function(event) {
        log(event)
        // 我们可以通过 event.target 来得到被点击的对象
        var self = event.target
        // 通过比较被点击元素的 class
        // 来判断元素是否是我们想要的
        // classList 属性保存了元素所有的 class
        log(self.classList, typeof(self.classList))
        if (self.classList.contains('weibo-active')) {
            self.classList.remove('weibo-active')
            var weiboCell = self.closest('.weibo-cell')
            var weiboUpdateForm = e('.weibo-update-form', weiboCell)
            weiboUpdateForm.remove()
        } else if(self.classList.contains('weibo-edit')) {
            log('点到了编辑按钮')
            self.classList.add('weibo-active')
            weiboCell = self.closest('.weibo-cell')
            weiboId = weiboCell.dataset['id']
            postDescription = e('.post-description', weiboCell)
            // weiboCommentList = e('.weibo-comment-list', weiboCell)
            var weiboSpan = e('.weibo-content', weiboCell)
            var content = weiboSpan.innerText
            // 插入编辑输入框
            insertUpdateForm(content, postDescription)
        }
    })
}

var bindEventWeiboUpdate = function() {
    var weiboList = e('#id-weibo-list')
    // 事件响应函数会传入一个参数 就是事件本身
    weiboList.addEventListener('click', function(event) {
        log(event)
        // 我们可以通过 event.target 来得到被点击的对象
        var self = event.target
        // 通过比较被点击元素的 class
        // 来判断元素是否是我们想要的
        // classList 属性保存了元素所有的 class
        log(self.classList)
        if (self.classList.contains('weibo-update')) {
            log('点到了更新按钮')
            weiboCell = self.closest('.weibo-cell')
            weiboId = weiboCell.dataset['id']
            log('update weibo id', weiboId)
            input = e('.weibo-update-input', weiboCell)
            content = input.value
            var form = {
                id: weiboId,
                content: content,
            }

            apiWeiboUpdate(form, function(weibo) {
                // 收到返回的数据, 插入到页面中
                log('apiWeiboUpdate', weibo)

                var weiboSpan = e('.weibo-content', weiboCell)
                weiboSpan.innerText = weibo.content

                var updateForm = e('.weibo-update-form', weiboCell)
                updateForm.remove()
                editButton = e('.weibo-edit', weiboCell)
                editButton.classList.remove('active')
            })
        }
    })
}


var bindEvents = function() {
    bindEventWeiboAdd()
    bindEventWeiboDelete()
    bindEventWeiboEdit()
    bindEventWeiboUpdate()
}

var __main = function() {
    bindEvents()
    loadWeibos()
}

__main()
