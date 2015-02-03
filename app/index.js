'use strict';
var yeoman = require('yeoman-generator');
var chalk = require('chalk');
var yosay = require('yosay');
var _ = require('underscore');

module.exports = yeoman.generators.Base.extend({
    initializing: function () {
        this.pkg = require('../package.json');
    },

    method1: function () {
        console.log('method1');
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
        }];

        this.prompt(prompts, function (props) {
            this.projectName = props.projectName;
            this.packageName = props.packageName;
            done();
        }.bind(this));
    },

    writing: {
        app: function () {

            _(['bower.json', 'package.json', 'requirements.txt', ['setup.py', {
                projectName: this.projectName,
                packageName: this.packageName,
            }]]).each(function (fname) {
                if (typeof(fname) == 'string') {
                    this.fs.copy(
                        this.templatePath(fname),
                        this.destinationPath(fname)
                    );
                } else {
                    this.fs.copyTpl(
                        this.templatePath(fname[0]),
                        this.destinationPath(fname[0]),
                        fname[1]
                    );
                
                }
            }.bind(this));

            this.fs.copy(this.templatePath('__package__/__init__.py'), this.destinationPath(this.packageName + '/__init__.py'));
            this.fs.copyTpl(this.templatePath('__package__/basemain.py'), this.destinationPath(this.packageName + '/basemain.py'), 
                            {
                                projectName: this.projectName,
                            });
            this.destinationRoot('test/static');
            this.composeWith('h5bp');
            this.destinationRoot('../../');
            this.fs.move(this.destinationPath('test/static/index.html'), this.destinationPath('test/templates/index.html'));
            this.fs.move(this.destinationPath('test/static/404.html'), this.destinationPath('test/templates/404.html'));
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
        }
    },

    install: function () {
        this.installDependencies({
            skipInstall: this.options['skip-install']
        });
    }
});
