var bodyParser = require('body-parser');
var cors = require('cors')
var express = require('express');
var path = require('path');
var passport = require('passport');
var config = require('./config/config.json')

// routes文件中添加的路由在这里进行注册
var auth = require('./routes/auth')
var index = require('./routes/index');
var news = require('./routes/news')

var app = express();

require('./models/main.js').connect(config.mongoDbUri)

// view engine setup
// 什么是build？react项目与angular项目很像，可以采用类似ng-build的方式，把前端代码build
// 到一个public的文件夹下，然后从服务端的文件夹下去serve，把public里的内容返回给用户
app.set('views', path.join(__dirname, '../client/build/'));
// 设置模板引擎，类似于jsp，php这种用template来呈现，从服务端生成好页面来返回给前端
// 与用react这种方式截然不同，此处放着就行
app.set('view engine', 'jade');
app.use('/static', express.static(path.join(__dirname, '../client/build/static/')));

// TODO: remove this after development is done
// 跨域，方便调试（前端client不支持自动build，所以调试时react的server也会起起来）
app.use(cors());
app.use(bodyParser.json());

// load passport strategies
// In a express-based application, passport.initialize() middleware is required to initialize Passport.
app.use(passport.initialize());
var localSignupStrategy = require('./passport/signup_passport');
var localLoginStrategy = require('./passport/login_passport');
passport.use('local-signup', localSignupStrategy);
passport.use('local-login', localLoginStrategy);

// 添加路由
app.use('/', index);
app.use('/auth', auth);

const authCheckMiddleware = require('./middleware/auth_checker');
app.use('/news', authCheckMiddleware);

app.use('/news', news)

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  var err = new Error('Not Found');
  err.status = 404;
  res.send('404 Not Found');
});

module.exports = app;
