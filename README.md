# emantery 的项目与测试实践

2027 届校招作品集，聚焦软件测试、测试开发和 AI 产品测试。首页展示项目经历、验证思路与明确标注的学习路线；技术文章中的独立教学示例不算原项目成果。

## 当前内容

- 云脑诊疗平台、Linux 棋牌游戏、图书管理系统三个项目
- 挂号/缴费、AI 导诊、业务状态等验证思路
- 测试开发学习路线：接口自动化、UI 自动化、持续集成
- [技术总结](./tech/)：挂号接口测试设计、pytest 接口自动化、AI 应用分层测试、Playwright 页面冒烟检查、SQL 状态核对
- [可运行的接口示例](./examples/appointment-api/)、[本站页面测试](./examples/site-smoke/)与[SQL 状态检查](./examples/sql-state-check/)
- 实际发布的更新记录

## 访问地址

<https://emantvery.github.io>

## 技术实现

网站本身使用零依赖静态 HTML、CSS 与 JavaScript；推送到 `main` 后由 GitHub Actions 部署到 GitHub Pages。示例代码分别使用 Python/pytest、Node.js/Playwright 和 Python 标准库 SQLite，安装与运行方法见各自 README。
