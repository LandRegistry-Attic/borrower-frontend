module.exports = function (grunt) {

  grunt.initConfig({

    // Builds Sass
    sass: {
      dev: {
        files: {
          'elements-toolkit/public/stylesheets/main.css': 'elements-toolkit/public/sass/main.scss',
          'elements-toolkit/public/stylesheets/main-ie6.css': 'elements-toolkit/public/sass/main-ie6.scss',
          'elements-toolkit/public/stylesheets/main-ie7.css': 'elements-toolkit/public/sass/main-ie7.scss',
          'elements-toolkit/public/stylesheets/main-ie8.css': 'elements-toolkit/public/sass/main-ie8.scss',
          'elements-toolkit/public/stylesheets/elements-page.css': 'elements-toolkit/public/sass/elements-page.scss',
          'elements-toolkit/public/stylesheets/elements-page-ie6.css': 'elements-toolkit/public/sass/elements-page-ie6.scss',
          'elements-toolkit/public/stylesheets/elements-page-ie7.css': 'elements-toolkit/public/sass/elements-page-ie7.scss',
          'elements-toolkit/public/stylesheets/elements-page-ie8.css': 'elements-toolkit/public/sass/elements-page-ie8.scss',
          'elements-toolkit/public/stylesheets/prism.css': 'elements-toolkit/public/sass/prism.scss'
        },
        options: {
          includePaths: ['elements-toolkit/govuk_modules/public/sass'],
          outputStyle: 'expanded',
          imagePath: '../images'
        }
      }
    },

    // Copies templates and assets from external modules and dirs
    copy: {

      govuk_template: {
        src: 'node_modules/govuk_template_mustache/views/layouts/govuk_template.html',
        dest: 'elements-toolkit/govuk_modules/views/',
        expand: true,
        flatten: true,
        filter: 'isFile'
      },

      govuk_assets: {
        files: [
          {
            expand: true,
            src: '**',
            cwd: 'elements-toolkit/node_modules/govuk_template_mustache/assets',
            dest: 'elements-toolkit/govuk_modules/public/'
          }
        ]
      },

      govuk_frontend_toolkit_scss: {
        expand: true,
        src: '**',
        cwd: 'elements-toolkit/node_modules/govuk_frontend_toolkit/stylesheets/',
        dest: 'elements-toolkit/govuk_modules/public/sass/'
      },

      govuk_frontend_toolkit_js: {
        expand: true,
        src: '**',
        cwd: 'elements-toolkit/node_modules/govuk_frontend_toolkit/javascripts/',
        dest: 'govuk_modules/public/javascripts/'
      },

      govuk_frontend_toolkit_img: {
        expand: true,
        src: '**',
        cwd: 'elements-toolkit/node_modules/govuk_frontend_toolkit/images/',
        dest: 'elements-toolkit/govuk_modules/public/images/icons/'
      },
      grunt_copy_css: {
        expand: true,           // required when using cwd
        cwd: 'elements-toolkit/public/stylesheets',  // set working folder / root to copy
        src: '*.css',           // copy all *.css
        dest: '../application/static/elements'   // destination folder
      }

    },

    // workaround for libsass
    replace: {
      fixSass: {
        src: ['elements-toolkit/govuk_modules/public/sass/**/*.scss'],
        overwrite: true,
        replacements: [{
          from: /filter:chroma(.*);/g,
          to: 'filter:unquote("chroma$1");'
        }]
      }
    },

    // Watches styles and specs for changes
    watch: {
      css: {
        files: ['elements-toolkit/public/sass/**/*.scss'],
        tasks: ['sass'],
        options: {nospawn: true}
      }
    },

    // nodemon watches for changes and restarts app
    nodemon: {
      dev: {
        script: 'app.js',
        options: {
          ext: 'html, js'
        }
      }
    },

    concurrent: {
      target: {
        tasks: ['watch', 'nodemon'],
        options: {
          logConcurrentOutput: true
        }
      }
    },

    // Lint scss files
    scsslint: {
      allFiles: [
        'elements-toolkit/public/sass/elements/*.scss',
        'elements-toolkit/public/sass/elements/forms/*.scss'
      ],
      options: {
        bundleExec: false,
        colorizeOutput: true,
        config: '.scss-lint.yml',
        force: true,
        reporterOutput: null
      }

    }
  });

  [
    'grunt-contrib-copy',
    'grunt-contrib-watch',
    'grunt-sass',
    'grunt-text-replace',
    'grunt-scss-lint'
  ].forEach(function (task) {
    grunt.loadNpmTasks(task);
  });

  grunt.registerTask(
    'convert_template',
    'Converts the govuk_template to use mustache inheritance',
    function () {
      var script = require(__dirname + '/elements-toolkit/lib/template-conversion.js');

      script.convert();
      grunt.log.writeln('govuk_template converted');
    }
  );

  grunt.registerTask('default', [
    'copy:govuk_template',
    'copy:govuk_assets',
    'convert_template',
    'copy:govuk_frontend_toolkit_scss',
    'copy:govuk_frontend_toolkit_js',
    'copy:govuk_frontend_toolkit_img',
    'replace',
    'sass',
    'copy:grunt_copy_css'
  ]);

  grunt.registerTask(
    'lint',
    'scsslint'
  );

};
