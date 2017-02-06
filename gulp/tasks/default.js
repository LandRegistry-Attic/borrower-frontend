var gulp = require('gulp')

gulp.task('copy', [
  'copyGov',
  'copyFontAwesome'
])

gulp.task('build', [
  'sass',
  'js'
])

gulp.task('default', [
  'build'
])
