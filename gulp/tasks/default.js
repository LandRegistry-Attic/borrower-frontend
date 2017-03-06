var gulp = require('gulp')

gulp.task('copy', [
  'clean',
  'copyGov'
])

gulp.task('build', [
  'sass',
  'js',
  'images'
])

gulp.task('default', [
  'build'
])
