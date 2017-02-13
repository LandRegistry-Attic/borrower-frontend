var gulp = require('gulp')
var path = require('path')

var config = require('../config')
var browserSync = require('../modules/browsersync')

gulp.task('watch', function () {
  gulp.watch(path.join(config.assetsPath, 'src/scss/**/*.scss'), ['sass', 'sass-lint'])
  gulp.watch(path.join(config.assetsPath, 'src/javascripts/**/*.js'), ['js', 'standardjs'])
  gulp.watch('gulp/**/*.js', ['standardjs'])

  browserSync.init({
    proxy: config.localhost
  })

  console.log('Watching...')
})
