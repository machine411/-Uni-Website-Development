const express = require('express');
const router = express.Router()
const sql = require('../config/mysql')
const { msg, reg } = require('../utils/utils')
const fs = require('fs');
const mkdirp = require('mkdirp');
// var user_info = require("./userinfo.js");

router.post('/uploadfile',function(req,res){
  // console.log(req.files)
  // path = 'C:/Users/P/Desktop/SEP/Code/Engine'
  console.log(req)
  if(req.files.ufile){
    var file = req.files.ufile,
    name = file.name,
    type = file.mimetype;
    console.log(req.session.username)
    u_path = 'C:/Users/P/Desktop/SEP/Code/Engine/Users/'+req.session.username
    chal_path = 'C:/Users/P/Desktop/SEP/Code/Engine/Users/'+req.session.username+'/'+req.session.chal_title
    // fs.exists('C:/Users/P/Desktop/SEP/Code/Engine/Users', function(exists) {
    // if(!exists){
    //
    // }
    // });
    mkdirp(u_path, function (err) {
    if (err) console.error(err)
    else console.log('file created')
    });
    mkdirp(chal_path, function (err) {
    if (err) console.error(err)
    else console.log('file created')
    });



    var uploadpath = chal_path + name;
    file.mv(uploadpath,function(err){
      if(err){
        console.log("File Upload Failed",name,err);
        res.send("Error Occured!")
      }
      else {
        console.log("File Uploaded: ",name);
        res.send('Done! Uploading files')
      }
    });
  }
  else {
    res.send("No File selected !");
    res.end();
  };
});

module.exports = router
