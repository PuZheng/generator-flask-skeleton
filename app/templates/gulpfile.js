var gulp = require('gulp')
    , spawn = require('child_process').spawn
    , compass = require('gulp-compass')
    , shell = require('shelljs')
    , livereload = require('gulp-livereload');

function runserver(mainFile, port) {
    var PIPE = { stdio: 'inherit' };
    spawn('python', [mainFile, '-p', (port || 5000)], PIPE);
}

gulp.task('serve', function () {
    runserver('<%= packageName %>/runserver.py')
});

gulp.task('watch', function () {
    livereload.listen();
    gulp.watch('<%= packageName %>/templates/**/*.html', function () {
        gulp.src('<%= packageName %>/templates/**/*.html').pipe(livereload());
    });
    gulp.watch('<%= packageName %>/static/sass/**/*.scss', ['compass'])
});

gulp.task('compass', function () {
    shell.cd('<%= packageName %>/static');
    shell.exec('compass compile');
    shell.cd('.././');
    gulp.src('static/css/**/*.css').pipe(livereload());
});

gulp.task('init-db', function () {
    shell.exec('python <%= packageName %>/scripts/init_db.py');
});

gulp.task('make-test-db', function () {
    shell.exec('python <%= packageName %>/scripts/make_test_data.py');
});

gulp.task('default', ['watch', 'serve'])
