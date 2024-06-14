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

var isImgLazy = getImgLazy()

// 获取图片父路径
var imgParentPath = ''

function onLoad() {
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
        // 懒加载开关文字
        renderLazySwitch()
        // 图片懒加载, 加载首屏的图片
        loadLazyImages()
    })
}

function onMaxCountChange(total) {
// 图片总数
    imgMaxCount = total || 99999
// 最大页数
    maxPageNo = Math.ceil(imgMaxCount / pageSize)
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


// 检查元素是否在视口中
function isInViewport(element) {
    var rect = element.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
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
        img.width = 350;
        if (isImgLazy) {
            img.src = '/static/img/blank.png';
            img.className = 'lazy'
            img.setAttribute('data-src', imageUrl)
        } else {
            img.src = imageUrl;
        }

        container.appendChild(img);
    }

    // 页面scroll到顶部
    container.scrollTop = 0

    document.getElementById('pageSelector').value = pageNo
    document.getElementById('currTxt').innerText = '当前页：' + pageNo + ' / ' + maxPageNo
}

function loadLazyImages() {
    if (!isImgLazy) {
        // 懒加载关闭
        return
    }
    // 获取所有需要懒加载的图片
    var lazyImages = [].slice.call(document.querySelectorAll("img.lazy"));
    lazyImages.forEach(function (img) {
        if (isInViewport(img)) {
            img.src = img.dataset.src;
            img.classList.remove('lazy'); // 可选：移除lazy类以进行样式更改或性能优化
        }
    });
}

// jquery监听页面滚动事件
$('#imageContainer').scroll(function () {
    loadLazyImages();
});


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
    if (pageNo < maxPageNo) {
        renderImg()
    }
}

// 点击按钮，回到顶部
function clickToTop() {
    container.scrollTop = 0
}

function pageSizeChange() {
    pageSize = document.getElementById('pageSizeSelector').value
    pageSize = parseInt(pageSize, 10)
    pageNo = 1
    maxPageNo = Math.ceil(imgMaxCount / pageSize)
    renderPageSelector()
    renderImg()
}

// 懒加载开关文字
function renderLazySwitch() {
    var lazySwitch = document.getElementById('imgLazySwitch')
    if (isImgLazy == true) {
        lazySwitch.innerText = '懒开'
    } else {
        lazySwitch.innerText = '懒关'
    }
}

// 懒加载打开关闭
function onImgLazySwichClick() {
    isImgLazy = !isImgLazy
    setImgLazy(isImgLazy)
    location.reload()
}

// 页面初始化
onLoad()