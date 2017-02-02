var gulp = require('gulp')

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

gulp.task('copyGov', [
  'copyGovTemplate',
  'copyGovTemplateAssets',
  'copyGovElements',
  'copyGovToolkitImages',
])
