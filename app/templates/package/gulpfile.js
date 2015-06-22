var gulp = require('gulp');
var spawn = require('child_process').spawn;
var shell = require('shelljs');
var livereload = require('gulp-livereload');

function runserver(mainFile, port) {
    'use strict';
    spawn('python', [mainFile, '-p', (port || 5000)], 
          { 
              stdio: 'inherit',
          });
}

gulp.task('serve', function () {
    'use strict';
    runserver('runserver.py');
});

gulp.task('watch', function () {
    'use strict';
    livereload.listen();
    gulp.watch('templates/**/*.html', function () {
        gulp.src('templates/**/*.html').pipe(livereload());
    });
    gulp.watch('static/sass/**/*.scss', ['compass']);
});

gulp.task('compass', function () {
    'use strict';
    shell.cd('static');
    shell.exec('compass compile');
    shell.cd('..');
    gulp.src('static/css/**/*.css').pipe(livereload());
});

gulp.task('init-db', function () {
    'use strict';
    spawn('python', ['scripts/init_db.py'], 
          { 
              stdio: 'inherit',
          });
});

gulp.task('make-test-data', function () {
    'use strict';
    spawn('python', ['scripts/make_test_data.py'], 
          { 
              stdio: 'inherit',
          });
});

gulp.task('render', ['compass'], function () {
    var scriptsMap = yaml.load('scripts.yml');
    var shimsMap = yaml.load('shims.yml');
    [
        {
            app: 'foo',
            mods: ['list', 'object']
        }
    ].forEach(function (app) {
        var libs = yaml.load('./' + app.app + '/libs.yml');
        app.mods.forEach(function (mod) {
            gulp.src(['main.js.mtpl']).pipe(data({
                scriptsMap: scriptsMap,
                shimsMap: shimsMap,
                urlRoot: '/',
                libs: libs[mod],
                app: app.app,
                mod: mod,
            })).pipe(template()).pipe(rename(function (path) {
                path.extname = '';
            })).pipe(gulp.dest('static/js/' + app.app + '/' + mod + '/'));
        });
    });
    gulp.src('templates/gas_station/import-manifest.md').pipe(markdown()).pipe(gulp.dest('templates/gas_station'));
    gulp.src('templates/utilities/gas-station-canonize-help.md').pipe(markdown()).pipe(gulp.dest('templates/utilities'));
});

gulp.task('default', ['watch', 'serve']);
