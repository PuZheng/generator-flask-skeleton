'use strict';
var yeoman = require('yeoman-generator');
var chalk = require('chalk');
var yosay = require('yosay');
var lodash = require('lodash');
var walk = require('walk');
var path = require('path');

module.exports = yeoman.generators.Base.extend({
    initializing: function () {
        this.pkg = require('../package.json');
    },

    prompting: function () {
        var done = this.async();

        // Have Yeoman greet the user.
        this.log(yosay(
            'Welcome to the awe-inspiring' + chalk.red('FlaskSkeleton') + ' generator!'
        ));

        var prompts = [{
            type: 'input',
            name: 'projectName',
            message: 'Your project name',
        },  {
            type: 'input',
            name: 'packageName',
            message: 'Your package name',
        }, {
            type: 'confirm',
            name: 'bootstrap',
            message: 'with bootstrap suite?',
            default: true
        }];

        this.templateArgs = {};
        this.prompt(prompts, function (props) {
            this.templateArgs.projectName = props.projectName;
            this.templateArgs.packageName = props.packageName;
            this.templateArgs.bootstrap = props.bootstrap;
            done();
        }.bind(this));
    },

    writing: {
        app: function () {
            lodash.each(['bower.json', 'package.json', 'requirements.txt', 
                        'gulpfile.js', '.bowerrc', 'setup.py'], function (fname) {
                            this.fs.copyTpl(
                                this.templatePath(fname),
                                this.destinationPath(fname),
                                this.templateArgs
                            );
                        }.bind(this));
            walk.walkSync(this.templatePath('__package__'), {
                listeners: {
                    file: function (root, stat, next) {
                        var fullpath = path.join(root, stat.name);
                        if (fullpath.indexOf('bower_components') === -1) {
                            this.fs.copyTpl(fullpath,
                                            this.destinationPath(this.templateArgs.packageName + '/' + 
                                                                 path.relative(this.templatePath('__package__'), fullpath)), 
                                            this.templateArgs);
                        }
                        next();
                    }.bind(this),
                }
            });
        },

        projectfiles: function () {
            this.fs.copy(
                this.templatePath('.editorconfig'),
                this.destinationPath('.editorconfig')
            );
            this.fs.copy(
                this.templatePath('.jshintrc'),
                this.destinationPath('.jshintrc')
            );
        }, 

    },

    install: function () {
        this.installDependencies({
            skipInstall: this.options['skip-install']
        });
        //this.spawnCommand('python', ['setup.py', 'develop']);
    }
});
