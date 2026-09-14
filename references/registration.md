# 账号注册：流程和字段字典

核查日期：2026-09-11。L=当前页面观察；D=官方说明/截图；U=目标期刊未验证。D 不代表目标期刊实测。

## 账号类型与流程

Elsevier Account 是统一身份；期刊 EM 记录承载角色及稿件；ORCID 是研究者标识及可选认证方式。统一账号存在不代表期刊记录完整。

本文件的统一身份实测主要针对 Elsevier。IEEE TIM 的独立账号及字段差异见[专项实测](ieee-tim-registration.md)；同一平台域名不代表共享出版社身份。

APEN 实测两条路径：
- 官网 → submit.elsevier.com/APEN → Sign in / Start a submission → id.elsevier.com → 邮箱。
- editorialmanager.com/apen/ → Login → Register Now → id.elsevier.com → 邮箱。

出现机构提示时可用“改用其他方式”的 Cancel 进入邮箱页；顶部关闭按钮会取消整次登录，两者不能混用。不要据机构提示填写作者单位。

根据[Elsevier 注册说明](https://www.elsevier.support/elsevieraccess/answer/how-do-i-create-an-elsevier-account)，邮箱匹配已有账号时登录，否则进入注册。首轮调研停在邮箱之前；第二轮用用户授权邮箱实测到了已有账号登录分支及一次性链接发送页。之后已恢复统一身份、打开期刊注册表并核查字段，详见[APEN 注册表实测](applied-energy-registration.md)。个人邮箱不进入本通用参考文件。

## 已有账号分支实测（2026-09-11 追加）

保留的旧会话首次提交邮箱出现通用功能错误；从期刊官方入口新建会话后提交成功。错误原因未知，不能断言是邮箱错误或账号不存在。

成功分流后，登录页实际显示：只读邮箱、密码输入框、忘记密码、默认勾选的保持登录、使用一次性链接登录、使用其他帐户。密码为空时密码登录按钮禁用。选择一次性链接后，网站显示已发送至指定邮箱，并显示 24 小时有效期。该期限是此页面本次观察值，不设为所有邮件的固定期限。

后续已验证：邮件到达，统一身份可识别，期刊记录未找到，已打开 APEN 注册表。设置页二次登录及姓名更正也已成功。后续已从作者主菜单及资料页核实期刊账号可用；最终确认点击过程未被工具观察。本次未创建新的 Elsevier 统一账号，因此下表中统一账号新注册字段仍保留 D/U 状态。

## 统一账号字段

下表及 EM 清单包含跨期刊的补充字段，不代表作者 YAML 的必填项。简版 YAML 仅保留本次 APEN 注册的六项必填资料；其余按当前页面需要另记。

| 标签/项目 | 中文及资料键 | 必填性证据 | 处理 |
|---|---|---|---|
| 电子邮箱 / Email | 邮箱 `email` | L：首屏入口，空值继续禁用（新版投稿） | 使用用户指定的真实邮箱 |
| Given name | 名 `given_name` | D：官方注册截图；目标校验 U | 作者确认的拼写，不自动拆分中文名 |
| Family name | 姓 `family_name` | D：官方注册截图；目标校验 U | 姓名字段与显示顺序分开 |
| Password | 密码，无资料键 | D：截图有此字段；目标规则 U | 用户创建与提交，不记录 |
| Stay signed in | `preferences.stay_signed_in` | D：偏好项 | 按用户选择 |
| 产品/活动邮件 | `preferences.marketing_emails` | D：偏好项 | 不把默认勾选当作选择 |
| 条款 / Register | 完成注册 | D：示例中继续关联条款 | 按当前页面和工具要求由用户处理 |

[官方注册截图](https://supportcontent.elsevier.com/RightNow%20Next%20Gen/ElsevierAccess/registration%20screenshot.png)来自上述官方说明。图中密码至少 8 字符，并建议数字、大小写和符号；这是官方示例而非目标当次校验，不在脚本写死。

## EM 通用资料准备字段

APEN 当前已观察的字段与必填星号见[独立实测表](applied-energy-registration.md)，优先使用该表并核对当前页面。以下是跨期刊的准备清单。依据：[个人资料说明](https://www.elsevier.support/publishing/answer/how-do-i-change-my-personal-information-in-editorial-manager)、[EM 注册说明](https://www.elsevier.support/publishing/answer/how-do-i-register-an-account-on-editorial-manager)。

| 项目 | 资料键 | 证据/条件 | 注意 |
|---|---|---|---|
| Username | `accounts.em_username` | D：可出现，唯一且无空格 | 不擅自重设 |
| Title / Degree | `title` / `degree` | L：APEN 分别必填/未标必填；其他期刊待核查 | 不推断称谓或学位 |
| Preferred Name | `preferred_name` | D：按期刊启用 | 不覆盖正式姓名 |
| E-mail | `email` / `additional_emails` | D：首个邮箱识别账户及找回 | 仅填本人控制的邮箱 |
| ORCID | `orcid` | D：按期刊设置 | 号码不等于授权关联 |
| Institution / Department | `institution` / `department` | D：可有机构联想 | 核对候选机构 |
| Position | `position` | D：可导入字段 | 职务不同于学位 |
| City / State or Province / Country or Region | 国家用 `country_or_region`；城市、省份另记 | D：可能出现 | 必填与省份条件看当前页 |
| Street / Postal code / Phone | 地址、邮编、电话 | L：APEN 可见且未标必填；其他期刊待核查 | 不猜私人信息 |
| Personal Classifications / Keywords | `classifications` / `expertise_keywords` | D：数量按期刊配置 | 模糊分类描述按[匹配机制](classification-matching.md)映射到网页正式选项；关键词不能替代必填分类 |
| Available as a Reviewer | `preferences.available_as_reviewer` | D：可能出现 | 不默认 Yes |
| Additional Information | 当次另记 | D：隐私及自定义问题 | 不预设问题与答案 |

## 传统 EM 分支

只有当前页面实际出现时才按传统路径操作：姓名与邮箱 → 重复记录检查 → 补资料 → 确认与问题 → 完成/邮件。已有记录可能来自编辑邀请，优先补原记录。统一账号分支不要套用此顺序。无真实邮箱时记录公开证据，不能用假资料或隐藏接口推进。

账号或邮件错误恢复、只读姓名纠错、传统分支与统一身份分支的差异，见[实测流程](applied-energy-registration.md)。

## 跨期刊复测：Energy and AI（2026-09-11）

从[期刊官网](https://www.sciencedirect.com/journal/energy-and-ai)及[作者指南](https://www.sciencedirect.com/journal/energy-and-ai/publish/guide-for-authors)进入 [EM](https://www.editorialmanager.com/eai/)。已有统一身份返回 Journal registration not found，随后可 Create journal registration。此前检查的另一家期刊直接进入作者菜单，属于已有记录登录，未把它算作新注册。

本次新注册表必填项为 Title、名、姓、邮箱、Institution、Country or Region；专业分类及个人关键词未标必填。这与 APEN 的必填组合不同：不能固定作者模板字段数，也不能为只缺单位的页面虚构单位。机构候选需同时核对名称与地域，将院系、城市、邮编填入对应字段。

分类复测完成了中文语义匹配、相邻细分类排除、勾选后 Add、Submit 和主表回读。未明确的可选方向保持未选，没有为了覆盖所有描述而增加未经支持的细分类。本次所选条目未自动带入上级，仍以各期刊实际保存值为准。

Confirm Registration 经用户现场确认条款及偏好后完成提交；Author Main Menu、Author 角色及 Update My Information 中保存资料均已核查。这验证了“已有统一身份 → 新期刊记录”的完整注册分支；未测试新建统一身份、设置密码、稿件上传或最终投稿。个人资料、具体研究方向及匹配条目只保存在任务记录中，不随技能分发。
