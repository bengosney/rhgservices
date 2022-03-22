const gulp = require("gulp");
const debug = require("gulp-debug");

gulp.task("css", () => {
  const dartSass = require("sass");
  const gulpSass = require("gulp-sass");
  const postcss = require("gulp-postcss");
  const sourcemaps = require("gulp-sourcemaps");
  const autoprefixer = require("autoprefixer");
  const cssnano = require("cssnano");
  const combine_media_query = require("postcss-combine-media-query");
  const postcssPresetEnv = require("postcss-preset-env");
  const inlineimage = require("gulp-inline-image");

  const purify = require("gulp-purifycss");

  const sass = gulpSass(dartSass);

  return (
    gulp
      .src("./scss/*.scss")
      .pipe(sourcemaps.init())
      .pipe(sass.sync())
      .pipe(inlineimage())
      //.pipe(purify(["**/!(vendor|node_modules)/*.{html,js}"]))
      .pipe(postcss([postcssPresetEnv({ stage: 0 }), autoprefixer(), combine_media_query()]))
      .pipe(postcss([cssnano()]))
      .pipe(sourcemaps.write("/"))
      .pipe(gulp.dest("rhgs/static/css/"))
  );
});

gulp.task("img", () => {
  const gulpAvif = require("gulp-avif");

  return gulp
    .src("media/**/*.{png,jpg}")
    .pipe(debug())
    .pipe(
      gulpAvif({
        speed: 0,
        quality: 60,
      })
    )
    .pipe(gulp.dest("./static/img/"));
});

gulp.task("default", () => {
  const browserSync = require("browser-sync").create();

  browserSync.init({
    proxy: "localhost:8000",
  });

  gulp.watch("scss/**/*.scss", gulp.series("css"));
  gulp.watch("rhgs/static/css/**/*.css").on("change", browserSync.reload);
  gulp.watch("**/templates/**/*.html").on("change", browserSync.reload);
});
gulp.task("build", () => gulp.parallel("css", "img"));
