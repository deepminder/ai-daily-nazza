---
name: ai-daily-nazza
description: 哪吒三智能体全球AI产业日报周报自动生成工作流 - 支持每日自动收集AI新闻、撰写完整报告、转换格式并发送邮件
---

# 🤖 ai-daily-nazza - 哪吒三智能体AI日报周报工作流

##  when to use 何时使用

当用户需要：
- 每日自动生成《全球AI产业日报》
- 每周生成AI产业周报
- 多智能体分工协作完成：搜索收集新闻 → 撰写完整报告 → 转换格式发送邮件
- 需要完整的十大板块结构，包含多个对比表格
- 自动发送邮件到指定邮箱

本技能实现了三智能体分工协作架构：
- **🔍 Researcher** - 搜索收集过去 24/72 小时全球AI产业新闻，按十大板块整理
- **📝 Reporter** - 根据素材按照固定格式生成完整深度报告
- **📤 Publisher** - Markdown → HTML → PDF 转换，发送邮件
- **🎯 Orchestrator** - 流程编排（主会话）

## 工作流程

### 完整流程

```
用户请求生成AI日报 → 
  ↓
启动 Researcher 子智能体
  ↓
搜索收集过去72小时AI产业新闻（按十大板块分类 → 保存到 `/shared/specs/`
  ↓
启动 Reporter 子智能体
  ↓
按照提示词模板生成完整十大板块日报 → 保存到 `/shared/artifacts/`
  ↓
转换为 HTML + PDF
  ↓
发送邮件（正文包含核心摘要，附件包含完整报告
  ↓
完成通知用户
```

### 目录结构

```
ai-daily-report/
├── TEAM.md                          # 团队说明文档
├── agents/
│   ├── researcher/SOUL.md          # 搜索者角色定义
│   ├── reporter/SOUL.md            # 撰写者角色定义
│   └── publisher/SOUL.md         # 发布者角色定义
├── shared/
│   ├── specs/
│   │   └── daily-report-prompt.md  # 日报提示词模板
│   └── artifacts/                  # 输出目录（HTML + PDF）
└── send_email.py                   # SMTP邮件发送脚本
```

## 使用说明

### 1. 初始化项目

首次使用时，创建项目结构：

```bash
mkdir -p ai-daily-report/agents/{researcher,reporter,publisher}
mkdir -p ai-daily-report/shared/{specs,artifacts}
```

### 2. 配置邮件配置

编辑 `send_email.py` 修改邮件配置：

```python
# Configuration
SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 465
SENDER_EMAIL = "your-email@qq.com"
RECEIVER_EMAIL = "receiver@example.com"
PASSWORD = "your-smtp-password"
```

### 3. 生成日报（完整流程）

当用户要求生成今日AI日报时：

1. **启动 Researcher**:
```python
{
  "task": "你是AI产业研究员，请完成以下任务：\n\n1. 使用 web_search 搜索过去 72 小时（YYYY-MM-DD 至 YYYY-MM-DD 全球AI产业重大新闻\n2. 按照十大板块分类整理...\n3. 结果写入：/root/.openclaw/workspace/ai-daily-report/shared/specs/daily-research-YYYY-MM-DD.md\n",
  "runtime": "subagent",
  "label": "ai-daily-researcher",
  "cwd": "/root/.openclaw/workspace/ai-daily-report"
}
```

2. **Researcher 完成后**，启动 Reporter：**
```python
{
  "task": "你是AI产业日报撰稿人，请完成以下任务：\n\n1. 读取素材文件...\n2. 严格按照 daily-report-prompt.md 格式要求生成...\n3. 输出文件：...\n",
  "runtime": "subagent",
  "label": "ai-daily-reporter",
  "cwd": "/root/.openclaw/workspace/ai-daily-report"
}
```

3. **Reporter 完成后**，转换格式并发送邮件：**

```bash
# 转换为 HTML
python convert.py

# 转换为 PDF
wkhtmltopdf --enable-local-file-access --page-size A4 ... output.html output.pdf

# 发送邮件
python send_email.py html-path pdf-path md-path
```

## 日报格式要求（十大板块

输出必须包含：

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

字数要求：**3500-6000 字，包含多个 Markdown 表格，关键数据加粗，信源标注。

## 周报生成

周报生成流程类似，只需：
- 搜索范围改为过去 7 天
- 增加周度总结分析
- 标题格式不变

## 依赖要求

- 需要 `send_email.py 已配置 SMTP
- 需要 `wkhtmltopdf` 已安装（用于 PDF 转换）
- 需要 `python-markdown` 包已安装
- 需要 `web_search` 技能可用

## 作者

ArkClaw 哪吒三智能体工作流 🐉
