var path = require('path')
var fs = require('fs')
var gulp = require('gulp')
var sourcemaps = require('gulp-sourcemaps')
var sass = require('gulp-sass')
var postcss = require('gulp-postcss')
var cssnano = require('cssnano')
var autoprefixer = require('autoprefixer')

var config = require('../config')

gulp.task('sass', ['copyGov'], function () {
  var sassOptions = {
    outputStyle: 'compressed',
    includePaths: [
      path.resolve(path.join(config.assetsPath, 'src/.govuk-elements'))
    ]
  }

  return gulp.src(path.join(config.assetsPath, config.sassPath))
    .pipe(sourcemaps.init())
    .pipe(sass({outputStyle: 'compressed'}).on('error', sass.logError))
    .pipe(postcss([
      autoprefixer(),
      cssnano()
    ]))
    .pipe(sourcemaps.write('.'))
    .pipe(gulp.dest(path.join(config.assetsPath, '.dist/stylesheets')))
})
