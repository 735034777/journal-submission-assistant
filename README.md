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

将 `REPOSITORY_URL` 替换为本仓库的克隆地址；私有仓库需要相应 GitHub 访问权限。目标目录应尚不存在。

```sh
git clone REPOSITORY_URL ~/.codex/skills/journal-submission-assistant
```

在可读取该 skill 的 Codex 任务中使用：

```text
使用 $journal-submission-assistant，参考我提供的作者资料和论文，
填写指定期刊的投稿草稿，全程记录，停在最终提交前供我审批。
```

开始前把 [作者 YAML 模板](assets/author-profile.template.yaml) 和 [投稿 JSON 模板](assets/submission.template.json) 复制到 skill 目录以外的任务目录，再填写真实资料。作者 YAML 仅列历史 APEN 注册必填项；其他期刊以当前页面为准。投稿 JSON 默认指向 Applied Energy，使用其他期刊时须更新期刊信息并核查相应规则。

`null` 和 `unknown` 表示待确认，不能解释成“无基金”“无利益冲突”或作者已批准。密码、验证码及验证链接不写入资料和日志。

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
