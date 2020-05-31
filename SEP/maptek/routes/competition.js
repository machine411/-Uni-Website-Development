const express = require('express')
const router = express.Router()
const sql = require('../config/mysql')
const { msg, reg } = require('../utils/utils')
const mkdirp = require('mkdirp');
const fsExtra = require('fs-extra')
const {PythonShell} = require('python-shell')
const csv_parse = require('csv-parser')
var chal_info = {id : "default", title: "default"};
var options = {
    mode: 'text',
    pythonPath: 'C:/Users/P/AppData/Local/Programs/Python/Python36/python.exe',
    pythonOptions: ['-u'],
    scriptPath: 'C:/Users/P/Desktop/SEP/Code/Engine',
    // args: ['value1', 'value2']
  };

router.get('/', function(req, res) {
    console.log("session.username: ",req.session.username)
    sql.query("select * from competition", (err, result) => {
        if (err) {console.log(err)};
        return msg(res, 0, 'get success', result, 200)
    })
});

router.get('/:id', function(req, res) {
    // console.log("get id: ",req.params.id)
    sql.query(`SELECT * FROM competition where id=${req.params.id}`, (err, result) => {
        if (err) {console.log(err)};
        req.session.chal_id = result[0].id
        req.session.chal_title = result[0].title
        // req.session.chal_id = result[0].id
        // req.session.chal_title = result[0].title
        console.log("check chal_info: ",req.session.chal_title,"  id: ",req.session.chal_id)
        return msg(res, 0, 'get success', result, 200)
    })
});

router.post('/uploadfile',function(req,res){
  // console.log("session:",req.session)
  console.log("chal_info id:  ",req.session.chal_id)
  // console.log("user:  ",require('./userinfo').username)

  if (req.session.username == "default" || typeof req.session.username == "undefined"){
    console.log("NEED LOG IN")
    return msg(res, -1, 'NEED LOG IN FIRST !', {}, 200)
  }
  if (req.files == null){
    // console.log("NEED LOG IN")
    return msg(res, -1, 'Pick A File Plz.. :(', {}, 200)
  }

  if(req.files.ufile){
    var file = req.files.ufile,
    name = file.name,
    type = file.mimetype;
    console.log(req.session.username)
    u_path = 'C:/Users/P/Desktop/SEP/Code/Engine/Users/'+req.session.username
    chal_path = 'C:/Users/P/Desktop/SEP/Code/Engine/Users/'+req.session.username+'/'+req.session.chal_title
    mkdirp(u_path, function (err) {
      if (err) {console.error(err)}
      else {
        console.log('User Folder Created')
        mkdirp(chal_path, function (err) {
          if (err) {console.error(err)}
          else {
            console.log('Challenge Folder created')

            mkdirp(chal_path+'/'+'submission', function (err) {
              if (err) {console.error(err)}
              else {
                console.log('Submission Folder created')
              };
            });

            mkdirp(chal_path+'/'+'best_score', function (err) {
              if (err) {console.error(err)}
              else {
                console.log('Best Submission Folder created')
              };
            });
          };
        });
      };
    });

    var uploadpath = chal_path + '/submission/' + name;
    fsExtra.emptyDirSync(chal_path + '/submission/')
    file.mv(uploadpath,function(err){
      if(err){
        console.log("File Upload Failed",name,err);
        res.send("Error Occured!")
      }
      // Success upload and compile
      else {
        console.log("File Uploaded: ",name);
        ext = name.split('.').pop()
        console.log("ext name: ",ext)
        if (ext != 'py' && ext != 'c' && ext != 'cpp' && ext != 'java')
        {
          return msg(res, -1, 'Check The File Plz.. :( !', {}, 200)
        }
        options.args = [req.session.username, req.session.chal_title]
        // console.log(options.args)
        // full_path = chal_path + '/' + name
        var pyShell = PythonShell.run('eng.py', options, function(err,results) {
          if (err) {console.log(err)};
          console.log(results);
        });
        return msg(res, 0, 'Successfully Uploaded !', {}, 200)
      }
    });
  }
  else {
    res.end();
  };

});

router.post('/delete', (req, res) => {
    let id =req.body.id;
    // Drop ranking table
    sql.query(`SELECT * FROM competition WHERE id="${id}"`, function (err, result) {
      if (err) {console.log(err)};
      bye = result[0].title
      bye = "`"+bye+"`"
      console.log(result[0].title)
      sql.query("DROP TABLE "+bye, function (err, result) {
          if (err) {console.log(err)};
          console.log("Ranking Table Dropped")
          });
    });

    sql.query(`delete FROM competition WHERE id="${id}"`, (err, result) => {
        if (err) {console.log(err)};
        if(result.affectedRows){
            msg(res, 0, 'delete success', {}, 200);
        }else{
            msg(res, -1, 'delete failed', {}, 200);
        }
    });
});


router.get('/:id/rank', (req, res) => {
  // var req.session.username = require('./userinfo')
  console.log("get id: ",req.params.id)

  sql.query(`SELECT title FROM competition WHERE id=${req.params.id}`, (err, result) => {
        if (err) {console.log(err)};
        req.session.chal_id = req.params;
        req.session.chal_title = result[0].title;
        console.log(req.session.chal_title)
        console.log("RANK")
        chal_lowcase = (req.session.chal_title).toLowerCase()
        options.args = [chal_lowcase]
        console.log("title: ",req.session.chal_title)
        // rank_path = "C:/Users/P/Desktop/SEP/Code/Engine/Rank/rank_v2.py"
        var pyShell = PythonShell.run("rank_v2.py", options, function(err,results) {
          if (err) {console.log(err)};
          console.log(results);
          if (results[0] == 'Empty Table'){return msg(res, 0, 'Rank sorted',{}, 200);}
          const fs = require('fs')
          var results = [];
          console.log("username: ",req.session.username);
          results.push(req.session.username);

      // Results -> [ user's marks, All data in csv ]
          tmp_title = "`"+req.session.chal_title+"`"
          sql.query(`SELECT * FROM ${tmp_title} WHERE username= "${req.session.username}"`, (err, result) => {
              if (err) {console.log(err)};
              results.push(result[0])
              fs.createReadStream('C:/Users/P/Desktop/SEP/Code/Engine/Rank/'+chal_lowcase+'.csv')
              .pipe(csv_parse(['username','score']))
              .on('data', (data) => results.push(data))
              .on('end', () => {
                // console.log(results);
                return msg(res, 0, 'Rank sorted',results, 200);
              });
          });
        });

  })



  // router.post('/:id/person',function(req,res){
  //   var req.session.username = require('./userinfo')
  //   console.log("adsfasdfasdfasdf")
  //   sql.query(`select * FROM ${req.session.chal_title} username="${req.session.chal_id}"`, (err, result) => {
  //       if (err) {console.log(err)};
  //       console.log(result);
  //       return msg(res, 0, 'Marks',result, 200);
  //   });
  // });


//   sql.query("select * from "+req.session.chal_title, (err, result) => {
//     if (err) {console.log(err)};
//     console.log(result)
//     return msg(res, 0, 'get success', result, 200)
//   })

});



router.post('/insert', (req, res) => {
    let title =req.body.title;
    let duetime =req.body.duetime;
    // let rank =req.body.rank;
    let description =req.body.description;
    let exist = 0
    title = title.trim()
    sql.query(`SELECT EXISTS(SELECT * from competition WHERE title='${title}') AS exist`, (err, result) => {
        if (err) {console.log(err)};
        exist = result[0].exist
        console.log("exist",exist)
        if(exist == 1){
          return msg(res, -1, "competition already exist", {}, 200);
        }else{
          sql.query(`insert into competition values(null,"${title}","${description}","${duetime}")`, (err, result) => {
              if (err) {console.log(err)};
              if(result.insertId){
                  msg(res, 0, 'insert success', {}, 200);
              }else{
                  msg(res, -1, 'insert failed', {}, 200);
              }
          })
          console.log(title)
          title = "`"+title+"`"
          var create_query = `CREATE TABLE `+ title +` (username varchar(255) NOT NULL PRIMARY KEY, final_mark float DEFAULT NULL, correct_mark float DEFAULT NULL, time_mark float DEFAULT NULL, memory_mark float DEFAULT NULL, best_mark float DEFAULT NULL)`;

          sql.query(create_query, function (err, result) {
          if (err) {console.log(err)};
          console.log("Table created");
          });
        }

    })


});














module.exports = router
