# Applied Energy 期刊注册表实测

观察日期：2026-09-11。分支：已有 Elsevier 统一账号 → 期刊记录未找到 → Create journal registration → Registration Page。已填写并进入 Confirm Registration；后续恢复页面时已能进入 Author Main Menu，且资料页保存值核对一致。最后确认动作未被工具观察；账号可用性已核实。必填性以星号及可见校验为依据，不能外推所有条件分支。个人资料不保存在此通用实例。

## 当前表单字段

| 页面标签 | 当前要求 | 形态与填写规则 |
|---|---|---|
| Title | 必填 * | 可编辑文本；由作者提供真实称谓，不自行推断 |
| Given/First Name | 必填 * | 从统一账号带入的只读文字；先核对名/姓对应关系 |
| Middle Name | 未标必填 | 文本；不适用可留空 |
| Family/Last Name | 必填 * | 从统一账号带入的只读文字 |
| Degree | 未标必填 | 按作者确认的学位填写，不由称谓推导 |
| Telephone Number | 未标必填 | 文本，页面提示包括国家代码 |
| E-mail Address | 必填 * | 从统一账号带入的只读文字 |
| ORCID | 未标必填 | Fetch/Register 关联入口；本次未关联 |
| Position | 未标必填 | 文本 |
| Institution | 未标必填 | 可输入，提示提供机构匹配候选 |
| Department | 未标必填 | 文本 |
| Street Address | 未标必填 | 四个地址输入行 |
| City | 未标必填 | 文本 |
| State or Province | 未标必填 | 文本；国家选择可能影响条件要求，按当次页面核查 |
| Zip or Postal Code | 未标必填 | 文本 |
| Country or Region | 必填 * | 下拉菜单，初始未选择；依据作者资料匹配当次选项 |
| Available as a Reviewer? | 未标必填 | Yes/No，初始 No 被选中；暂存到确认页，最终提交前需核对用户意愿 |
| Personal Classifications | 必填 * | 页面明确 Select 1+ Classifications，至少 1 个 |
| Personal Keywords | 未标必填 | Edit Personal Keywords；初始 None Defined，编辑窗口已实测，按条 Add 后 Close，回读全部关键词 |
| Continue >> | 下一步 | 已点击并进入 Confirm Registration；后续账号可用性另行核查 |

该分支未显示可编辑的 EM 用户名或新密码，不添加虚构的必填项。页面提示注册成功后可在 Update My Information 补充资料；确认页及条款已观察（见下节）；账号可用性后续已核查（见文末）；最终确认点击过程、其他未出现的自定义问题及注册完成邮件未验证。

## 专业分类窗口

Select Personal Classifications 会打开独立窗口。实测有搜索、展开/折叠、Add、Remove、已选列表、Cancel、Submit；未选任何项时 Submit 禁用。界面提示须点 Submit 才保存选择，不能把高亮候选当作已经选入。实际添加和保存已测试：搜索结果的文字行点击可能不勾选复选框；检查勾选状态后再 Add。系统可能同时添加上级分类；Submit 后回到主表核对实际列表。

分类按层级组织，展开后可见细分类。依据作者真实研究方向按[专业分类匹配机制](classification-matching.md)在当次列表搜索、比较并自动选择明确匹配项；不在通用技能中保存具体分类名称、代码或个人关键词示例。

## 401 与会话恢复

本次一次性登录由内置浏览器发起，用户在 Chrome 打开邮件后，EM 回调路径 `/oauth2/idpresponse` 显示 401 Authorization Required。在 Chrome 从[期刊正式入口](https://www.editorialmanager.com/apen/)重新点击 Elsevier account，随后直接出现 Journal registration not found，列出该统一账号邮箱，并允许打开期刊注册表。恢复期刊流程未重发邮件、未重放认证链接，也未更改浏览器安全设置。

可确认：统一身份已被识别，期刊注册匹配缺失，注册表可访问。推测：跨浏览器会话不一致可能参与了 401；未取得根因证据，不能写为已修复的确定原因，也不能把 401 等同于邮箱错误、链接过期或账号不存在。

恢复顺序：核对错误位置与浏览器 → 在实际打开邮件的同一浏览器从正式期刊入口重新开始 → 按新页面决定是可继续、期刊记录缺失还是仍需验证。不要先连续重发。只有新页面确实需要验证时再请求新邮件。

## 姓名纠错

本次发现统一账号带入的名/姓对应关系需要用户确认，且期刊页不可直接编辑。应先记录用户明确更正，再从[官方个人资料说明](https://www.elsevier.support/elsevieraccess/answer/how-can-i-change-my-email-or-personal-details)进入[Elsevier Settings](https://id.elsevier.com/settings/)。本次设置页要求重新登录；用户明确授权邮箱操作后，在原邮箱核对最新邮件的发件人、收件人、时间及设置用途，点击进入设置并保存姓名，出现成功提示。正式姓名和显示名称是两个字段；中文界面的称谓选项有本地化显示，不据此改变期刊要求的英文 Title。

更正统一资料后须回到期刊流程检查带入值是否刷新，不假设即时同步，不用隐藏字段改写只读姓名；避免把错误姓名写入新期刊记录。

本次直接刷新及通过期刊 Login 再次进入，仍带入旧姓名；已按网站 Logout 退出 EM 身份旧会话，重新通过个人邮箱登录以刷新身份。退出旧身份会话并用新邮件完成登录后，期刊注册表带入的新姓名已正确；这一恢复路径已实测成功。只刷新 iframe 或重新打开网址不等同于重建身份会话。

重新从期刊根入口进入时，本次还观察到传统注册表：Enter preferred user name、Password、Re-type Password 均有必填星号，姓名和邮箱变为可编辑；未填写这组新凭证。发现路径变化时先核对身份分支，不能把这组字段混到统一身份注册表。

## 个人关键词实测

Edit Personal Keywords 打开独立窗口。New Keyword 非空后 Add 可用；每次 Add 后显示当前列表及 Remove/Edit，输入框清空；可以继续添加。Close 后主表显示已加关键词。本次按用户研究方向填写英文，并核对自动排序没有遗漏。这里的 Close 用于回主表，与分类窗口必须 Submit 的行为不同。

## Confirm Registration 实测

本次初始表单 Continue 后先显示 Saving changes，随后出现 Confirm Registration。确认页列出名、姓、邮箱和国家；未在此页显示的称谓、分类、关键词在此前主表已经回读，不能仅凭确认页就推断所有字段保存成功。

确认页另外包含：

- 营销退订复选框，初始未勾选。文字含义为勾选后不接收新闻、促销和特别优惠；这是反向选项，不能把勾选误当作订阅。
- 必选的接受项：Publisher's Terms and Conditions、Publisher's Privacy Policy、Aries Privacy Policy，初始未勾选。
- Previous Page 返回资料页；Continue 在接受项未勾选时禁用，页面说明此按钮用于完成注册。

观察确认页时，助手未勾选接受项，也未点击最终 Continue。后续恢复已是作者主菜单：可以报告账号可用，但不能声称助手执行了未观察到的最终操作。接受条款遵守当前浏览器工具的即时确认要求，向用户展示具体动作及已核对资料，并合并确认尚未知的审稿意愿、营销偏好。用户早先授权注册不替代工具明确要求的条款即时确认。

条款原文：[Publisher Terms and Conditions](https://www.elsevier.com/legal/elsevier-website-terms-and-conditions)、[Publisher Privacy Policy](https://www.elsevier.com/legal/privacy-policy)、[Aries Privacy Policy](https://www.ariessys.com/about/privacy-policy/)。

## 注册完成后的核对

当前已观察到 Author Main Menu 与 Author 角色，并从 Update My Information 核对核心注册字段、分类和关键词已保存。先将用户确认资料整理到任务目录的作者 YAML 文件，读取最新文件再对照网页；字段一致时不重复注册或无故重提资料。

更新资料页新增了常用姓名、备用联系方式、首选联系方式等项目，不应把这些项目全部倒推成初次注册必填。统一账号 Display Name 与期刊 Preferred Name 的含义不同，应分别记录。若最终操作发生在工具观察之外，区分账号当前状态与助手实际动作，不补写虚构过程。
