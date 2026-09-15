# 论文投稿助手

辅助注册期刊账号、整理稿件资料和填写投稿表单的 Codex skill，包含 Elsevier 与 IEEE TIM 的流程参考。

## 功能

- 读取当前期刊指南与表单，区分出版社统一身份、期刊账号及 ORCID。
- 从作者 YAML 和稿件资料整理必填字段，核查缺项与冲突。
- 根据中文、英文、简称或模糊研究方向匹配网页实际提供的专业分类。
- 辅助上传材料、核对作者与声明、保存草稿，并记录真实操作阶段以便续办。
- 用本地 Python 脚本检查作者关联、资料完整性、文件路径及指定期刊规则。

正式提交、公开预印本与付费操作按用户明确授权执行。历史实例和本地检查结果不能证明当前网页已填写或稿件已满足投稿条件。

## 安装与使用

使用者在自己的 Codex 中安装，并提供自己的作者资料、论文及期刊账号。

### 1. 安装 skill

把下面这句话发给 Codex：

```text
使用 $skill-installer 安装这个仓库中的 skill：
https://github.com/735034777/journal-submission-assistant
SKILL.md 位于仓库根目录。
```

安装后若未显示，重启 Codex。官方支持从其他 GitHub 仓库安装 skill，见 [OpenAI 安装说明](https://learn.chatgpt.com/docs/build-skills)。

也可以在已安装 Git 的 macOS / Linux 终端中手动安装；目标目录应尚不存在：

```sh
mkdir -p ~/.agents/skills
git clone https://github.com/735034777/journal-submission-assistant.git \
  ~/.agents/skills/journal-submission-assistant
```

这里使用当前官方文档列出的用户级目录 `~/.agents/skills`。若已经通过安装器安装并被 Codex 识别，无需再手动安装一份。

### 2. 准备自己的资料

- 注册账号：提供目标期刊、姓名、邮箱、称谓、国家或地区、单位和研究方向，具体必填项以当前注册页面为准。
- 填写投稿草稿：再提供论文文件、作者名单与顺序、通讯作者、单位、基金及声明信息。缺项由助手集中询问。

可以直接提供资料，也可以让 Codex 把 [作者 YAML 模板](assets/author-profile.template.yaml) 和 [投稿 JSON 模板](assets/submission.template.json) 复制到论文项目目录后协助填写。真实资料存放在 skill 目录以外，不写回公开仓库。

作者 YAML 仅列历史 APEN 注册必填项；其他期刊以当前页面为准。投稿 JSON 默认指向 Applied Energy，使用其他期刊时须更新期刊信息并核查相应规则。

`null` 和 `unknown` 表示待确认，不能解释成“无基金”“无利益冲突”或作者已批准。密码、验证码及验证链接不写入资料和日志。

### 3. 发出任务

注册账号示例：

```text
使用 $journal-submission-assistant 帮我注册 Energy 的投稿账号。
先检查需要哪些资料，缺项集中询问，全程记录。
```

填写投稿草稿示例，将方括号内容替换为自己的论文目录：

```text
使用 $journal-submission-assistant，
根据这个目录中的论文和作者资料，填写 Energy 投稿草稿：
[填写自己的论文目录]

全程记录，核对上传文件和填写内容，
停在最终提交前供我审批。
```

示例期刊可替换成自己的目标期刊；助手会重新核查该期刊指南与表单。

### 4. 浏览器与账号要求

实际填写网页需要使用者的 Codex 具备浏览器操作能力，并使用其自己的期刊账号及相应访问授权。安装这个 skill 不会自动安装浏览器工具，也不会共享仓库维护者的账号或登录状态。

没有浏览器工具时，仍可整理材料、检查缺项和生成填写对照表；此时不能报告网页已填写或材料已上传。遇到需要本人处理的密码、验证码或邮箱验证步骤，按当前工具要求交接后继续。

## 本地检查

检查脚本仅依赖 Python 3 标准库。从仓库根目录运行：

```sh
python3 scripts/check_submission.py /path/to/submission.json \
  --rules references/applied-energy.rules.json
python3 -m unittest discover -s tests -v
```

规则文件仅适用于标注的期刊，使用前重新核查当前指南。退出码 `0` 表示未发现本地检查错误，`1` 表示存在检查错误，`2` 表示输入错误。空白模板预期会报告缺项；检查通过也不代表可以正式投稿。

## 文件与资料边界

- [SKILL.md](SKILL.md)：执行流程、授权范围与中断续办规则。
- `assets/`：空白资料模板及 Elsevier 利益冲突声明模板。
- `references/`：注册、投稿、分类匹配和期刊实例说明。
- `scripts/` 与 `tests/`：本地检查工具及使用虚构资料的回归测试。

本仓库只保存可复用的 skill 内容，不收录真实作者资料、论文、账号凭据或投稿操作记录。`.gitignore` 使用文件白名单；增加可复用文件时需一并更新白名单。

Elsevier Word 模板来自官方文件，出处和调整记录见[模板说明](references/competing-interests.md)，原模板权利归相应权利人。其第一项按既有偏好预选；每篇稿件仍须依据真实情况确认，预选不构成事实声明。
