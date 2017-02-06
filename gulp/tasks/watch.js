var gulp = require('gulp')
var path = require('path')

var config = require('../config')

gulp.task('watch', function () {
  gulp.watch(path.join(config.assetsPath, 'src/scss/**/*.scss'), ['sass', 'sass-lint'])
  gulp.watch(path.join(config.assetsPath, 'src/javascripts/**/*.js'), ['js', 'standardjs'])
  gulp.watch('gulp/**/*.js', ['standardjs'])

  console.log('Watching...')
})
