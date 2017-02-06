var fs = require('fs')
var path = require('path')
var gulp = require('gulp')
var rollup = require('rollup-stream')
var source = require('vinyl-source-stream')
var buffer = require('vinyl-buffer')
var uglify = require('rollup-plugin-uglify')
var sourcemaps = require('gulp-sourcemaps')
var nodeResolve = require('rollup-plugin-node-resolve')

var config = require('../config')

gulp.task('js', function () {
  var entryPoint = path.join(config.assetsPath, 'src/javascripts/main.js')

  if (!fs.existsSync(entryPoint)) {
    return
  }

  return rollup({
    entry: entryPoint,
    sourceMap: true,
    plugins: [
      nodeResolve(),
      uglify({
        compress: {
          screw_ie8: false
        },
        mangle: {
          screw_ie8: false
        },
        output: {
          screw_ie8: false
        }
      })
    ],
    format: 'es'
  })
  .pipe(source('main.js', path.join(config.assetsPath, 'src/javascripts')))
  .pipe(buffer())                           // buffer the output. most gulp plugins, including gulp-sourcemaps, don't support streams.
  .pipe(sourcemaps.init({loadMaps: true}))  // tell gulp-sourcemaps to load the inline sourcemap produced by rollup-stream.
  .pipe(sourcemaps.write('.'))
  .pipe(gulp.dest(path.join(config.assetsPath, '.dist/javascripts')))
})
