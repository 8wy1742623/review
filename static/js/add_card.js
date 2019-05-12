// 功能一：显示时间
// fixme 浏览器读取这个文件后，显示乱码。
var show_date = function() {
    // 获取 p#show_date
    p_date = e('#show_date')
    // 获取本地日期
    var date = new Date()
    date_str = date.toLocaleDateString()
    // 文本内容替换为日期
    p_date.innerText = date_str
}

var __main = function() {
    show_date()
}

$(document).ready(function() {
    __main()
})
