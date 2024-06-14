function lsSet(key, value) {
    if (value == null) {
        throw new Error("lsSet: value is null");
    }
    localStorage.setItem(key, JSON.stringify(value));
}

function lsGet(key, fallback = null) {
    var v = localStorage.getItem(key);
    if (v) {
        return JSON.parse(v);
    } else {
        return fallback;
    }
}

function setImgLazy(v) {
    lsSet('imgLazy', v)
}

function getImgLazy() {
    return lsGet('imgLazy', true)
}