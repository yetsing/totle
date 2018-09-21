var log = console.log.bind(console)

var e = function(selector, parent=document) {
    return parent.querySelector(selector)
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
            log('load ajax response', r.response, typeof(r.response))
            var json = JSON.parse(r.response)
            if (json.done == 'false') {
                alert(json.message)
            } else {
                responseCallback(json)
            }

        }
    }
    // 把数据转换为 json 格式字符串
    data = JSON.stringify(data)
    // 发送请求
    r.send(data)
}

var fromNow = function(time) {
    var now = Math.floor(new Date() / 1000)
    var delta = now - time
    if (delta < 60) {
        second = delta
        return `${second} 秒前`
    } else if (delta < 3600) {
        minute = Math.floor(delta / 60)
        return `${minute} 分钟前`
    } else if (delta < 86400) {
        hour = Math.floor(delta / 3600)
        return `${hour} 小时前`
    } else if (delta < 2592000) {
        day = Math.floor(delta / 86400)
        return `${day} 天前`
    } else if (delta < 933120000) {
        month = Math.floor(delta / 2592000)
        return `${month} 个月前`
    } else {
        year = Math.floor(delta / 933120000)
        return `${year} 年前`
    }
}
