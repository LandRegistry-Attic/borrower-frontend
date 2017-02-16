var gulp = require('gulp')
var del = require('del')
var path = require('path')

var config = require('../config')

gulp.task('clean', ['cleanDist', 'cleanGov'])

gulp.task('cleanDist', function () {
  return del(path.join(config.assetsPath, 'dist'))
})

gulp.task('cleanGov', function () {
  return del(path.join(config.assetsPath, 'src/scss/vendor/govuk-elements'))
})
