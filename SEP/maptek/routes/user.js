const express = require('express')
const router = express.Router()
const sql = require('../config/mysql')
const { msg, reg } = require('../utils/utils')
const fs = require('fs');
var checker = {username : 0}

// const user_info = {user_username : "default"}
// var { current_user } = require('./userinfo');
// export { user_info };

// Login socket
router.post('/login', (req, res) => {
    if (req.body.email && req.body.password) {
        if (reg.test(req.body.email)) {
            if (req.body.password.length >= 6 && req.body.password.length < 16) {
                sql.query(`SELECT * FROM users WHERE email="${req.body.email}"`, (err, result, fields) => {
                    if (err) {console.log(err)};
                    console.log(result)
                    if (!result.length)
                        msg(res, -1, 'User is not exist, please signup first', {}, 200)
                    else {
                        sql.query(`SELECT * FROM users WHERE email="${req.body.email}" and password="${req.body.password}"`, (err, result, fields) => {
                            if (err) {console.log(err)};
                            if (!result.length) {
                                return msg(res, -1, 'Incorrect email or Password ', {}, 200)
                            } else {
                                // current_user.user_username = req.body.email;
                                // require('./userinfo').username = result[0].username;
                                // console.log(req.session.username)
                                // console.log("----------------")

                                req.session.username = result[0].username
                                req.session.isLogin = true

                                return msg(res, 0, 'Login success', result[0], 200)
                            }
                        })
                    }
                })
            } else
                msg(res, -1, 'Please enter a password greater than 6 digits and less than 16 digits', {}, 200)
        } else
            msg(res, -1, 'The format of mailbox is incorrect, please re-enter', {}, 200)
    } else
      msg(res, -1, 'email or password cannot be empty', {}, 200)
});


// Register socket
router.post('/register', (req, res) => {
  sql.query(`SELECT * FROM users WHERE username="${req.body.username}"`, (err, result, fields) => {
      if (err) {console.log(err)};
      // console.log(req.body.username)
      // console.log(result.length)
      if (result.length){
        checker.username = 1
      }
  })
console.log("len:", checker.username)
console.log(req.body)
if (req.body.email && req.body.password && req.body.password2) {
    if (reg.test(req.body.email)) {

      sql.query(`SELECT * FROM users WHERE username="${req.body.username}"`, (err, result, fields) => {
          if (err) {console.log(err)};
          // console.log(req.body.username)
          // console.log(result.length)
          if (typeof result == "undefined"||!result.length){
            console.log("Username Not In Database")
            if ((req.body.password.length >= 6 && req.body.password.length < 16) && (req.body.password2.length >= 6 && req.body.password2.length < 16)) {
                if (req.body.password == req.body.password2) {
                    sql.query(`SELECT * FROM users WHERE email="${req.body.email}"`, (err, result, fields) => {
                        if (err) {console.log(err)};
                        if (result.length)
                            return msg(res, -1, 'This user already exists, please log in!!', {}, 200)
                        else {
                            delete req.body.password2
                            sql.query(`INSERT INTO users SET ?`, req.body, (err, result, fields) => {
                                if (err) {console.log(err)};
                                return msg(res, 0, 'registration success', req.body, 200)
                            })
                        }
                    })
                } else
                    msg(res, -1, 'Two passwords are inconsistent', {}, 200)
            } else
                msg(res, -1, 'Password length must be greater than 6 and less than 16 digits', {}, 200)

          } else
            msg(res, -1, 'Display username already exist !', {}, 200)
      });

    } else
      msg(res, -1, 'The format of mailbox is incorrect, please re-enter', {}, 200)
} else
    msg(res, -1, 'email or password cannot be empty', {}, 200)
});


router.get('/total', (req, res) => {
  sql.query(`SELECT * FROM competition`, (err, result, fields) => {
      if (err) {console.log(err)};
      len = result.length
      console.log("competition table size: ",result.length)
      return msg(res,0, 'length', len, 200)
  })
})

router.post('/user_comp', (req, res) => {
  var u_name = req.body.user_c
  q = `SELECT id from competition WHERE title="${u_name}"`
  console.log(q)
  sql.query(`SELECT id from competition WHERE title="${u_name}"`, (err, result, fields) => {
      console.log(result)
      if (typeof result == "undefined" || result.length == 0){
        return msg(res,0, 'id', "undefined", 200)
      } else {
        if (err) {console.log(err)};
        console.log("id: ",result[0].id)
        return msg(res,0, 'id', result[0].id, 200)
      }
  })
})

router.post('/user_comp_info', (req, res) => {
  var user_n = req.body.user_n
  var comp_n = req.body.comp_n
  sql.query(`SELECT * from ${comp_n} WHERE username="${user_n}"`, (err, result, fields) => {
    console.log(result)
      if (typeof result == 'undefined') {
        return msg(res,0, 'id', "undefined", 200)
      } else {
        if (err) {console.log(err)};
        console.log("id: ",result)
        return msg(res,0, 'id', result, 200)
      }
  })
})



// sign out
router.get('/logout', (req, res) => {
    // require('./userinfo').username = "default";
    req.session.username = "default";
    req.session.isLogin = false;
    return msg(res,0, 'Logged Out', {}, 200)
})

module.exports = router
