const mysql = require('mysql')

// mysql connect
const connection = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: '123',
    database: 'test_version',
});

// connect to database
connection.connect(err => {
    if (err) throw err;
    console.log('MySQL is Connected...');
})

module.exports = connection
