# Frontend

A GOV frontend is comprised of three things:

- `govuk_template_jinja` - Provides the header, footer and site wrapper
- `govuk_frontend_toolkit` - Provides various reusable mixins and utilities
- `govuk-elements-sass` - Applies the mixins from the toolkit to generate CSS

These dependencies are managed using `npm` and are tracked in `package.json`. These are pulled together by a [Gulp](http://gulpjs.com/) build process to generate the CSS output for this service.

## Requirements

You will need to install Node.JS on your local machine (Not in the vagrant environment). It is highly recommended that you do this using `nvm`. Follow the steps below:

1. Install `nvm` from https://github.com/creationix/nvm
2. Type `nvm -v`. If it cannot find nvm, you will need to re-source your shell's .zshrc or .bashrc file. To do this, type something like `source ~/.zshrc`
3. Check that `nvm -v` runs
4. Navigate to the application directory (Where the package.json lives)
5. Type `nvm install`. This will look at the `.nvmrc` file in the application directory and install the specified version. If you already had this version installed, you could switch to it with `nvm use`.
6. Type `npm install` (Note the _p_ in the middle, not _v_ this time!)

You then have 2 options. You can

1. Do a one off build by typing `npm run build`
2. Watch the SCSS and JS files and run a build every time they are updated by typing `npm run dev`

At the time of writing, the build does not run in the pipeline and must be run on the developer's laptop. This means that the build artefacts need to be committed into the repository. The following files need to be committed in, but _should not be manually modified_

- `application/assets/dist/**/*.*`
- `application/templates/govuk_template.html` (This file is copied from the `govuk_template_jinja` module in `node_modules`. It is checked into the repository, but should not be modified manually.)

## Editing CSS and JS

Application specific frontend code is held in `application/assets/src` - this is the only place you should be manually editing files.

### JavaScript

The JavaScript is organised as a set of [ES6 modules](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/import) and bundled for the browser using [Rollup](https://github.com/rollup/rollup). There is a single entry point / bundle (`main.js`) by default, but additional bundles will be created for each `.js` file directly inside the `javascripts` folder.

These top levels bundles can be used to `import` files from the `modules` subfolder, or from `node_modules` (Such as if you wish to include a module from https://npmjs.org/). Rollup is set up to import ES6 modules and CommonJS modules (via [rollup-plugin-node-resolve](https://github.com/rollup/rollup-plugin-node-resolve)). Additional plugins can be found at https://github.com/rollup/rollup/wiki/Plugins which can provide support for additional module types, transpilation etc.

### CSS (SCSS)

CSS is organised into application specific and vendor code. At build time, the govuk elements will be copied into the vendor folder ready for use, but it should not be committed into the repository.

Similarly to the JavaScript, the files directly in the `scss` folder represent entry points / bundles, and they import files from the subdirectories. Additional entry points can be created as necessary, but no actual CSS should be written in them.

## Sourcemaps

Sourcemaps are generated for both the CSS and JS output, allowing devtools to map errors back to the original source files (rather than just "line 1, character 37948" of the output bundle).

See https://developers.google.com/web/tools/chrome-devtools/javascript/source-maps#source_maps_in_devtools_sources_panel for info on how to enable these.

## Linting

Run `npm test` to run the linter.

JavaScript is linted with [standardjs](http://standardjs.com/) which is intentionally unconfigurable ([No semicolons - it's fine. Really!](https://github.com/feross/standard#the-rules)) This is gaining widespread adoption including by GOV.UK.

SCSS is linted with [sass-lint](https://github.com/sasstools/sass-lint) but is configured to disable some of the more onerous rules.

## Updating gov.uk elements

The Gov.uk kit versions are maintained as NodeJS dependencies. The versions are tracked in `package.json` but also in `npm-shrinkwrap.json`. To update these, you need to explicitly install the new versions, for example:

- `npm install govuk-elements-sass@2.2.1`
- `npm install govuk_frontend_toolkit@5.0.3`
- `npm install govuk_template_jinja@0.19.2`

This will update `package.json` as well as `npm-shrinkwrap.json`. You should commit these into Git.

Once the packages are updated, run `npm run build`. If nothing significant has changed, then you are done. But there may be errors if they have changed things upstream in an incompatible way. To resolve this, you should read the release notes to see if this helps. If errors occur beyond that, it is a case of traditional debugging.

It is worth noting that new releases often include small markup changes, and sometimes new JavaScript files etc. Reading the release notes thoroughly will reveal anything like this that might be necessary.

### Gov.uk release notes:
- https://github.com/alphagov/govuk_elements/releases
- https://github.com/alphagov/govuk_template/releases

