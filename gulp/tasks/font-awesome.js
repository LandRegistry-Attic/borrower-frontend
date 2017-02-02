var gulp = require('gulp')
var path = require('path')

var config = require('../config')

gulp.task('copyFontAwesome', ['clean'], function () {
  return gulp
    .src(path.join(config.assetsPath, 'src/scss/font-awesome/font/**'))
    .pipe(gulp.dest(path.join(config.assetsPath, '.dist/font')))
})
