var path = require('path')
var gulp = require('gulp')
var sourcemaps = require('gulp-sourcemaps')
var sass = require('gulp-sass')
var postcss = require('gulp-postcss')
var cssnano = require('cssnano')
var autoprefixer = require('autoprefixer')

var config = require('../config')

gulp.task('sass', function () {
  var sassOptions = {
    outputStyle: 'compressed'
  }

  return gulp.src(path.join(config.assetsPath, config.sassPath))
    .pipe(sourcemaps.init())
    .pipe(sass(sassOptions).on('error', sass.logError))
    .pipe(postcss([
      autoprefixer(),
      cssnano()
    ]))
    .pipe(sourcemaps.write('.'))
    .pipe(gulp.dest(path.join(config.assetsPath, 'dist/stylesheets')))
})
