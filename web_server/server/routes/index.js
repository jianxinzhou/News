
var express = require('express');
var router = express.Router();
var path = require('path');

// 访问根目录，返回页面index.html
router.get('/', function(req, res, next) {
  res.sendFile("index.html",{root:path.join(__dirname,'../../client/build/')});
});

module.exports = router;
