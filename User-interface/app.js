const express = require('express');
const app = express();
const path = require('path');
const bodyParser = require('body-parser');
// const multer = require('multer');
const client = require('./routes/client')
const user = require('./routes/user')

const session = require('express-session');


// view engine
app.set('views', __dirname);
app.set('view engine', 'html');
app.engine('.html', require('ejs').__express);

// bodyParser
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));

// multer file upload
// app.use(multer());

// Resource path of static directory
app.use(express.static(path.join(__dirname, 'public')));


// home
app.use('/', client)
// login and sighup 
app.use('/user', user)


// session configuration
const options = {
    secret :  'secret', // session id cookie 
    resave : true,
    saveUninitialized: true, //  save Uninitialized session
    cookie : {
        maxAge : 1000 * 60 * 3, // Set the valid time of the session，Unit is milliseconds
    },
};

// session middleware
app.use(session(options));

const port = 3300;
app.listen(port, err => {
    if (err) throw err;
    console.log(`Server is runing address http://localhost:${port}`)
});