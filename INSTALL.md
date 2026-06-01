# 安装与使用

同一套源码同时支持 **Claude Code** 和 **OpenAI Codex CLI**——一份 `skills/`、
一份阶段规程（`plugins/recomby-geo/commands/` + `orchestrator/run.md`，两端共享
的单一逻辑源），各自一个 manifest。

> alpha · 零外部依赖 · 零 API Key（默认流程）· [English README](README.en.md)

---

## Claude Code

```bash
# 在 Claude Code 会话里
/plugin marketplace add recomby-ai/recomby-geo
/plugin install recomby-geo
```

装好后是 7 个**裸斜杠命令**，按顺序驱动流程：

```
/01-intake clients/<slug>
/02-audit  clients/<slug>
/03-gap    clients/<slug>
/04-content-brief clients/<slug> --priority <id>
#   [业务专家填写 briefs/<id>.html 或 .md 里的 REQUIRED-FILL 槽位]
/05-production    clients/<slug> --priority <id>
/06-distribution  clients/<slug> --priority <id>
#   [发布，等待 7+ 天]
/07-reaudit clients/<slug>
```

## OpenAI Codex CLI

Codex 没有裸斜杠命令，入口是 **`geo-pipeline` skill**——它承载编排规则并路由到
各阶段规程。

```bash
codex plugin marketplace add ./        # 读 .agents/plugins/marketplace.json
# 或从远程仓库：
codex plugin marketplace add recomby-ai/recomby-geo
```

装好后在会话里用自然语言驱动各阶段（`geo-pipeline` 按 description 自动触发）：

```
「在 clients/<slug> 上跑 GEO intake 阶段」      → 触发 geo-pipeline → 执行 01-intake
「audit 这个客户的 AI 搜索可见性」              → 02-audit
…依此类推，到 07-reaudit
```

`geo-pipeline` 会读对应的 `commands/0X-*.md` 执行，并显式跑 Schema 校验
（Codex 无内置 Schema 校验，靠 `jsonschema` 跑 `schemas/*.schema.json`）。

## 仓库为什么有两个 manifest

| 文件 | runtime | skills 声明方式 |
|------|---------|----------------|
| `plugins/recomby-geo/plugin.json` | Claude Code | 显式数组（8 个，**不含** `geo-pipeline`，因为有裸命令） |
| `plugins/recomby-geo/.codex-plugin/plugin.json` | Codex CLI | `skills: "./skills/"`（扫描目录，**含** `geo-pipeline`） |

一份 `skills/` 目录，两端共享，零重复。marketplace 同理：
`.claude-plugin/marketplace.json`（Claude）与 `.agents/plugins/marketplace.json`
（Codex）并存。

## 7 阶段流程

```
inputs/ → 01-intake → 02-audit → 03-gap → 04-content-brief
        → [业务专家填写 brief] → 05-production → 06-distribution
        → [发布 + 等待] → 07-reaudit（每月）→ 喂给下一轮 03-gap
```

完整目录约定与依赖图见 [`plugins/recomby-geo/orchestrator/run.md`](plugins/recomby-geo/orchestrator/run.md)。

## 硬规则（两端一致）

1. **brief 由业务专家填，绝不由 AI 填。** `05-production` 在 brief 状态
   ≠ `ready-for-production` 时拒绝运行。自动填 REQUIRED-FILL 槽位会摧毁人在环
   护城河——专家不在时暂停流程，不要自动填。
2. **每阶段产物先过 `schemas/*.schema.json` 校验**再进入下一阶段（Draft 2020-12）。
3. **一个客户一个文件夹** `clients/<slug>/`，不跨文件夹共享 JSON（`clients/` 含客户
   数据，不要纳入版本控制）。
4. **绝不乱序运行阶段**（见依赖图）。

## 依赖

`python3`（skills 的脚本需要）；`pip install jsonschema`（Schema 校验步骤需要）。
两端依赖一致。
