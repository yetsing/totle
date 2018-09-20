var log = console.log.bind(console)

var e = function (sel, parent=document) {
    return parent.querySelector(sel)
}

var es = function (sel) {
    return document.querySelectorAll(sel)
}

/*
 ajax 函数
*/
var ajax = function(method, path, data, responseCallback) {
    var r = new XMLHttpRequest()
    // 设置请求方法和请求地址
    r.open(method, path, true)
    // 设置发送的数据的格式为 application/json
    r.setRequestHeader('Content-Type', 'application/json')
    // 注册响应函数
    r.onreadystatechange = function() {
        if (r.readyState === 4) {
            // r.response 存的就是服务器发过来的放在 HTTP BODY 中的数据
            var json = JSON.parse(r.response)
            responseCallback()
        }
    }
    // 把数据转换为 json 格式字符串
    data = JSON.stringify(data)
    // 发送请求
    r.send(data)
}

var apiCollect = function(topicId, callback) {
    var path = `/club/collect/${topicId}`
    ajax('GET', path, '', callback)
}

var apiDelCollect = function(topicId, callback) {
    var path = `/club/del_collect/${topicId}`
    ajax('GET', path, '', callback)
}

var bindEventCollect = function() {
    var b = e('.collect_btn')
    b.addEventListener('click', function(event) {
        var self = event.target
        var topicId = self.dataset['id']
        if (self.classList.contains('span-success')) {
            log('collect')
            apiCollect(topicId, function() {
                self.classList.remove('span-success')
                self.value = '取消收藏'
            })
        }
    })
}

var bindEventDelCollect = function() {
    var b = e('.collect_btn')
    b.addEventListener('click', function(event) {
        var self = event.target
        var topicId = self.dataset['id']
        if (!self.classList.contains('span-success')) {
            log('del_collect')
            apiDelCollect(topicId, function() {
                self.classList.add('span-success')
                self.value = '收藏'
            })
        }
    })
}

var bindEvent = function() {
    bindEventCollect()
    bindEventDelCollect()
}

bindEvent()
