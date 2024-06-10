$(function () {
    $.ajaxSetup({
        cache: false,
        // complete(resData, textStatus, jqXHR) {
        //     console.log('setup', resData, textStatus, jqXHR)
        // }
    })
})

/**
 * jquery ajax
 * @param url
 * @param type
 * @param data
 * @returns {Promise<unknown>}
 */
function xhr({url, type = 'POST', data} = option) {
    return new Promise((resolve, reject) => {
        $.ajax({
            url: url,
            type: type,
            data: data,
            success: function (resData, textStatus, jqXHR) {
                console.log(url, resData)
                if (jqXHR.status == 200 && resData.code == 200) {
                    resolve(resData.data);
                } else {
                    reject(resData.msg)
                }
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                console.log(errorThrown)
                reject(XMLHttpRequest);
            }
        });
    })
}

/**
 * 解析query
 * @param queryString
 * @returns {{}}
 */
function parseQuery(queryString) {
    var query = {};
    var pairs = (queryString[0] === '?' ? queryString.substr(1) : queryString).split('&');
    for (var i = 0; i < pairs.length; i++) {
        var pair = pairs[i].split('=');
        query[decodeURIComponent(pair[0])] = decodeURIComponent(pair[1] || '');
    }
    return query;
}