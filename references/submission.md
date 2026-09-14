# 投稿资料与表单操作

## 通用资料映射

下表是本地资料模型，不是出版商 API。标签、顺序、必填性以当次页面和指南为准。

| 信息组 | 模板键 | 来源与核对 |
|---|---|---|
| 期刊/类型/专刊 | journal / article_type / special_issue | 用户意图、实际下拉选项 |
| 标题/摘要/关键词 | title / abstract / keywords | 稿件原文，符号、截断、数量 |
| 作者及顺序 | authors / source_author_order | 标题页和作者确认；稳定 ID 对照 |
| 单位 | affiliations / authors[].affiliation_ids | 可多单位；工作时与现单位分开 |
| 通讯/投稿人 | corresponding_author_id / submitting_author_id | 不默认等于操作账号 |
| 贡献 | authors[].credit_roles | 作者 CRediT 声明，不按排名推断 |
| 基金 | funding | 正式名称、项目号、资助对象；未知不等于无 |
| 声明 | declarations | 冲突、伦理、同意、AI 使用的真实信息 |
| 数据 | data_availability | 可访问链接或不能公开的实际原因 |
| 文件 | files | 路径、用途、版本；本地存在不等于已上传 |
| 审稿偏好 | reviewer_preferences | 身份、邮箱、理由；要求待期刊核查 |
| 出版偏好 | publication_preferences | OA、预印本与许可按用户决定 |
| 附加问题 | journal_questions | 原问题、条件、拟答、来源 |

在 provenance 中记录文件/章节或用户说明，在 open_questions 汇总缺项。

Elsevier 利益冲突声明的本地 Word 模板、官方来源及使用条件见[利益冲突声明](competing-interests.md)。

## JSON 填写约定

- funding.status：unknown / funded / none。sources 内每项用 organization、grant_numbers（数组）、recipient_author_id（可空）；项目号必须来自真实资助材料。
- competing_interests.status、ai_use.status：unknown / none / declared；declared 时填 statement。
- ethics.status：unknown / not_applicable / approved / exempt；除 unknown 外写明真实 statement，审批编号可放 approval_reference，不自动生成。
- all_authors_approved、not_under_review_elsewhere：null / true / false；仅作者确认后修改。
- data_availability.status：unknown / public / restricted / on_request / not_applicable；附 statement，public 时记录 links。某状态在本地模型可表达，不保证满足期刊政策。
- files 每项含 role、path，可另加 version 和 notes。常见用途 manuscript、highlights、competing_interests、figure、supplement、cover_letter、graphical_abstract；例如 {"role":"highlights","path":"materials/highlights.docx"}。文件格式最终按网站要求核查。
- provenance 每项记录 field、source、location；例如 field 为 authors，source 为用户提供的标题页路径，location 为作者列表。不要复制验证链接或凭证。
- journal_questions 每项记录 label、required（true/false/null）、condition、answer、source、verified；这组问题须人工核查，脚本不代答。
- source_author_order 使用与 authors[].id 对应的 ID 列表，从原稿单独提取后记录；不是复制当前表单顺序来冒充原稿证据。

上述标志是资料状态，不是授权凭据。单名作者、团体作者和代办投稿等特殊情况需要按期刊实际页面处理；脚本可能提示人工核查，不应编造姓、名或作者身份来通过检查。

## 平台处理

新版服务按当前进度列表处理文章类型、伦理问题、文件、元数据、作者、基金、出版选项及附加问题，最终核对提交。Word 可能自动提取信息；基金号可能选填；伦理问题随研究类型变化。APEN 登录后表单尚未实测。依据：[新版官方指南](https://www.elsevier.support/publishing/answer/author-guide-to-editorial-managers-new-submission-experience)（2026-08-28）。

该指南仍列有转投限制，但 APEN 公开入口已显示 Complete a transfer。转投需要另核查当前流程，不自动判定支持或不支持。正式投稿后进入 EM 管理，返修也在 EM。

传统 EM：确认 Author 角色，优先恢复草稿。主文件上传后检查提取结果，补文件与元数据。更改通讯作者可能把草稿控制权转给另一账号，执行前说明影响。构建 PDF、保存待续、最终批准投稿是不同步骤。依据：[EM 官方投稿指南](https://www.elsevier.support/publishing/answer/how-do-i-submit-a-manuscript-in-editorial-manager)（2026-08-28）。

## 本地检查的边界

check_submission.py 只用 Python 标准库，不联网。相对文件路径按输入 JSON 所在目录解析。检查缺项、ID/单位关系、顺序、声明状态、文件存在及给定的长度限制；不读 Word/PDF 正文，不验证伦理真实性、排版、网页保存或投稿结果。

词数以空白分隔近似计算；字符数采用 Unicode 码点并包含空格；特殊字符和网站计数应再核查。无错误不等于可以投稿。代理需要实际读取稿件核对来源，不能伪造 source_author_order 来通过检查。

续办记录写期刊入口、平台、日期、阶段、草稿标识、已核对页、缺项、保存状态、下一步及真实用户授权范围，不存凭证、认证链接或固定控件编号。
