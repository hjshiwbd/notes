const clog = console.log;

for (let i = 0; i < 10; i++) {
    var len = 32;
    const a = generateCode(len, {
        hasSymbol: 0,
        hasChar: 1,
        hasNum: 1,
    })
    clog(a)
}

/**
 * 生成密码字符串
 * 33~47：!~/
 * 48~57：0~9
 * 58~64：:~@
 * 65~90：A~Z
 * 91~96：[~`
 * 97~122：a~z
 * 123~127：{~
 * @param length 长度
 * @param hasNum 是否包含数字 1-包含 0-不包含
 * @param hasChar 是否包含字母 1-包含 0-不包含
 * @param hasSymbol 是否包含其他符号 1-包含 0-不包含   "~!@#$%^&*()_";
 */
function generateCode(length, {
    hasNum = 1,
    hasChar = 1,
    hasSymbol = 1
} = {}) {
    var m = "";
    if (hasNum == "0" && hasChar == "0" && hasSymbol == "0") return m;
    for (var i = length - 1; i >= 0; i--) {
        var num = Math.floor((Math.random() * 94) + 33);
        if (
            (
                (hasNum == "0") && ((num >= 48) && (num <= 57))
            ) || (
                (hasChar == "0") && ((
                    (num >= 65) && (num <= 90)
                ) || (
                    (num >= 97) && (num <= 122)
                ))
            ) || (
                (hasSymbol == "0") && ((
                    (num >= 33) && (num <= 47)
                ) || (
                    (num >= 58) && (num <= 64)
                ) || (
                    (num >= 91) && (num <= 96)
                ) || (
                    (num >= 123) && (num <= 127)
                ))
            )
        ) {
            i++;
            continue;
        }
        m += String.fromCharCode(num);
    }
    return m;
}