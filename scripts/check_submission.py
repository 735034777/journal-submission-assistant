#!/usr/bin/env python3
"""Local, limited submission-data checks. No network, browser, or document parsing."""
import argparse
import json
import re
from pathlib import Path


def check_submission(data, base_dir, rules=None):
    issues = []
    rules = rules or {}

    def add(code, field, message, level="error"):
        issues.append(dict(level=level, code=code, field=field, message=message))

    def obj(value, field):
        if not isinstance(value, dict):
            add("object_required", field, "需要对象结构。")
            return {}
        return value

    def array(value, field):
        if not isinstance(value, list):
            add("array_required", field, "需要数组结构。")
            return []
        return value

    def text_required(value, field):
        if not isinstance(value, str) or not value.strip():
            add("missing_text", field, "缺少非空文本；请补充或按当前页面确认。")
            return False
        return True

    def strings(value, field):
        values = array(value, field)
        for index, item in enumerate(values):
            text_required(item, f"{field}[{index}]")
        return [v for v in values if isinstance(v, str) and v.strip()]

    def records(value, field):
        return [obj(v, f"{field}[{i}]") for i, v in enumerate(array(value, field))]

    def unique_ids(items, field):
        result = []
        for i, item in enumerate(items):
            value = item.get("id")
            if text_required(value, f"{field}[{i}].id"):
                if value in result:
                    add("duplicate_id", f"{field}[{i}].id", "本地关联 ID 重复。")
                result.append(value)
        return result

    data = obj(data, "root")
    journal = obj(data.get("journal"), "journal")
    if rules and journal.get("code") != rules.get("journal_code"):
        add("wrong_journal_rules", "journal.code", "期刊与规则文件不匹配，未应用该期刊数字规则。")
        rules = {}
    if rules and journal.get("guide_checked_on") != rules.get("checked_on"):
        add("rules_recheck", "journal.guide_checked_on", "资料与规则核查日期不一致；重新阅读当前指南。", "warning")
    for field in ("article_type", "title", "abstract"):
        text_required(data.get(field), field)
    abstract = data.get("abstract")
    word_count = len(abstract.split()) if isinstance(abstract, str) else 0
    maximum = rules.get("abstract_max_words")
    if maximum is not None and word_count > maximum:
        add("abstract_too_long", "abstract", f"近似词数 {word_count}，超过规则上限 {maximum}。")
    keywords = strings(data.get("keywords"), "keywords")
    highlights = strings(data.get("highlights"), "highlights")
    for label, values in (("keywords", keywords), ("highlights", highlights)):
        minimum, maximum = rules.get(label + "_min"), rules.get(label + "_max")
        if minimum is not None and len(values) < minimum:
            add("too_few_items", label, f"数量少于规则下限 {minimum}。")
        if maximum is not None and len(values) > maximum:
            add("too_many_items", label, f"数量超过规则上限 {maximum}。")
    maximum = rules.get("highlight_max_characters")
    for i, item in enumerate(highlights):
        if maximum is not None and len(item) > maximum:
            add("highlight_too_long", f"highlights[{i}]", f"字符数含空格为 {len(item)}，上限 {maximum}。")
    if len({v.casefold() for v in keywords}) != len(keywords):
        add("duplicate_keyword", "keywords", "存在重复关键词，请核查。", "warning")

    affiliations = records(data.get("affiliations"), "affiliations")
    affiliation_ids = unique_ids(affiliations, "affiliations")
    for i, item in enumerate(affiliations):
        for key in ("institution", "country_or_region"):
            text_required(item.get(key), f"affiliations[{i}].{key}")
    authors = records(data.get("authors"), "authors")
    if not authors:
        add("authors_missing", "authors", "作者清单为空。")
    author_ids = unique_ids(authors, "authors")
    for i, author in enumerate(authors):
        path = f"authors[{i}]"
        for key in ("given_name", "family_name"):
            text_required(author.get(key), f"{path}.{key}")
        email = author.get("email")
        if text_required(email, path + ".email") and not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email):
            add("email_format", path + ".email", "邮箱形式异常；此检查不验证所有权或可投递性。")
        ids = strings(author.get("affiliation_ids"), path + ".affiliation_ids")
        if not ids:
            add("affiliation_missing", path + ".affiliation_ids", "作者尚未关联单位。")
        if any(v not in affiliation_ids for v in ids):
            add("broken_affiliation", path + ".affiliation_ids", "关联到不存在的单位 ID。")
        if rules.get("require_credit_roles") and not strings(author.get("credit_roles"), path + ".credit_roles"):
            add("credit_missing", path + ".credit_roles", "请依据作者贡献说明补充 CRediT，不能根据排名推断。")
    source_order = strings(data.get("source_author_order"), "source_author_order")
    if not source_order:
        add("source_order_missing", "source_author_order", "需要从原稿/作者说明独立提取作者顺序以供比对。")
    elif source_order != author_ids:
        add("author_order_mismatch", "authors", "作者清单顺序与记录的原稿顺序不同。")
    for field in ("corresponding_author_id", "submitting_author_id"):
        value = data.get(field)
        if not isinstance(value, str) or value not in author_ids:
            add("author_role_unresolved", field, "未指定有效稿件作者；如为代办投稿需人工确认系统角色。")

    funding = obj(data.get("funding"), "funding")
    status = funding.get("status")
    sources = records(funding.get("sources"), "funding.sources")
    if status not in ("funded", "none"):
        add("funding_unconfirmed", "funding.status", "资助情况未确认；unknown 不能转换为无资助。")
    if status == "funded" and not sources:
        add("funders_missing", "funding.sources", "已声明有资助但未列资助方。")
    if status == "none" and sources:
        add("funding_conflict", "funding", "无资助与列出的资助方冲突。")
    for i, source in enumerate(sources):
        text_required(source.get("organization"), f"funding.sources[{i}].organization")
        recipient = source.get("recipient_author_id")
        if recipient is not None and (not isinstance(recipient, str) or recipient not in author_ids):
            add("funder_recipient", f"funding.sources[{i}]", "资助对象与作者 ID 未对应。")

    declarations = obj(data.get("declarations"), "declarations")
    for field in ("all_authors_approved", "not_under_review_elsewhere"):
        if declarations.get(field) is not True:
            add("author_confirmation_needed", f"declarations.{field}", "尚无肯定确认，不能认定具备正式投稿条件。")
    allowed = {"competing_interests": ("none", "declared"), "ethics": ("not_applicable", "approved", "exempt"), "ai_use": ("none", "declared")}
    for field, statuses in allowed.items():
        item = obj(declarations.get(field), f"declarations.{field}")
        if item.get("status") not in statuses:
            add("declaration_unconfirmed", f"declarations.{field}", "声明状态未确认；不要推断否或不适用。")
        elif item.get("status") != "none":
            text_required(item.get("statement"), f"declarations.{field}.statement")
    availability = obj(data.get("data_availability"), "data_availability")
    if availability.get("status") not in ("public", "restricted", "on_request", "not_applicable"):
        add("data_unconfirmed", "data_availability.status", "数据可用性待确认。")
    text_required(availability.get("statement"), "data_availability.statement")
    if availability.get("status") == "public" and not strings(availability.get("links"), "data_availability.links"):
        add("data_links_missing", "data_availability.links", "声明公开但未记录数据链接。")

    files = records(data.get("files"), "files")
    roles = [f.get("role") for f in files if isinstance(f.get("role"), str)]
    for role in rules.get("required_file_roles", []):
        if role not in roles:
            add("required_file_missing", "files", f"规则要求的文件用途未提供：{role}。")
    for i, item in enumerate(files):
        field = f"files[{i}]"
        text_required(item.get("role"), field + ".role")
        value = item.get("path")
        if not text_required(value, field + ".path"):
            continue
        path = Path(value).expanduser()
        if not path.is_absolute():
            path = Path(base_dir) / path
        if not path.is_file():
            add("file_not_found", field + ".path", "本地文件不存在或不是普通文件。")
        suffix, role = path.suffix.lower(), item.get("role")
        if role in ("manuscript", "highlights") and suffix == ".pdf" and rules:
            add("editable_source_needed", field, "该用途需要可编辑材料，PDF 不能代替源文件。")
        if role == "competing_interests" and rules.get("competing_interests_extensions") and suffix not in rules["competing_interests_extensions"]:
            add("declaration_file_format", field, "利益冲突文件扩展名不符合规则中的 Word 格式要求。")
        token = rules.get("highlights_filename_contains")
        if role == "highlights" and token and token.casefold() not in path.name.casefold():
            add("highlights_filename", field, "Highlights 文件名缺少规则要求的标识。")
    for i, question in enumerate(array(data.get("open_questions"), "open_questions")):
        add("open_question", f"open_questions[{i}]", "仍有待作者答复的问题。")
    if not array(data.get("provenance"), "provenance"):
        add("provenance_missing", "provenance", "尚未记录信息来源，需人工对照原稿。", "warning")
    return {"scope": "local_data_checks_only", "submission_ready": "not_determined", "abstract_word_count_approx": word_count, "errors": sum(i["level"] == "error" for i in issues), "warnings": sum(i["level"] == "warning" for i in issues), "issues": issues}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("submission", type=Path)
    parser.add_argument("--rules", type=Path, help="Rules rechecked against the target journal's current guide")
    args = parser.parse_args()
    try:
        data = json.loads(args.submission.read_text(encoding="utf-8"))
        rules = json.loads(args.rules.read_text(encoding="utf-8")) if args.rules else None
        if rules is not None and not isinstance(rules, dict):
            raise ValueError("rules must be a JSON object")
        report = check_submission(data, args.submission.resolve().parent, rules)
        report["rules_checked_on"] = rules.get("checked_on") if rules else None
    except (OSError, ValueError, TypeError) as error:
        print(json.dumps({"scope": "input_error", "error_type": type(error).__name__, "message": "输入文件、JSON 结构或规则类型错误；请检查输入。"}, ensure_ascii=False, indent=2))
        return 2
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
