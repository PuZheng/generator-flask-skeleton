var gulp = require('gulp');
var spawn = require('child_process').spawn;
var shell = require('shelljs');
var livereload = require('gulp-livereload');

function runserver(mainFile, port) {
    'use strict';
    var PIPE = { stdio: 'inherit' };
    spawn('python', [mainFile, '-p', (port || 5000)], PIPE);
}

gulp.task('serve', function () {
    'use strict';
    runserver('runserver.py');
});

gulp.task('watch', function () {
    'use strict';
    livereload.listen();
    gulp.watch('<%= packageName %>/templates/**/*.html', function () {
        gulp.src('<%= packageName %>/templates/**/*.html').pipe(livereload());
    });
    gulp.watch('<%= packageName %>/static/sass/**/*.scss', ['compass']);
});

gulp.task('compass', function () {
    'use strict';
    shell.cd('<%= packageName %>/static');
    shell.exec('compass compile');
    shell.cd('../../');
    gulp.src('<%= packageName %>/static/css/**/*.css').pipe(livereload());
});

gulp.task('init-db', function () {
    'use strict';
    shell.exec('python scripts/init_db.py');
});

gulp.task('make-test-db', function () {
    'use strict';
    shell.exec('python scripts/make_test_data.py');
});

gulp.task('default', ['watch', 'serve']);
