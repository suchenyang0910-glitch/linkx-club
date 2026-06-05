const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './tests/e2e',
  retries: 1,
  use: {
    baseURL: 'http://localhost:3034',
    trace: 'on-first-retry'
  },
  webServer: {
    command: 'node article-server.js',
    port: 3034,
    reuseExistingServer: true
  }
});
