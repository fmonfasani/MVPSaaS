module.exports = (cfg) => {
  cfg.addPassthroughCopy("src/assets");
  return { dir: { input:"src", output:"dist", includes:"_includes", data:"_data" } };
};
