# 挂号接口测试示例

这是技术文章配套的**独立教学示例**，不连接云脑诊疗平台，也不代表原项目的接口、实现或测试覆盖率。数据只存在内存中；不含鉴权、持久化和支付。

运行环境：Python 3.10+。

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

测试会为每个用例启动独立的本地服务和数据，覆盖创建预约、必填项缺失、相同请求重复发送、去重键冲突、号源耗尽和两个请求竞争一个号源。所有 HTTP 请求都设置超时。

对应文章：[用 pytest 搭一组可复现的接口测试](../../tech/pytest-api-tests.html)。
