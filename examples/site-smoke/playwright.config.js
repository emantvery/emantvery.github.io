const { defineConfig } = require("playwright/test");
const path = require("node:path");

module.exports = defineConfig({
  testDir: __dirname,
  testMatch: "*.spec.js",
  timeout: 15000,
  use: {
    baseURL: "http://127.0.0.1:8766",
    browserName: "chromium",
    launchOptions: {
      executablePath: process.env.CHROME_PATH || undefined,
    },
  },
  webServer: {
    command: `"${process.execPath}" "${path.join(__dirname, "server.js")}"`,
    cwd: path.dirname(process.execPath),
    url: "http://127.0.0.1:8766",
    reuseExistingServer: !process.env.CI,
    timeout: 10000,
  },
  reporter: "list",
});
