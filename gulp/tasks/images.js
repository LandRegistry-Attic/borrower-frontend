var gulp = require('gulp')
var path = require('path')
var config = require('../config')

gulp.task('images', function () {
  return gulp
    .src(path.join(config.assetsPath, 'src/images/**'))
    .pipe(gulp.dest(path.join(config.assetsPath, 'dist/images/app')))
})