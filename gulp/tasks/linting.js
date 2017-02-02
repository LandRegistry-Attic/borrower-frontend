var gulp = require('gulp')
var standard = require('gulp-standard')

gulp.task('standardjs', function () {
  return gulp.src(['**/*.js', '!node_modules/**/*.*'])
    .pipe(standard())
    .pipe(standard.reporter('default', {
      breakOnError: false,
      quiet: true,
      showRuleNames: true
    }))
})

gulp.task('test', ['standardjs'])
