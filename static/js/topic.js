var markContents = function () {
    var contentDivs = es('.markdown-text')
    for (var i = 0; i < contentDivs.length; i++) {
        var contentDiv = contentDivs[i]
        var content = marked(contentDiv.textContent)
        contentDiv.innerHTML = content
    }
}

var highlight = function () {
    var code_list = es('pre code')
    for (var i = 0; i < code_list.length; i++) {
        var code = code_list[i]
        code.className = code.className.replace('lang', 'language')
    }
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

var registerTimer = function () {
    setInterval(function () {
        var times = es('.reply-time')
        for (var i = 0; i < times.length; i++) {
            var t = times[i]
            var time = Number(t.id)
            var s = fromNow(time)
            t.innerText = s
        }
    }, 1000)
}

var __main = function () {
    markContents()
    registerTimer()
    highlight()
}

__main()
