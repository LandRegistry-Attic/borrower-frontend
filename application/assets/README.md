# Frontend

A GOV frontend is comprised of three things:

- `govuk_template_jinja` - Provides the header, footer and site wrapper
- `govuk_frontend_toolkit` - Provides various reusable mixins and utilities
- `govuk-elements-sass` - Applies the mixins from the toolkit to generate CSS

These dependencies are managed using `npm` and are tracked in `package.json`. These are pulled together by a [Gulp](http://gulpjs.com/) build process to generate the CSS output for this service.

## Requirements

You will need to install Node.JS on your local machine (Not in the vagrant environment). It is highly recommended that you do this using `nvm`. Follow the steps below:

1. Install `nvm` from https://github.com/creationix/nvm
2. Navigate to the application directory (Where the package.json lives)
3. Type `nvm use`. This will look at the `.nvmrc` file in the application directory and install the specified version.
4. Type `npm install`

You then have 2 options. You can

1. Do a one off build by typing `npm run build`
2. Watch the SCSS and JS files and run a build every time they are updated by typing `npm run dev`

At the time of writing, the build does not run in the pipeline and must be run on the developer's laptop. This means that the build artefacts need to be committed into the repository. The following files need to be committed in, but _should not be manually modified_

- `application/assets/dist/**/*.*`
- `application/templates/govuk_template.html` (This file is copied from the `govuk_template_jinja` module in `node_modules`. It is checked into the repository, but should not be modified manually.)

## Updating gov.uk elements

Instructions to follow, once follow-on task has been completed.
