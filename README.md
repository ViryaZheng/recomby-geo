# recomby-geo

## GEO 领域的 AI 员工开源解决方案

把 Agent、办公 CLI、GEO 专业知识 skills 整合成一套**协作型 AI 员工方案**——给你的 agent 装上 GEO skills，让它跟你的业务专家一起干 GEO 协作活儿。

> alpha · 零外部依赖 · 零 API Key  ·  [安装与使用](INSTALL.md)  ·  [English](README.en.md)

---

## 什么是「AI 员工方案」

不是「AI 替代员工」，是一个**虚拟岗位的组装产物**。四块拼起来才是 AI 员工，缺一不可：

```
       业务专家                     Agent
   （你/客户团队，懂业务）   （CC / Codex / ...，可接本地模型）
              │                        │
              └──────────── ╳ ─────────┘
                            │
              ┌─────────────┴─────────────┐
              │                           │
        办公 CLI 层                   GEO Skills
   （飞书/钉钉/Slack/Notion…）   （← 本项目的主战场）
   数据源 + 操作脚手架            专业知识赋能 agent
```

| 角色 | 提供者 | 本项目集合 / 开发 |
|------|--------|--------------------|
| 业务专家 | 你自己 / 客户团队 | — |
| Agent | CC / Codex / OpenCode / ... 生态 | ✓ 集合 → [`agents.md`](agents.md) |
| 数据 + CLI 脚手架 | 飞书 / 钉钉 / Slack / Notion ... | ✓ 集合 → [`clis.md`](clis.md) |
| **GEO Skills** | **本项目自研 + vendor 开源** | ✓ 主战场 → [`plugins/recomby-geo/skills/`](plugins/recomby-geo/skills/) |

我们做三件事：**集合主流 Agent CLI、集合国内外办公软件 CLI、封装 GEO 专业知识 skills**。

---

## 我们持续投入的主战场：GEO Skills

> **`plugins/recomby-geo/`（commands + skills + schemas）是本项目长期维护、未来持续优化的主要方向**，MIT 许可证，可商用、可修改、可分发。

我们做的事是把 GEO 领域的专业知识封装成 agent 可调用的 skills，加上完整的 7 阶段协作工作流命令——这是仓库里**我们持续投入、迭代、维护的核心资产**。其中很多结构和方法论参考了 Princeton KDD 2024、Auriti Labs、awesome-geo 等开源工作，我们做的是组装、打磨、面向 AI 员工场景重新封装。

`agents.md` 和 `clis.md` 不是产品的另一部分——它们是**方案架构说明页**：讲清楚我们的 GEO skills 在「业务专家 + Agent + 办公 CLI + Skills」这套 AI 员工方案里处于什么位置，配合哪些 agent / CLI 工作。读者可以从那两页知道生态全貌，但**主战场是 skills**。

---

## 本地化部署 · 数据不出本地

这套方案天然 **Local-first**——这是相比 SurferSEO / Frase / Clearscope 这类必须把客户数据上传到云端的 SaaS GEO 工具，最关键的差异化：

- **Agent 可接本地模型** — CC/Codex 等都支持本地 LLM（Ollama / vLLM / LM Studio）
- **办公数据不出本地** — 飞书/钉钉等 CLI 在你自己的环境里跑，业务数据不上第三方云
- **整套方案开源** — vendor 的 skills 全部 MIT / Apache 2.0，可审计、可定制
- **合规友好** — 国内数据合规、敏感行业、内部资料场景刚需

---

## GEO Skills 清单（核心）

`plugins/recomby-geo/skills/` 下封装了 6 个 GEO 专业知识 skill，**模型根据 description 自动匹配调用**——你不直接调用它们：

| Skill | 来源 | 用途 |
|-------|------|------|
| `seo-geo-optimizer` | [199-biotechnologies](https://github.com/199-biotechnologies/claude-skill-seo-geo-optimizer) (MIT) | 主力，13 个 Python 脚本 |
| `content-writer` | [toprank](https://github.com/nowork-studio/toprank) (MIT) | 内容生产 |
| `content-quality-auditor` | [aaron-he-zhu](https://github.com/aaron-he-zhu/seo-geo-claude-skills) (Apache 2.0) | E-E-A-T / 引用度审计 |
| `internal-linking-optimizer` | aaron-he-zhu (Apache 2.0) | 内链优化 |
| `keyword-research` | toprank (MIT) | 关键词扩展 |
| `meta-tags-optimizer` | toprank (MIT) | 标题 / Meta |

加上 `plugins/recomby-geo/commands/` 下 7 个我们自研的 GEO 工作流命令（`/01-intake` 到 `/07-reaudit`），共同构成完整的 GEO AI 员工能力包。**这就是我们对外开源的核心产物。**

许可证详见 [`LICENSE`](LICENSE) 与 [`THIRD_PARTY_LICENSES.md`](THIRD_PARTY_LICENSES.md)。

---

## 配套生态：Agent + 办公 CLI

GEO Skills 装在哪个 agent、跟哪些办公 CLI 配合——这两份是**方案架构说明**，不是产品：

- **[Agent 集合 → `agents.md`](agents.md)** — 主流可加载 skills 的 AI agent CLI：CC、Codex CLI、OpenCode、Cline、Goose、字节 Trae 等
- **[办公 CLI 集合 → `clis.md`](clis.md)** — 让 agent 接客户业务数据：飞书 / 钉钉 / 企微 / 语雀（国内）+ Slack / Notion / GitHub / Linear / Google Workspace / Jira（国外）

两份让你看清整套 AI 员工方案的全貌（agent 是身体、办公 CLI 是手脚），但**核心要装的是 GEO Skills 本身**。

---

## 为什么 GEO 是验证「AI 员工」范式的最佳战场

GEO 天然**不能全自动化**——这是优势：

- 大模型搜索引擎主动惩罚 AI 拼水文，必须有真实业务洞察才被引用
- 业务洞察只能由业务专家贡献，AI 替代不了
- 所以「AI 员工」在 GEO 场景里**只能是协作型**，「AI 替代员工」的伪命题不存在

带来：客户决策方一听就懂、落地阻力小（业务专家不会有被替代恐惧）、价值归属清晰。

GEO 是协作型 AI 员工范式的最佳演示场。

---

## 上手

```bash
# 1. 在 Claude Code 中安装本插件（GEO Skills + 7 阶段工作流命令）
/plugin marketplace add recomby-ai/recomby-geo
/plugin install recomby-geo

# 2. 准备你的项目目录
mkdir -p clients/<your-project>/inputs
# 把业务资料（PDF / URL / notes）放进 inputs/

# 3. 启动协作工作流
/01-intake clients/<your-project>
# 按提示依次：/02-audit → /03-gap → /04-content-brief → ...
```

完整运行流程图：[`plugins/recomby-geo/orchestrator/run.md`](plugins/recomby-geo/orchestrator/run.md)

> **不用 Claude Code？** —— 在其他支持 skill/plugin 加载的 agent（见 [`agents.md`](agents.md)）里手动拷贝 `plugins/recomby-geo/skills/` 即可加载。

---

## 协作工作流（业务专家视角）

完整 GEO 工作流 7 个阶段，**重点是中段的「专家填写 brief」**——agent 准备好框架，业务洞察必须由你填进去。这是 AI 员工协作本质的体现：

```
  /01-intake → /02-audit → /03-gap → /04-content-brief
                                            │
                                  ┌─────────┘
                                  ▼
                       [业务专家填写洞察槽位]
                                  │
                                  ▼
  /05-production → /06-distribution → 发布 → 7 天后 /07-reaudit
```

各阶段命令文档：[`plugins/recomby-geo/commands/`](plugins/recomby-geo/commands/)

**关键约束**：
- `/05-production` 在 brief 状态不是 `ready-for-production` 时硬拒绝——专家槽位没填完，agent 不会自动用 AI 内容代填。这是协作的硬门槛。
- `/02-audit` 用无客户上下文的子 agent 跑可见性基线，模拟陌生用户对 AI 引擎的真实提问。
- 所有阶段输出通过 JSON Schema 校验后才进入下一阶段。

---

## 项目布局

```
recomby-geo/
├── README.md                         # 本文件（中文）
├── README.en.md                      # 英文版
├── agents.md                         # Agent 集合（curated list）
├── clis.md                           # 国内外办公 CLI 集合
├── plugins/recomby-geo/
│   ├── plugin.json
│   ├── orchestrator/run.md           # 完整运行流程图
│   ├── commands/                     # 7 个工作流命令
│   ├── skills/                       # 6 个 vendor skills（主战场）
│   ├── schemas/                      # 4 个 JSON Schema
│   └── references/                   # Princeton GEO 方法论等参考
├── THIRD_PARTY_LICENSES.md
└── .gitignore
```

技术细节、Schema 契约、接手 agent 须知：见 [`README.en.md`](README.en.md)。

---

## License

本仓库由 Recomby.ai 维护，未来持续投入的主要方向是 `plugins/recomby-geo/`（commands、4 个 Schema、orchestrator、skills 选集）以及 agents.md / clis.md 两份方案架构页——这些组合方式与封装由我们完成（许多原始内容引自开源社区，见下文与 `THIRD_PARTY_LICENSES.md`），整体采用 **MIT** 许可证，详见 [`LICENSE`](LICENSE)。

6 个 vendor skills 保留原始许可证（MIT / Apache 2.0），详见 [`THIRD_PARTY_LICENSES.md`](THIRD_PARTY_LICENSES.md)。

---

## 工作流参考

完整 7 阶段运行流程图与契约：[`plugins/recomby-geo/orchestrator/run.md`](plugins/recomby-geo/orchestrator/run.md)（single source of truth）。
