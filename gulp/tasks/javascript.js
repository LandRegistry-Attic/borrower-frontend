var fs = require('fs')
var path = require('path')
var gulp = require('gulp')
var rollup = require('rollup-stream')
var source = require('vinyl-source-stream')
var buffer = require('vinyl-buffer')
var uglify = require('rollup-plugin-uglify')
var sourcemaps = require('gulp-sourcemaps')

var config = require('../config')

gulp.task('js', ['copyGov'], function () {
  var entryPoint = 'src/javascript/main.js'

  if(!fs.existsSync(entryPoint)) {
    return
  }

  return rollup({
    entry: path.join(config.assetsPath, entryPoint),
    sourceMap: true,
    plugins: [
      uglify()
    ]
  })
  .pipe(source('main.js', path.join(config.assetsPath, 'src/javascript')))         // point to the entry file.
  .pipe(buffer())                           // buffer the output. most gulp plugins, including gulp-sourcemaps, don't support streams.
  .pipe(sourcemaps.init({loadMaps: true}))  // tell gulp-sourcemaps to load the inline sourcemap produced by rollup-stream.
  // .pipe(rename('index.js'))                // if you want to output with a different name from the input file, use gulp-rename here.
  .pipe(sourcemaps.write('.'))
  .pipe(gulp.dest(path.join(config.assetsPath, '.dist/javascripts')))
})
