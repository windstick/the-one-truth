module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://39.104.20.38:8000',
        changeOrigin: true,
        // ws: true,
        pathRewrite: { 
          '^/api': ''
        }
      }
    }
  }
}