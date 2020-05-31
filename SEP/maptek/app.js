const express = require('express');
const app = express();
const path = require('path');
const bodyParser = require('body-parser');
// const multer = require('multer');
const client = require('./routes/client')
const user = require('./routes/user')
// const upload = require('./routes/upload')
const dashboard = require('./routes/dashboard')
const competition = require('./routes/competition')
// const multer = require('multer');
const session = require('express-session');
const fileUpload = require('express-fileupload')

// const port = 3300;
const{
  port = 3300,
  sess_name = 'sid'

} = process.env

// session configuration
const options = {
  secret :'secret', // session id cookie
  name: sess_name,
  resave : true,
  saveUninitialized: false, //  save Uninitialized session
  cookie : {
    maxAge : 1000 * 60 * 60 * 2, // Set the valid time of the session，Unit is milliseconds
  },
};

// session middleware
app.use(session(options));

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

//
// const up = multer({ dest: 'uploads/' })
app.use(fileUpload())
// home
app.use('/', client)
// login and sighup
app.use('/user', user)

app.use('/dashboard', dashboard)

// app.use('/upload', upload)
app.use('/getCompetition', competition)





app.listen(port, err => {
    if (err) throw err;
    console.log(`Server is runing address http://localhost:${port}`)
});
