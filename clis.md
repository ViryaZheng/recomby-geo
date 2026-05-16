# 办公 CLI 集合

让 agent 接入业务数据 + 操作客户协作空间的**命令行工具**列表，作为 AI 员工方案的「数据源 + 操作脚手架」一层。

CLI 是 agent（CC / Codex / Cline / Goose 等）通过 Bash 工具最自然的接入方式——任何 agent 只要能调 shell 就能用，不依赖额外协议层和配置。MCP 是补充。

> 📌 信息基于 2025-2026 自动调研，链接与许可证以官方页面为准。欢迎 PR 补充 / 勘误。
>
> **Verified: 2026-05** — 所有条目最后核对于此日期；提交新条目 / 勘误时请同步更新自己条目的 verified 日期。

---

## 国内

| 产品 | CLI | 来源 | 安装 | 链接 | MCP 备注 |
|------|-----|------|------|------|---------|
| **飞书 (Lark)** | `lark-cli` | 官方 | `npm i -g @larksuite/cli` | [larksuite/cli](https://github.com/larksuite/cli) | 同组织 [lark-openapi-mcp](https://github.com/larksuite/lark-openapi-mcp) 官方 MCP 可选用 |
| **钉钉 (DingTalk)** | `dws` | 官方 | `npm i -g @dingtalk/cli` | [DingTalk-Real-AI/dingtalk-workspace-cli](https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli) | AI-native 设计，跳过确认 + 审计全链 |
| **语雀 (Yuque)** | `yuque-cli` | 官方 | `npm i -g yuque-cli` | [yuque/yuque-cli](https://github.com/yuque/yuque-cli) | 同组织 [yuque-mcp-server](https://github.com/yuque/yuque-mcp-server) 官方 MCP 可选用 |
| **企业微信** | — | 无官方 | — | — | 仅社区 MCP：[shellus/qiye_wechat_mcp](https://github.com/shellus/qiye_wechat_mcp) |
| **微信（个人）** | `wechaty` (SDK) | 社区 | `npm i wechaty` | [wechaty/wechaty](https://github.com/wechaty/wechaty) | 个人微信无官方开放，wechaty 是 SDK 非 CLI |

---

## 国外

| 产品 | CLI | 来源 | 安装 | 链接 | MCP 备注 |
|------|-----|------|------|------|---------|
| **GitHub** | `gh` | 官方 | `brew install gh` | [cli/cli](https://github.com/cli/cli) | 官方 [github-mcp-server](https://github.com/github/github-mcp-server) 基于 `gh` |
| **Slack** | `slack` | 官方 | `npm i -g @slack/cli` | [slackapi/slack-cli](https://github.com/slackapi/slack-cli) | 官方 [Slack MCP](https://docs.slack.dev/ai/slack-mcp-server/) 可选用 |
| **Atlassian (Jira / Confluence)** | `jira-cli` | 社区主流 | `brew install jira-cli` | [ankitpokhrel/jira-cli](https://github.com/ankitpokhrel/jira-cli) | 官方 [atlassian-mcp-server](https://github.com/atlassian/atlassian-mcp-server) 可选用 |
| **Microsoft 365** | `m365` | 社区主流 (PnP) | `npm i -g @pnp/cli-microsoft365` | [pnp/cli-microsoft365](https://github.com/pnp/cli-microsoft365) | 官方 Work IQ MCP 可选用 |
| **Google Workspace** | `clasp` (Apps Script) | 官方 | `npm i -g @google/clasp` | [google/clasp](https://github.com/google/clasp) | Workspace 完整面用[官方 MCP](https://developers.google.com/workspace/guides/configure-mcp-servers) |
| **Notion** | — | 无官方 | — | — | 官方策略 API-first；用[官方 MCP](https://developers.notion.com/docs/mcp) |
| **Linear** | — | 无官方 | — | — | 官方策略 API-first；用[官方 MCP](https://linear.app/docs/mcp) |
| **ClickUp** | — | 社区废弃 | — | — | 用 [官方 MCP](https://developer.clickup.com/docs/connect-an-ai-assistant-to-clickups-mcp-server) |
| **Asana** | — | 社区不活跃 | — | — | 仅社区 MCP |

---

## 选型建议

按本项目 **CLI 优先 · 官方维护优先 · 数据不出本地** 原则：

| 客户类型 | 首选 |
|----------|------|
| 国内一般企业 | **飞书 `lark-cli`** + **钉钉 `dws`** |
| 国内技术团队 / 知识库重 | **语雀 `yuque-cli`** + **飞书 `lark-cli`** |
| 国外 SaaS 重度用户 | **Slack `slack`** + **GitHub `gh`** + Notion MCP |
| 跨国企业 | **Microsoft 365 `m365`** + Google Workspace MCP |
| 研发驱动型 | **GitHub `gh`** + **Jira `jira-cli`** + Linear MCP |

---

## 为什么 CLI 优先（而不是 MCP）

- **通用性**：CLI 工具任何 agent 通过 Bash 都能调，不需要 agent 内置 MCP client
- **可观测性**：CLI 输出是文本流，agent 直接读懂；MCP 调用是 JSON-RPC，调试链路长
- **本地化天然**：CLI 工具直接在你的环境跑，跟「数据不出本地」对齐
- **生态成熟**：shell 工具链是几十年沉淀，错误处理 / 重试 / pipe 都成熟

**MCP 是补充**：对 API-first 的产品（Notion、Linear、ClickUp 这种没官方 CLI 的），MCP 是接入路径；对有完整 CLI 的产品（飞书、钉钉、GitHub），CLI 更直接。

---

## 贡献

新增 / 勘误：提交 PR 修改本文件。每条请提供：产品名、CLI 名（或"无"）、来源（官方 / 社区主流 / 社区不活跃 / 无）、安装命令、GitHub 链接、可选 MCP 备注。同步更新自己条目的 verified 日期。
