var gulp = require('gulp')

gulp.task('copy', [
  'clean',
  'copyGov'
])

gulp.task('build', [
  'sass',
  'js'
])

gulp.task('default', [
  'build'
])
