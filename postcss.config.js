module.exports = {
  map: { inline: false },
  plugins: [
    require("pixrem")(),
    require("autoprefixer")(),
    require("postcss-preset-env")({ stage: 0 }),
    require("css-mqpacker")({ sort: true }),
    require("cssnano")({ zindex: false }),
    require("@fullhuman/postcss-purgecss")({
      content: ["./**/*.html"],
      safelist: [
        /^nav-level-\d$/,
        /^slide-label-\d$/,
        /^slide-\d$/,
        /^block-/,
        /^field-/,
        "richtext-image",
        "left",
        "right",
      ],
      skippedContentGlobs: ["node_modules/**", ".direnv/**"],
    }),
  ],
};
