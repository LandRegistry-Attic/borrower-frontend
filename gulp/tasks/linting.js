var gulp = require('gulp')
var path = require('path')
var standard = require('gulp-standard')

var config = require('../config')

gulp.task('standardjs', function () {
  return gulp.src([path.join(config.assetsPath, '**/*.js'), 'gulp/**/*.js'])
    .pipe(standard())
    .pipe(standard.reporter('default', {
      breakOnError: false,
      quiet: true,
      showRuleNames: true
    }))
})

gulp.task('test', ['standardjs'])
