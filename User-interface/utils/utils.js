// resopons config
const msg = (res, code, msg, data, status) => {
    return res.status(status).json({ code, msg, data, status })
}

const reg = /^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/

module.exports = {
    msg,
    reg
}