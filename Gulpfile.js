var path = require('path')
var fs = require('fs')

var gulp = require('gulp')
var sourcemaps = require('gulp-sourcemaps')
var sass = require('gulp-sass')
var postcss = require('gulp-postcss')
var cssnano = require('cssnano')
var autoprefixer = require('autoprefixer')
var rollup = require('rollup-stream')
var source = require('vinyl-source-stream')
var buffer = require('vinyl-buffer')
var uglify = require('rollup-plugin-uglify')
var standard = require('gulp-standard')

var assetsPath = './application/assets'
var sassPath = 'src/scss/*.scss'

/**
 * Custom node-sass importer to fetch sass files from the govuk_frontend_toolkit
 * node_modules folder
 *
 * @param  {String}   url     the path in import as-is, which LibSass encountered
 * @param  {String}   prev    the previously resolved path
 * @param  {Function} done    a callback function to invoke on async completion.
 *                            @see https://github.com/sass/node-sass#importer--v200---experimental
 */
// var govukFrontendToolkitImporter = function(url, prev, done) {
//   if (url.indexOf('govuk_frontend_toolkit') === 0) {
//     return done({
//       file: url.replace('govuk_frontend_toolkit', path.join(pkg_dir.sync(__dirname), 'node_modules/govuk-elements-sass/node_modules/govuk_frontend_toolkit/stylesheets'))
//     });
//   }

//   done();
// };

gulp.task('sass', function () {
  var sassOptions = {
    outputStyle: 'compressed',
    includePaths: [
      path.resolve('application/assets/src/.govuk-elements')
    ]
  }

  console.log(path.resolve('node_modules/govuk_frontend_toolkit/stylesheets'))

  return gulp.src(path.join(assetsPath, sassPath))
    .pipe(sourcemaps.init())
    .pipe(sass({outputStyle: 'compressed'}).on('error', sass.logError))
    .pipe(postcss([
      autoprefixer(),
      cssnano()
    ]))
    .pipe(sourcemaps.write('.'))
    .pipe(gulp.dest(path.join(assetsPath, '.dist/stylesheets')))
})

gulp.task('js', function () {
  var entryPoint = 'src/javascript/main.js'

  if(!fs.existsSync(entryPoint)) {
    return
  }

  return rollup({
    entry: path.join(assetsPath, entryPoint),
    sourceMap: true,
    plugins: [
      uglify()
    ]
  })
  .pipe(source('main.js', path.join(assetsPath, 'src/javascript')))         // point to the entry file.
  .pipe(buffer())                           // buffer the output. most gulp plugins, including gulp-sourcemaps, don't support streams.
  .pipe(sourcemaps.init({loadMaps: true}))  // tell gulp-sourcemaps to load the inline sourcemap produced by rollup-stream.
  // .pipe(rename('index.js'))                // if you want to output with a different name from the input file, use gulp-rename here.
  .pipe(sourcemaps.write('.'))
  .pipe(gulp.dest(path.join(assetsPath, '.dist/javascripts')))
})

gulp.task('standardjs', function () {
  return gulp.src(['**/*.js', '!node_modules/**/*.*'])
    .pipe(standard())
    .pipe(standard.reporter('default', {
      breakOnError: false,
      quiet: true,
      showRuleNames: true
    }))
})

gulp.task('copyGovTemplate', function() {
   return gulp
    .src('node_modules/govuk_template_jinja/views/layouts/**')
    .pipe(gulp.dest('application/templates/base'))
});

gulp.task('copyGovTemplateAssets', function() {
   return gulp
    .src('node_modules/govuk_template_jinja/assets/**')
    .pipe(gulp.dest('application/assets/.dist'))
});

gulp.task('copyGovToolkitImages', function() {
   return gulp
    .src('node_modules/govuk_frontend_toolkit/images/**')
    .pipe(gulp.dest('application/assets/.dist/images'))
});

gulp.task('copyGovElements', function() {
   return gulp
    .src([
       'node_modules/govuk-elements-sass/public/sass/**',
       'node_modules/govuk_frontend_toolkit/stylesheets/**'
    ])
    .pipe(gulp.dest('application/assets/src/scss/.govuk-elements'))
});

gulp.task('test', ['standardjs'])

gulp.task('watch', function () {
  gulp.watch(path.join(assetsPath, sassPath), ['sass'])
  gulp.watch(path.join(assetsPath, 'src/javascript/**/*.js'), ['js', 'standardjs'])
})

gulp.task('default', ['copyGovTemplate', 'copyGovTemplateAssets', 'copyGovElements', 'copyGovToolkitImages', /*'copyGovToolkitJavascript',*/ 'sass', 'js'])
