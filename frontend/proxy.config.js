const target = 'http://31.129.108.243'

const PROXY_CONFIG = [
  {
    context: ['/auth/api'],
    target,
    secure: true,
    changeOrigin: true,
    logLevel: 'debug',
    configure: (proxy) => {
      proxy.on("error", (err) => {
        console.log("proxy error", err);
      });
      proxy.on("proxyReq", (proxyReq, req) => {
        const headers = proxyReq.getHeaders();
        console.log(
          req.method,
          req.url,
          // " -> ",
          // `${headers.host}${proxyReq.path}`,
        );
      });
      proxy.on("proxyRes", (proxyRes, req) => {
        console.log(
          req.method,
          "Target Response",
          proxyRes.statusCode,
          ":",
          req.url,
        );
      });
    }
  },
];

module.exports = PROXY_CONFIG;
