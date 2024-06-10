// 获取图片容器
var container = document.getElementById('imageContainer');

// 循环创建并添加图片元素
var pageNo = 1
var pageSizeArr = [50, 100, 200, 300, 400, 500]
var pageSize = pageSizeArr[0]

// 图片总数
var imgMaxCount = 99999
// 最大页数
var maxPageNo = 200

// 获取图片父路径
var imgParentPath = ''
$(async function () {
    var query = parseQuery(location.search)
    var info = await xhr({
        url: '/api/mangaDetail',
        data: {path: query.path}
    })
    onMaxCountChange(info.total)
    imgParentPath = info.imgParentPath

    // 渲染分页选择器
    renderPageSelector()
    // 渲染图片
    renderImg()
    // 每页显示图片数量的选择器,select元素
    renderPageSizeSelector()
    // 键盘翻页事件
    attachPageEvent()
})

function onMaxCountChange(total) {
// 图片总数
    imgMaxCount = total || 99999
// 最大页数
    maxPageNo = Math.ceil(imgMaxCount / pageSize)
}


function getMaxCount() {
    try {
        var arr = location.pathname.split("/")
        var folder = arr[arr.length - 2]
        // unescape解码
        var folderName = decodeURIComponent(folder)
        console.log(folderName)
        var v = imageCount[folderName] || 8000
        console.log(`folderName: ${folderName}, imageCount: ${v}`)
        return v
    } catch (e) {
        console.log(e)
        return 8000
    }
}

/**
 * 渲染分页选择器.select元素, 用1->maxPageNo,步长=1
 */
function renderPageSelector() {
    var select = document.getElementById('pageSelector')
    select.innerHTML = ''
    for (var i = 1; i <= maxPageNo; i++) {
        var option = document.createElement('option')
        option.value = i
        option.innerText = i
        select.appendChild(option)
    }
}

/**
 * 加载&渲染图片
 */
function renderImg() {
    container.innerHTML = ''
    var startNo = (pageNo - 1) * pageSize
    var endNo = Math.min(imgMaxCount - 1, (startNo + pageSize))
    for (var i = startNo + 1; i <= endNo; i++) {
        var imageNumber = i.toString().padStart(5, '0');
        var imageUrl = `/imgs/${imgParentPath}/Image${imageNumber}.jpg`
        var img = document.createElement('img');
        img.src = imageUrl;
        img.width = 350;
        container.appendChild(img);
    }

    // 页面scroll到顶部
    container.scrollTop = 0

    document.getElementById('pageSelector').value = pageNo
    document.getElementById('currTxt').innerText = '当前页：' + pageNo + ' / ' + maxPageNo
}

// 每页显示图片数量的选择器,select元素
function renderPageSizeSelector() {
    var select = document.getElementById('pageSizeSelector')
    for (var i = 0; i < pageSizeArr.length; i++) {
        var option = document.createElement('option')
        option.value = pageSizeArr[i]
        option.innerText = pageSizeArr[i]
        select.appendChild(option)
    }
}


function attachPageEvent() {
    document.onkeydown = function (e) {
        console.log(e)
        switch (e.code) {
            // 左键向前翻页
            case 'ArrowLeft': {
                clickprev()
                break;
            }
            // 右键向后翻页
            case 'ArrowRight': {
                clicknext()
                break;
            }
        }
    }
}

function clickfirst() {
    pageNo = 1
    renderImg()
}

function clicklast() {
    pageNo = maxPageNo
    renderImg()
}

function clickprev() {
    pageNo--
    if (pageNo > 0) {
        renderImg()
    }
}

function clicknext() {
    pageNo++
    if (pageNo <= maxPageNo) {
        renderImg()
    }
}

// 点击按钮，回到顶部
function clickToTop() {
    container.scrollTop = 0
}

function pageSizeChange() {
    pageSize = document.getElementById('pageSizeSelector').value
    pageNo = 1
    maxPageNo = Math.ceil(imgMaxCount / pageSize)
    renderPageSelector()
    renderImg()
}

// 加载滚动条
function loadNicescroll() {
    $(".div1").niceScroll({
        cursoropacitymin: 1, // change opacity when cursor is inactive (scrollabar "hidden" state), range from 1 to 0
        cursoropacitymax: 1, // change opacity when cursor is active (scrollabar "visible" state), range from 1 to 0
        cursorwidth: "30px", // cursor width in pixel (you can also write "5px")
        cursorminheight: 50, // set the minimum cursor height (pixel)
        scrollspeed: 1, // speed of selection when dragged with cursor
        cursordragontouch: true,
        cursorfixedheight: false, // set fixed height for cursor in pixel
    });
}