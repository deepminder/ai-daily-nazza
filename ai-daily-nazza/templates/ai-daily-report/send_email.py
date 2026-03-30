#!/usr/bin/env python3
"""
Send AI Daily Report HTML + PDF to specified email via SMTP
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from datetime import datetime
import re

# Configuration
SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 465
SENDER_EMAIL = "your-email@qq.com"      # 请修改为你的发件邮箱
RECEIVER_EMAIL = "receiver@example.com"  # 请修改为你的收件邮箱
PASSWORD = "your-smtp-authorization-code" # 请修改为你的SMTP授权码

def extract_summary(md_path):
    """Extract key highlights from the markdown report"""
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract core intelligence summary
        summary = ""
        if "## 一、今日核心情报摘要" in content:
            start = content.find("## 一、今日核心情报摘要")
            end = content.find("## 二、")
            if end == -1:
                end = content.find("## 三、")
            if end == -1:
                end = len(content)
            section = content[start:end]
            # Clean up heading
            section = section.replace("## 一、今日核心情报摘要（Executive Summary）", "").replace("## 一、今日核心情报摘要", "").strip()
            summary = section
        else:
            summary = "无法提取核心摘要，请查看附件完整报告。"
        
        # Truncate if too long
        if len(summary) > 800:
            summary = summary[:800] + "\n...(详见附件完整报告)"
        
        return summary
    except Exception as e:
        return f"提取摘要失败: {str(e)}"

def send_email(html_path, pdf_path, md_path):
    today = datetime.now().strftime("%Y年%m月%d日")
    
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = f"【哪吒】全球AI产业日报 | {today}"
    
    # Extract summary from markdown
    summary = extract_summary(md_path)
    
    # Email body
    body = f"""报告玉帝，

今日（{today}）的《全球AI产业日报》已生成完成，包含 HTML 和 PDF 两种格式，详见附件。

---

【核心情报摘要】

{summary}

---

【说明】
- 搜索范围：昨日全天 + 过去 72 小时全球AI产业重大新闻
- 特别关注：已优先收集国内顶级AI企业（百度、阿里、腾讯、字节、智谱、DeepSeek、华为等）最新进展
- 产出：严格遵循 10 大板块结构，包含多组对比表格，关键数据加粗标注，信源引用规范
- 格式：HTML 可直接浏览器打开，PDF 适合存档分享

本邮件由哪吒三智能体团队自动生成，微臣（ArkClaw）代为递呈。

-- 哪吒
"""
    msg.attach(MIMEText(body, 'plain'))
    
    # Attach HTML
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    html_part = MIMEText(html_content, 'html')
    html_part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(html_path)}"')
    msg.attach(html_part)
    
    # Attach PDF
    with open(pdf_path, 'rb') as f:
        pdf_content = f.read()
    pdf_part = MIMEBase('application', 'pdf')
    pdf_part.set_payload(pdf_content)
    encoders.encode_base64(pdf_part)
    pdf_part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(pdf_path)}"')
    msg.attach(pdf_part)
    
    # Send
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(SENDER_EMAIL, PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
    
    print(f"Email sent successfully to {RECEIVER_EMAIL}")
    return True

import sys

if __name__ == "__main__":
    if len(sys.argv) == 4:
        html_path = sys.argv[1]
        pdf_path = sys.argv[2]
        md_path = sys.argv[3]
    elif len(sys.argv) == 3:
        html_path = sys.argv[1]
        pdf_path = sys.argv[2]
        # guess md path
        md_path = html_path.replace('.html', '.md').replace('-v3', '').replace('-v2', '').replace('-v1', '')
    else:
        today = datetime.now().strftime("%Y-%m-%d")
        html_path = f"/root/.openclaw/workspace/ai-daily-report/shared/artifacts/global-ai-daily-report-{today}-v3.html"
        pdf_path = f"/root/.openclaw/workspace/ai-daily-report/shared/artifacts/global-ai-daily-report-{today}-v3.pdf"
        md_path = f"/root/.openclaw/workspace/ai-daily-report/shared/artifacts/global-ai-daily-report-{today}-v3.md"
    
    if not os.path.exists(html_path):
        print(f"HTML file not found: {html_path}")
        exit(1)
    if not os.path.exists(pdf_path):
        print(f"PDF file not found: {pdf_path}")
        exit(1)
    if not os.path.exists(md_path):
        print(f"MD file not found: {md_path}")
        exit(1)
    
    try:
        send_email(html_path, pdf_path, md_path)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")
        exit(1)
