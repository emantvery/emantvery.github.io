# Playwright 页面冒烟检查

这是博客本身的独立教学示例：检查文章入口、手机菜单、锚点、明暗主题与页面横向溢出。它不代表云脑诊疗平台已完成 UI 自动化。

在本目录执行：

```bash
npm install
npx playwright install chromium
npm test
```

如果已安装 Chrome，可设置 `CHROME_PATH` 为 Chrome 可执行文件路径后运行 `npm test`，无需再下载浏览器。测试会自动启动本地 HTTP 服务，模拟 GitHub Pages 对目录链接的解析，不依赖线上网络。对应文章：[从稳定定位到页面冒烟检查](../../tech/playwright-ui-tests.html)。
