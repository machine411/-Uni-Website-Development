var express = require('express');
var app = express();
var path = require('path');
 
app.set('views', __dirname);
 
app.set( 'view engine', 'html' );
app.engine( '.html', require( 'ejs' ).__express );
 
app.get('/', function(req, res) {
　　res.render('login');
});
 
app.listen(80);