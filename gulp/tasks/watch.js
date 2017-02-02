var gulp = require('gulp')
var path = require('path')

gulp.task('watch', function () {
  gulp.watch(path.join(assetsPath, sassPath), ['sass'])
  gulp.watch(path.join(assetsPath, 'src/javascript/**/*.js'), ['js', 'standardjs'])
})
