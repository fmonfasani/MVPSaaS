module.exports = (cfg) => {
  cfg.addPassthroughCopy("src/assets");
  return {
    dir: { input:"web/src", output:"web/dist", includes:"_includes", data:"_data" },
    pathPrefix: "/MVPSaaS/",
  };
};
