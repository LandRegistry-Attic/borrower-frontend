var gulp = require('gulp')
var del = require('del')
var path = require('path')

var config = require('../config')

gulp.task('clean', function () {
  return del(path.join(config.assetsPath, '.dist'))
})
