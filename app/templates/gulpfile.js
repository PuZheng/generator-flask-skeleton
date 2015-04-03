var gulp = require('gulp');
var spawn = require('child_process').spawn;
var shell = require('shelljs');
var livereload = require('gulp-livereload');

function runserver(mainFile, port) {
    'use strict';
    spawn('python', [mainFile, '-p', (port || 5000)], 
          { 
              stdio: 'inherit',
              cwd: '<%= packageName %>',
          });
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
    spawn('python', ['scripts/init_db.py'], 
          { 
              stdio: 'inherit',
              cwd: '<%= packageName %>',
          });
});

gulp.task('make-test-db', function () {
    'use strict';
    spawn('python', ['scripts/make_test_data.py'], 
          { 
              stdio: 'inherit',
              cwd: '<%= packageName %>',
          });
});

gulp.task('default', ['watch', 'serve']);
