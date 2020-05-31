const express = require('express')
const router = express.Router()
const sql = require('../config/mysql')
const { msg, reg } = require('../utils/utils')
const fs = require('fs');



router.get('/list', (req, res) => {
  // var user_info = require('./userinfo')
  // var user_info = req.session.username
  var query = ""
  // chal_lowcase = (chal_info.title).toLowerCase()
  console.log("current user: ",req.session.username)
  if (req.session.username == "default"){
      return msg(res, 0, 'Chal & Mark',"default", 200);
  } else if (req.session.username == "BALEX"){
      return msg(res, 0, 'Chal & Mark',"BALEX", 200);
  }

  sql.query(`SELECT competition.title FROM competition ;`, (err, title_result) => {
    if (err) throw err;
    console.log("all_comp: ",title_result[0].title)

    for (var i = 0; i < title_result.length; i++) {
      if (i == 0){
        query = `SELECT best_mark From ${title_result[i].title} WHERE username="${req.session.username}"`;
      } else{
        query += ` UNION `+ `SELECT best_mark From ${title_result[i].title} WHERE username="${req.session.username}"`
      }
    }
    sql.query(query, (err, result) => {
        if (err) {console.log(err)};
        console.log("query res:",result)
        var chal_mark = [];
        if (result.length == 0){
          chal_mark.push({user:req.session.username})
          console.log(chal_mark)
          return msg(res, 0, 'Chal & Mark',chal_mark, 200);
        }
        for (var i = 0; i < result.length; i++) {
          chal_mark.push({chal: title_result[i].title, mark: result[i].best_mark});
        }

        chal_mark.push({user:req.session.username});
        return msg(res, 0, 'Chal & Mark',chal_mark, 200);
    });

  });

});


router.post('/getid', function(req, res) {
    sql.query(`SELECT id FROM competition WHERE title="${req.body.chal}"`, (err, result) => {
        if (err) throw err;
        console.log(result)
        return msg(res, 0, 'get success', result, 200)
    })
});













module.exports = router
