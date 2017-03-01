
# dm-borrower-frontend -frontend - build

The templates and styles for the borrower frontend are built using a copy of the 
[Gov.UK Elements repo](https://github.com/alphagov/govuk_elements) which is setup as a git sub-module repo in the 
/build/elements-toolkit directory. 

The Elements repo uses the [Gov.UK frontend toolkit](https://github.com/alphagov/govuk_frontend_toolkit) which is 
downloaded into the build/elements-toolkit/govuk_modules directory as part of a grunt build (see below). 

The dm-borrower-frontend also uses the [Gov.UK Jinja2](https://github.com/alphagov/govuk_template) template which 
is downloaded into the /build directory before being copied into the 'live' /application/static/govuk_template folder.
The build directory in this project is intended as a staging area for the import and compilation of the 
government templates from source code (SASS). The build process only needs to be run if the intention is to update
the government templates and styles into the live /application directory.


## Contents
- [Initialise Elements Submodule](#initalise-elements-submodule)
- [Install Grunt](#install-grunt)
- [Run Grunt](#run-grunt)
- [Update GovUK FrontEnd Templates](#Update-GovUK-FrontEnd-Templates)

#Initialise Elements Submodule

```
git submodule init
git submodule update
```

#Install Grunt

From the build/ directory:-

```
npm install                     -- installs the dependencies in the package.json as local node modules
sudo npm install -g grunt-cli   -- install the grunt tool as a global tool
cd elements-toolkit
npm install
```

#Run Grunt

From the build/elements-toolkit directory:-

```
grunt
```

From the build/ directory:-

```
grunt
```

Running grunt will:-


1) download the govuk-frontend-toolkit
2) Compile elements and frontend toolkit SASS
3) Copy *.css files into /application/static/elements directory

note: the gruntfile in this directory is a copy of the one in the elements toolkit sub-module extended with an
extra task to copy the built *.css files into /application/static/elements directory (with necessary path adjustments)


#Update GovUK FrontEnd Templates


From the build/ directory

```
python3 tap.py
```

This will download the latest copy of the Jinja templates and assets and copy them into 
/application/static/govuk_template directory.

#Setup PyCharm IDE

1) Install SASS using:- gem install sass
2) In PyCharm, Setup a watcher to auto build sass Preferences|Tools|File Watchers

Click '+' to add and setup as follows:

File Type: .SCSS
Scope: Project files
Program: /usr/local/bin/sass
Arguments: $FileDir$/$FileName$ $FileDir$/$FileNameWithoutExtension$.css  -I /Users/User1/landregistry/beta/dm-borrower-frontend/build/elements-toolkit/govuk_modules/public/sass
Working Directory: $ProjectFileDir
Output Paths to refresh: $FileNameWithoutExtension$.css

3) Changes to landregistry.scss and application.scss will build .css files


