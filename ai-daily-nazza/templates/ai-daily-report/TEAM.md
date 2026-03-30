# 哪吒三智能体 - 全球AI产业日报团队

## 团队架构

### 三智能体分工协作

| 角色 | 位置 | 核心职责 |
|------|------|----------|
| 🔍 **Researcher** | `agents/researcher/` | 每日搜索收集过去 **24/72 小时** 全球AI产业新闻，按十大板块分类整理，标注信源和可信度 |
| 📝 **Reporter** | `agents/reporter/` | 读取 Researcher 的素材，按照固定提示词格式生成完整的《全球AI产业日报》，严格遵循 10 大板块结构 |
| 📤 **Publisher** | `agents/publisher/` | 将 Markdown 通过 **pandoc → wkhtmltopdf** 两步转换为 HTML + PDF，发送邮件，正文包含核心摘要 |
| 🎯 **Orchestrator** | 主会话 | 每日调度任务，跟踪流程，处理异常，报告结果 |

---

## 工作流

```
用户触发（或定时 每天上午 7:00 UTC+8）
    ↓
Orchestrator → 启动今日 Researcher 任务
    ↓
Researcher → 搜索收集全球AI产业新闻 → /shared/specs/
    ↓
Reporter → 根据素材生成日报 → /shared/artifacts/ (.md)
    ↓
Publisher → Markdown → HTML → PDF → 发送邮件（正文核心摘要 + 附件完整报告）
    ↓
Orchestrator → 标记完成，通知用户
```

---

## 完整十大板块结构

1. **一、今日核心情报摘要** - 市场脉冲、技术突破、地缘政治三段式
2. **二、大模型生态动态** - 技术规格对比表
3. **三、AI开发生态** - 开发工具范式演进表
4. **四、算力与芯片** - 出货量预测表
5. **五、AI Agent** - 框架对比表
6. **六、具身智能与机器人** - 关键指标表
7. **七、AI投融资** - 大额交易表
8. **八、政策与监管** - 硬法约束表
9. **九、技术趋势洞察** - 产业深度分析
10. **十、未来重要时间节点** - 事件雷达表

---

## 配置说明

### 邮件配置

编辑 `send_email.py` 修改：

```python
SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 465
SENDER_EMAIL = "your-email@qq.com"
RECEIVER_EMAIL = "receiver@example.com"
PASSWORD = "your-smtp-authorization-code"
```

### 依赖安装

```bash
pip install markdown
apt install wkhtmltopdf
```

---

**哪吒三智能体** 🐉
- 三智能体分工协作，专业事情交给专业智能体
- 保证信息收集广度 + 报告撰写深度 + 格式输出规范
