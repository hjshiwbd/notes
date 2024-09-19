// ref: https://wiki.metacubex.one/
// 功能说明,添加负载均衡代理组,且去掉部分节点(比如日本节点,它虽然速度快,但是Google由此会出现日语搜索结果,看不懂)
// 附录1: 负载均衡load-balance和自动选择url-test都是clash内置的策略, 区别: 自动同一时间里只用一个,挂了换下一个.且有日本节点; 负载均衡会同时使用多个节点, 由本文件代码控制逻辑, 不使用日本节点

var clog = console.log

//参数配置
var params = {
  'ss': { //订阅profileName的名字
    srcGroup: 'Auto', //复制原有代理组name
    destGroup: '!负载均衡', //复制后新代理组name
    destGroupType: 'load-balance', //复制后新代理组type
    baseGroup: 'Proxy', //基础group,需要手动选择的那个,
    proxiesFilters: [{ //过滤器
      type: 'wildcard', // 通配符匹配,满足value格式的都会被过滤掉
      value: '*japan*'
    }]
  },
  '紫鸟': {
    srcGroup: '自动选择', //复制原有代理组name
    destGroup: '!负载均衡', //复制后新代理组name
    destGroupType: 'load-balance', //复制后新代理组type
    baseGroup: '紫鸟', //基础group,需要手动选择的那个
    proxiesFilters: [{
      type: 'wildcard',
      value: '*日本*'
    }]
  }
}

function main(config, profileName) {
  if (params[profileName]) {
    runFor(config, params[profileName])
  }

  return config;
}

function runFor(config, configParam) {
  var auto = config['proxy-groups'].find(o => o.name == configParam.srcGroup)
  var newGroup = JSON.parse(JSON.stringify(auto)) // deepcopy一份得到新代理组
  newGroup.name = configParam.destGroup // 设置名字
  newGroup.type = configParam.destGroupType //设置type

  // 过滤节点
  let filterResult = []
  configParam.proxiesFilters.forEach(filter => {
    let toBeFilter = filterResult.length > 0 ? filterResult : newGroup.proxies
    if (filter.type == 'wildcard') {
      filterResult = toBeFilter.filter(name => !wildcardMatch(name.toLowerCase(), filter.value.toLowerCase())) // 过滤不要的节点1
    }
  })
  newGroup.proxies = filterResult //设置节点
  config['proxy-groups'].push(newGroup) //新增代理组

  // 把新代理组,加到手动选择中以供使用
  var proxy = config['proxy-groups'].find(o => o.name == configParam.baseGroup)
  proxy.proxies.unshift(configParam.destGroup)

}

// 通配符匹配, '*Japan*'匹配'asrgaw-Japan-asdfasd'
function wildcardMatch(src, pattern) {
  // Escape all regex special characters except for ? and *
  const escapedPattern = pattern.replace(/([.+^=!:${}()|\[\]\/\\])/g, '\\$1')
    .replace(/\?/g, '.')
    .replace(/\*/g, '.*');

  // Create the RegExp object
  const regex = new RegExp(`^${escapedPattern}$`);

  // Test the source string against the pattern
  return regex.test(src);
}