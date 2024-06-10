$(async function () {
    var opt = dgSetting1({
        url: '/api/getAllFolders',
        cols: [
            {
                field: 'name', title: '名称', width: 100, formatter(value, row, index) {
                    var p = encodeURIComponent(row.path)
                    return `<a href="/view?path=${p}">${value}</a>`
                }
            },
            {field: 'path', title: '路径', width: 100},
        ],
        onLoadSuccess: function (data) {
            console.log(data)
            $('#dg').datagrid('enableFilter', [{
                field: 'name',
                type: 'text',
                options: {
                    precision: 2
                }
            }]);
        }
    })
    $('#dg').datagrid(opt)
})
