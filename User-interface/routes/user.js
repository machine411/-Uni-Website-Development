const express = require('express')
const router = express.Router()
const sql = require('../config/mysql')
const { msg, reg } = require('../utils/utils')


// Login socket
router.post('/login', (req, res) => {
    if (req.body.username && req.body.password) {
        if (reg.test(req.body.username)) {
            if (req.body.password.length >= 6 && req.body.password.length < 16) {
                sql.query(`SELECT * FROM users WHERE username="${req.body.username}"`, (err, result, fields) => {
                    if (err) throw err;
                    if (!result.length)
                        return msg(res, -1, 'User is not exist, please signup first', {}, 200)
                    else {
                        sql.query(`SELECT * FROM users WHERE password="${req.body.password}"`, (err, result, fields) => {
                            if (err) throw err;
                            if (!result.length) {
                                return msg(res, -1, 'Incorrect Username or Password ', {}, 200)
                            } else {
                                msg(res, 0, 'Login success', {}, 200)
                            
                                // req.session.username = req.body.username
                                // req.session.isLogin = true
                            }
                        })
                    }
                })
            } else
                msg(res, -1, 'Please enter a password greater than 6 digits and less than 16 digits', {}, 200)
        } else
            msg(res, -1, 'The format of mailbox is incorrect, please re-enter', {}, 200)
    } else
        msg(res, -1, 'Username or password cannot be empty', {}, 200)
});



// Register socket
router.post('/register', (req, res) => {
    if (req.body.username && req.body.password && req.body.password2) {
        if (reg.test(req.body.username)) {
            if ((req.body.password.length >= 6 && req.body.password.length < 16) && (req.body.password2.length >= 6 && req.body.password2.length < 16)) {
                if (req.body.password == req.body.password2) {
                    sql.query(`SELECT * FROM users WHERE username="${req.body.username}"`, (err, result, fields) => {
                        if (err) throw err;
                        if (result.length)
                            return msg(res, -1, 'This user already exists, please log in!!', {}, 200)
                        else {
                            delete req.body.password2
                            sql.query(`INSERT INTO users SET ?`, req.body, (err, result, fields) => {
                                if (err) throw err;
                                return msg(res, 0, 'registration success', req.body, 200)
                            })
                        }
                    })
                } else
                    msg(res, -1, 'Two passwords are inconsistent', {}, 200)
            } else 
                msg(res, -1, 'Password length must be greater than 6 and less than 16 digits', {}, 200)
        } else
            msg(res, -1, 'The format of mailbox is incorrect, please re-enter', {}, 200)
    } else
        msg(res, -1, 'Username or password cannot be empty', {}, 200)
});

// sign out
router.post('/logout', (req, res) => {
    req.session.username = null; // delete session
    req.session.isLogin = false; // delete session
    req.session.destroy(err => {
        msg(res, 0, 'sign out', {}, 200)
    });
})

module.exports = router