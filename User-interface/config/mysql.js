const mysql = require('mysql')

// mysql connect
const connection = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: 'Kaixiang82',
    database: 'testsql'
});

// 连接数据库
connection.connect(err => {
    if (err) throw err;
    console.log('MySQL is Connected...');
})

module.exports = connection