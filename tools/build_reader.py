#!/usr/bin/env python3
"""Build the offline paper-library reader from its Markdown notes and index."""

import html
import json
import os
import re
from pathlib import Path
from urllib.parse import urlsplit

LIBRARY = Path(__file__).resolve().parents[1]
EVIDENCE = {
    'sim-and-real': '仿真与真机', 'simulation-only': '仅仿真',
    'real-robot': '真机实验', 'survey-no-new-experiment': '综述',
    'offline-motion-benchmarks': '人体运动离线评测',
    'offline-and-qualitative-robot': '离线定量 · 真机定性展示',
}
STYLE = """
:root{color-scheme:light dark;--bg:light-dark(#fafaf8,#171918);--fg:light-dark(#202520,#edf0ec);--sub:light-dark(#566157,#b3beb4);--rule:light-dark(#d7ded6,#374238);--link:light-dark(#285c40,#99cda5)}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:24px}body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.85 system-ui,-apple-system,"Noto Sans CJK SC","Microsoft YaHei",sans-serif}.layout{display:grid;grid-template-columns:220px minmax(0,850px);gap:40px;max-width:1210px;padding:40px 28px;margin:auto}aside{align-self:start;position:sticky;top:24px;max-height:calc(100vh - 48px);overflow:auto}aside p{font-size:13px;color:var(--sub);margin:0 0 16px}nav{display:flex;flex-direction:column;gap:10px;font-size:14px}a{color:var(--link);text-underline-offset:3px;overflow-wrap:anywhere}nav a{text-decoration:none}main{min-width:0}h1{font-size:30px;line-height:1.35;margin:0 0 24px}h2{font-size:23px;line-height:1.5;margin:44px 0 16px;padding-top:16px;border-top:1px solid var(--rule)}h3{font-size:18px;line-height:1.5;margin:28px 0 12px}p{margin:12px 0}ul,ol{padding-left:1.5em}li{margin:7px 0}code{font-family:ui-monospace,monospace;font-size:.9em;overflow-wrap:anywhere}.actions{display:flex;gap:16px;flex-wrap:wrap;margin-top:24px}button{font:inherit;color:var(--fg);background:transparent;border:1px solid var(--rule);border-radius:5px;padding:5px 12px;cursor:pointer}button:focus-visible,a:focus-visible{outline:2px solid var(--link);outline-offset:4px}.library-label{letter-spacing:.04em;font-size:13px;color:var(--sub);margin-bottom:12px}.paper-nav{margin:20px 0 0;padding-top:16px;border-top:1px solid var(--rule)}.paper-nav a[aria-current=page]{font-weight:700}figure{margin:24px 0}figure img{display:block;width:100%;height:auto}figcaption{font-size:13px;color:var(--sub);margin-top:8px}.library-list{margin-top:36px}.paper-entry{padding:24px 0;border-top:1px solid var(--rule)}.paper-entry h2{margin:0 0 12px;padding:0;border:0}.paper-entry .full-title{font-size:14px;color:var(--sub);margin:0 0 12px}.paper-entry .links{display:flex;gap:16px;flex-wrap:wrap;font-size:14px}.paper-entry p{max-width:800px}.index{max-width:980px;margin:auto;padding:44px 28px}.small{font-size:13px;color:var(--sub)}
@media(max-width:760px){.layout{display:block;padding:24px 20px}aside{position:static;max-height:none;overflow:visible;padding-bottom:24px;margin-bottom:28px;border-bottom:1px solid var(--rule)}nav{flex-direction:row;flex-wrap:wrap;gap:8px 16px}h1{font-size:27px}h2{font-size:21px}.index{padding:28px 20px}}@media print{aside,.actions,.paper-nav{display:none}.layout{display:block;padding:0;max-width:none}a{color:inherit}h2,h3{break-after:avoid}figure{break-inside:avoid}body{background:transparent}}
"""

CATEGORY_STYLE = """
.category-filters{display:flex;flex-wrap:wrap;gap:10px;margin:20px 0}.category-filters button[aria-pressed=true]{background:var(--link);color:var(--bg);border-color:var(--link)}.subcategory-filters{padding:14px 16px;border:1px solid var(--rule);border-radius:8px;margin-bottom:20px}.subcategory-filters .category-filters{margin:10px 0 0}.subcategory-filters p{margin:0}.category-group{margin-top:36px}.category-heading,.subcategory-heading{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap}.category-heading h2{margin:0;padding:0;border:0}.category-group>p,.subcategory-group>p{margin:8px 0 20px;color:var(--sub)}.subcategory-group{margin-top:30px}.subcategory-heading h3{font-size:21px;margin:0}.subcategory-heading a{text-decoration:none}.category-group .paper-entry h3,.category-group .paper-entry h4{font-size:21px;line-height:1.5;margin:0 0 12px}.category-count,.subcategory-count{font-size:14px;color:var(--sub)}.classification{font-size:13px;color:var(--sub)}.nav-category,.nav-subcategory{display:flex;flex-direction:column;gap:10px;padding-top:12px}.nav-subcategory{padding-left:12px;border-left:1px solid var(--rule)}.nav-group-label,.nav-subgroup-label{font-weight:700;font-size:13px;color:var(--sub)}[hidden]{display:none!important}
"""

FILTER_SCRIPT = """
const search = document.getElementById("paper-search");
const categoryButtons = Array.from(document.querySelectorAll("[data-category-filter]"));
const subcategoryButtons = Array.from(document.querySelectorAll("[data-subcategory-filter]"));
const entries = Array.from(document.querySelectorAll(".paper-entry"));
let activeCategory = "all";
let activeSubcategory = "all";

function updateResults() {
  const query = search.value.trim().toLowerCase();
  let count = 0;
  entries.forEach(entry => {
    entry.hidden = !(activeCategory === "all" || entry.dataset.category === activeCategory)
      || !(activeSubcategory === "all" || entry.dataset.subcategory === activeSubcategory)
      || !entry.dataset.search.includes(query);
    if (!entry.hidden) count++;
  });
  document.querySelectorAll(".category-group, .subcategory-group").forEach(group => {
    const visible = Array.from(group.querySelectorAll(".paper-entry")).filter(entry => !entry.hidden).length;
    group.hidden = visible === 0;
    const label = group.querySelector(group.classList.contains("category-group") ? ".category-count" : ".subcategory-count");
    label.textContent = visible === Number(label.dataset.total) ? visible + " 篇" : visible + " / " + label.dataset.total + " 篇";
  });
  categoryButtons.forEach(button => button.setAttribute("aria-pressed", String(button.dataset.categoryFilter === activeCategory)));
  subcategoryButtons.forEach(button => button.setAttribute("aria-pressed", String(button.dataset.subcategoryFilter === activeSubcategory)));
  document.querySelectorAll(".subcategory-filters").forEach(group => {
    group.hidden = activeCategory !== "all" && group.dataset.parentCategory !== activeCategory;
  });
  document.getElementById("search-count").textContent = "显示 " + count + " / " + entries.length + " 篇";
}

function selectFromHash() {
  const hash = window.location.hash.slice(1);
  const category = categoryButtons.find(button => hash === "category-" + button.dataset.categoryFilter);
  const subcategory = subcategoryButtons.find(button => button.dataset.subcategoryFilter !== "all" && hash === "subcategory-" + button.dataset.subcategoryFilter);
  activeCategory = subcategory ? subcategory.dataset.parentCategory : category ? category.dataset.categoryFilter : "all";
  activeSubcategory = subcategory ? subcategory.dataset.subcategoryFilter : "all";
  updateResults();
}

function setFilterHash(hash) {
  window.location.hash = hash;
  selectFromHash();
}
categoryButtons.forEach(button => button.addEventListener("click", () => {
  const category = button.dataset.categoryFilter;
  setFilterHash(category === "all" ? "papers" : "category-" + category);
}));
subcategoryButtons.forEach(button => button.addEventListener("click", () => {
  const subcategory = button.dataset.subcategoryFilter;
  setFilterHash(subcategory === "all" ? "category-" + button.dataset.parentCategory : "subcategory-" + subcategory);
}));
search.addEventListener("input", updateResults);
window.addEventListener("hashchange", selectFromHash);
selectFromHash();
"""


def subgroups(category, papers):
    subcategories = category.get("subcategories", [])
    if not subcategories:
        return [(None, papers)]
    return [(subcategory, [paper for paper in papers if paper["subcategory"] == subcategory["id"]])
            for subcategory in subcategories]


def paper_groups(library):
    categories = library["categories"]
    groups = {category["id"]: [] for category in categories}
    if len(groups) != len(categories):
        raise ValueError("Duplicate category IDs")
    subcategory_ids = set()
    allowed = {}
    for category in categories:
        allowed[category["id"]] = set()
        for subcategory in category.get("subcategories", []):
            identifier = subcategory["id"]
            if identifier in subcategory_ids:
                raise ValueError("Duplicate subcategory ID: " + identifier)
            subcategory_ids.add(identifier)
            allowed[category["id"]].add(identifier)
    for paper in library["papers"]:
        category = paper.get("category")
        if category not in groups:
            raise ValueError("Unknown or missing category for paper " + paper["id"])
        subcategory = paper.get("subcategory")
        if (allowed[category] and subcategory not in allowed[category]) or (subcategory and subcategory not in allowed[category]):
            raise ValueError("Unknown or missing subcategory for paper " + paper["id"])
        related = paper.get("related_subcategories", [])
        if len(related) != len(set(related)) or subcategory in related or any(item not in allowed[category] for item in related):
            raise ValueError("Invalid related subcategories for paper " + paper["id"])
        groups[category].append(paper)
    return [(category, groups[category["id"]]) for category in categories]


def classification_details(paper, category):
    subcategories = {item["id"]: item for item in category.get("subcategories", [])}
    if not subcategories:
        return ""
    primary = subcategories[paper["subcategory"]]
    result = '<p class="classification">主类：<a href="index.html#subcategory-' + html.escape(primary["id"], quote=True) + '">' + html.escape(primary["label"]) + '</a>'
    if paper.get("related_subcategories"):
        result += ' · 关联方向：' + ' / '.join(html.escape(subcategories[item]["label"]) for item in paper["related_subcategories"])
    result += '</p>'
    if paper.get("classification_reason"):
        result += '<p class="classification">' + html.escape(paper["classification_reason"]) + '</p>'
    return result


def paper_navigation(library, groups, current_id):
    navigation = '<a href="index.html">全部论文</a>'
    for reading_list in library.get("reading_lists", []):
        navigation += ('<a href="' + html.escape(reading_list["reader_path"], quote=True)
                       + '">' + html.escape(reading_list["title"]) + '</a>')
    for category, papers in groups:
        navigation += ('<div class="nav-category"><a class="nav-group-label" href="index.html#category-'
                       + html.escape(category["id"], quote=True) + '">'
                       + html.escape(category["label"]) + ' · ' + str(len(papers)) + ' 篇</a>')
        for subcategory, members in subgroups(category, papers):
            if subcategory:
                navigation += ('<div class="nav-subcategory"><a class="nav-subgroup-label" href="index.html#subcategory-'
                               + html.escape(subcategory["id"], quote=True) + '">'
                               + html.escape(subcategory["label"]) + ' · ' + str(len(members)) + ' 篇</a>')
            for other in members:
                current = ' aria-current="page"' if other["id"] == current_id else ""
                navigation += (f'<a href="{html.escape(other["reader_path"], quote=True)}"{current}>'
                               f'{html.escape(other["id"] + " · " + other["short_title"])}</a>')
            if subcategory:
                navigation += '</div>'
        navigation += '</div>'
    return navigation


def local_href(target, note):
    parts = urlsplit(target)
    if parts.scheme in ("http", "https") or target.startswith("#"):
        return target
    if parts.scheme:
        raise ValueError("Unsupported link scheme: " + target)
    path = (note.parent / parts.path).resolve()
    if not path.is_relative_to(LIBRARY):
        raise ValueError("Link leaves library: " + target)
    result = Path(os.path.relpath(path, LIBRARY)).as_posix()
    if parts.query:
        result += "?" + parts.query
    if parts.fragment:
        result += "#" + parts.fragment
    return result


def inline(text, note):
    pattern = r"(\*\*.+?\*\*|`[^`]+`|\[[^\]]+\]\([^)]+\))"
    result = []
    for token in re.split(pattern, text):
        if token.startswith("**") and token.endswith("**"):
            result.append("<strong>" + inline(token[2:-2], note) + "</strong>")
        elif token.startswith("`") and token.endswith("`"):
            result.append("<code>" + html.escape(token[1:-1]) + "</code>")
        elif (match := re.fullmatch(r"\[([^\]]+)\]\(([^)]+)\)", token)):
            href = local_href(match[2], note)
            external = ' target="_blank" rel="noopener noreferrer"' if href.startswith("http") else ""
            result.append(f'<a href="{html.escape(href, quote=True)}"{external}>'
                          + html.escape(match[1]) + "</a>")
        else:
            result.append(html.escape(token))
    return "".join(result)


def render_markdown(note):
    blocks, toc, paragraph = [], [], []
    list_kind = None
    heading_number = 0

    def flush():
        if paragraph:
            blocks.append("<p>" + inline(" ".join(paragraph), note) + "</p>")
            paragraph.clear()

    def close_list():
        nonlocal list_kind
        if list_kind:
            blocks.append("</" + list_kind + ">")
            list_kind = None

    for line in note.read_text(encoding="utf-8").splitlines():
        if match := re.fullmatch(r"!\[([^\]]*)\]\(([^)]+)\)", line):
            flush()
            close_list()
            src = html.escape(local_href(match[2], note), quote=True)
            alt = html.escape(match[1], quote=True)
            blocks.append(f'<figure><a href="{src}" target="_blank" rel="noopener">'
                          f'<img src="{src}" alt="{alt}" loading="lazy"></a>'
                          f'<figcaption>{html.escape(match[1])} · 点击查看原尺寸</figcaption></figure>')
        elif match := re.match(r"^(#{1,3})\s+(.+)$", line):
            flush()
            close_list()
            heading_number += 1
            level, label = len(match[1]), match[2]
            identifier = "section-" + str(heading_number)
            blocks.append(f'<h{level} id="{identifier}">{inline(label, note)}</h{level}>')
            if level == 2:
                toc.append(f'<a href="#{identifier}">{html.escape(label)}</a>')
        elif match := re.match(r"^(?:([-*])|(\d+)\.)\s+(.+)$", line):
            flush()
            kind = "ul" if match[1] else "ol"
            if list_kind != kind:
                close_list()
                blocks.append("<" + kind + ">")
                list_kind = kind
            blocks.append("<li>" + inline(match[3], note) + "</li>")
        elif not line.strip():
            flush()
            close_list()
        else:
            close_list()
            paragraph.append(line)
    flush()
    close_list()
    return "\n".join(blocks), "\n".join(toc)


def shell(title, body):
    return ('<!doctype html>\n<html lang="zh-CN"><head><meta charset="UTF-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<meta name="color-scheme" content="light dark"><title>' + html.escape(title)
            + "</title><style>" + STYLE + CATEGORY_STYLE + "</style></head><body>" + body + "</body></html>\n")


def main():
    library = json.loads((LIBRARY / "library.json").read_text(encoding="utf-8"))
    papers = library["papers"]
    groups = paper_groups(library)
    categories = {category["id"]: category for category, _ in groups}
    repository_url = library.get("repository", {}).get("url", "").rstrip("/")
    repository_link = ('<p class="small"><a href="' + html.escape(repository_url, quote=True)
                       + '" target="_blank" rel="noopener noreferrer">GitHub 仓库 · 维护笔记</a></p>') if repository_url else ''
    entries = {}
    for paper in papers:
        name = paper["short_title"]
        category = categories[paper["category"]]
        category_label = category["label"]
        subcategory = next((item for item in category.get("subcategories", [])
                            if item["id"] == paper.get("subcategory")), None)
        category_path = category_label + (' › ' + subcategory["label"] if subcategory else '')
        classification = classification_details(paper, category)
        edit_link = ('<p class="small"><a href="' + html.escape(repository_url + '/edit/main/' + paper["note_path"], quote=True)
                     + '" target="_blank" rel="noopener noreferrer">在 GitHub 编辑这篇笔记</a></p>') if repository_url else ''
        output = paper["reader_path"]
        note = LIBRARY / paper["note_path"]
        content, toc = render_markdown(note)
        navigation = paper_navigation(library, groups, paper["id"])
        body = (f'<div class="layout"><aside><p>全身智能 · Paper 笔记库<br>{paper["id"]} / {paper["read_on"]}<br>'
                + html.escape(category_path) + '</p>'
                '<nav aria-label="笔记章节">' + toc + '</nav><nav class="paper-nav" aria-label="论文列表">'
                + navigation + '</nav><div class="actions"><button type="button" onclick="window.print()">'
                '打印 / 保存为 PDF</button></div></aside><main><div class="library-label">'
                + html.escape(category_path + " · " + name) + "</div>" + classification + edit_link + content + "</main></div>")
        (LIBRARY / output).write_text(shell(name + " · 全身智能 Paper 笔记库", body), encoding="utf-8")
        links = f'<a href="{html.escape(output)}">阅读笔记</a><a href="{html.escape(paper["note_path"])}">文字版</a>'
        if paper.get("figures_manifest"):
            links += f'<a href="{html.escape(paper["figures_manifest"])}">原图来源记录</a>'
        if paper.get('sources', {}).get('local_pdf'):
            links += f'<a href="{html.escape(paper["sources"]["local_pdf"])}">论文 PDF</a>'
        elif paper.get('sources', {}).get('paper'):
            links += ('<a href="' + html.escape(paper['sources']['paper'], quote=True)
                      + '" target="_blank" rel="noopener noreferrer">原论文</a>')
        evidence = EVIDENCE.get(paper.get('evidence', ''), '')
        related = [item for item in category.get("subcategories", [])
                   if item["id"] in paper.get("related_subcategories", [])]
        search = ' '.join([name, category_path, paper['title'], paper['library_summary'], evidence,
                           paper.get('platform', ''), paper.get('classification_reason', ''),
                           *paper.get('tags', []),
                           *(value for item in ([subcategory] if subcategory else []) + related
                             for value in [item['label'], *item.get('keywords', [])])])
        detail = '<p class="small">' + html.escape(evidence + (' · ' if evidence else '') + ' / '.join(paper.get('tags', []))) + '</p>'
        heading = 'h4' if subcategory else 'h3'
        entries[paper["id"]] = ('<article class="paper-entry" data-category="'
                       + html.escape(category["id"], quote=True) + '" data-subcategory="'
                       + html.escape(paper.get("subcategory", ""), quote=True) + '" data-search="' + html.escape(search.lower(), quote=True)
                       + '"><' + heading + '><a href="' + html.escape(output) + '">'
                       + html.escape(paper["id"] + " · " + name) + '</a></' + heading + '><p class="full-title">'
                       + html.escape(paper["title"]) + "</p><p>" + html.escape(paper["library_summary"])
                       + '</p>' + classification + detail + '<div class="links">' + links + "</div></article>")
    reading_list_links = []
    for reading_list in library.get("reading_lists", []):
        content, toc = render_markdown(LIBRARY / reading_list["note_path"])
        body = ('<div class="layout"><aside><p>全身智能 · 专题阅读清单<br>'
                + html.escape(reading_list["updated_on"]) + '</p><nav aria-label="清单章节">'
                + toc + '</nav><nav class="paper-nav"><a href="index.html">返回笔记库</a>'
                '<a href="' + html.escape(reading_list["note_path"], quote=True) + '">文字版</a>'
                '</nav><div class="actions"><button type="button" onclick="window.print()">'
                '打印 / 保存为 PDF</button></div></aside><main><div class="library-label">'
                '文献检索 · 方法接口 · 证据范围</div>' + content + '</main></div>')
        (LIBRARY / reading_list["reader_path"]).write_text(shell(reading_list["title"], body), encoding="utf-8")
        reading_list_links.append('<p><a href="' + html.escape(reading_list["reader_path"], quote=True)
                                  + '">' + html.escape(reading_list["title"]) + '</a> · '
                                  + html.escape(reading_list["updated_on"]) + '</p>')
    reading_list_section = ('<section aria-label="专题阅读"><h2>专题阅读</h2>'
                            + "".join(reading_list_links) + '</section>') if reading_list_links else ''
    batch_history = []
    for batch in library.get("batches", []):
        details = ["新增 " + str(batch["added_unique_papers"]) + " 篇"]
        if batch.get("skipped_existing_papers"):
            details.append("跳过 " + str(batch["skipped_existing_papers"]) + " 篇已有笔记")
        if batch.get("merged_version_entries"):
            details.append("合并 " + str(batch["merged_version_entries"]) + " 个版本条目")
        details.append("保存 " + str(batch["saved_figures"]) + " 张原图")
        label = batch["read_on"] + " · " + batch["collection"] + "：" + "，".join(details) + "。"
        batch_history.append('<p class="small">' + html.escape(label) + '</p>')
    category_filters = ('<div class="category-filters" role="group" aria-label="按类目筛选">'
                        '<button type="button" data-category-filter="all" aria-pressed="true">全部 · '
                        + str(len(papers)) + ' 篇</button>')
    category_sections = []
    subcategory_filters = []
    for category, group_papers in groups:
        key = html.escape(category["id"], quote=True)
        label = html.escape(category["label"])
        total = str(len(group_papers))
        category_filters += ('<button type="button" data-category-filter="' + key
                             + '" aria-pressed="false">' + label + ' · ' + total + ' 篇</button>')
        contents = []
        if category.get("subcategories"):
            child_filters = ('<div class="subcategory-filters" data-parent-category="' + key + '">'
                             '<p class="small">' + label + ' 细分 · 按主要贡献计数，关联方向可通过关键词检索。</p>'
                             '<div class="category-filters" role="group" aria-label="' + label + ' 细分筛选">'
                             '<button type="button" data-subcategory-filter="all" data-parent-category="' + key
                             + '" aria-pressed="true">全部全身智能 · ' + total + ' 篇</button>')
        for subcategory, members in subgroups(category, group_papers):
            if not subcategory:
                contents.append(''.join(entries[paper["id"]] for paper in members))
                continue
            subkey = html.escape(subcategory["id"], quote=True)
            sublabel = html.escape(subcategory["label"])
            subtotal = str(len(members))
            child_filters += ('<button type="button" data-subcategory-filter="' + subkey + '" data-parent-category="'
                              + key + '" aria-pressed="false">' + sublabel + ' · ' + subtotal + ' 篇</button>')
            contents.append('<section class="subcategory-group" id="subcategory-' + subkey
                            + '" data-subcategory="' + subkey + '" aria-labelledby="heading-' + subkey + '">'
                            '<div class="subcategory-heading"><h3 id="heading-' + subkey + '"><a href="#subcategory-'
                            + subkey + '">' + sublabel + '</a></h3><span class="subcategory-count" data-total="' + subtotal
                            + '">' + subtotal + ' 篇</span></div><p>' + html.escape(subcategory.get("description", ""))
                            + '</p>' + ''.join(entries[paper["id"]] for paper in members) + '</section>')
        if category.get("subcategories"):
            subcategory_filters.append(child_filters + '</div></div>')
        category_sections.append('<section class="category-group" id="category-' + key
                                 + '" data-category="' + key + '" aria-labelledby="heading-' + key + '">'
                                 '<div class="category-heading"><h2 id="heading-' + key + '">' + label
                                 + '</h2><span class="category-count" data-total="' + total + '">'
                                 + total + ' 篇</span></div><p>' + html.escape(category.get("description", ""))
                                 + '</p>' + ''.join(contents) + '</section>')
    category_filters += '</div>'
    body = ('<main class="index"><p class="library-label">持续阅读 · 独立笔记 · 来源可追溯</p>'
            '<h1>全身智能 · Paper 笔记库</h1><p>已收录 ' + str(len(papers))
            + ' 篇。每篇按 Motivation、方法、实验、结论整理，记录个人判断与证据边界。</p>'
            + repository_link
            + '<p class="small">自 KODA 起保存论文总览图与方法图，保留图号、原图注、来源快照。</p>'
            + "".join(batch_history)
            + reading_list_section
            + category_filters
            + ''.join(subcategory_filters)
            + '<label for="paper-search">搜索标题、主题或关键词</label><br>'
            '<input id="paper-search" type="search" placeholder="例如 SONIC、retargeting、仿真" '
            'style="font:inherit;width:100%;padding:10px 12px;margin:10px 0;background:transparent;'
            'color:var(--fg);border:1px solid var(--rule);border-radius:5px">'
            '<p id="search-count" class="small" role="status" aria-live="polite">显示全部 ' + str(len(papers)) + ' 篇</p>'
            '<div class="library-list" id="papers">' + "".join(category_sections) + '</div><p class="small">更新于 '
            + html.escape(library["updated_on"]) + '</p></main><script>'
            + FILTER_SCRIPT + '</script>')
    (LIBRARY / "index.html").write_text(shell("全身智能 · Paper 笔记库", body), encoding="utf-8")
    print("Built " + str(len(papers)) + " paper readers, " + str(len(reading_list_links))
          + " reading lists and the library index.")


if __name__ == "__main__":
    main()
