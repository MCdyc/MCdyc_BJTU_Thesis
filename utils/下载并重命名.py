#!/usr/bin/env python3
"""
解析 `arxiv_mappings.json`，通过 `arxiv_url` 下载论文 PDF，并根据 `source` 字段重命名文件名。

重命名规则：取 `source` 字段中第一个 `.` 之后的片段，截断到遇到常见分隔符之一（`[`、`(`、`//`、换行）或遇到形如 `[` 后面大写字母（例如 `[C]`）处之前，作为论文标题片段，用于文件名。

结果保存到子目录 `papers/`，并对文件名进行 Windows 安全化与长度限制。

用法（在包含 `arxiv_mappings.json` 的目录）：
    python 下载并重命名.py
"""

import os
import re
import json
import sys
import time
import urllib.request
from typing import Optional


INPUT = "arxiv_mappings.json"
OUT_DIR = "papers"
USER_AGENT = "arXiv-downloader/1.0"


def safe_filename(s: str, max_len: int = 200) -> str:
    # 移除文件系统不允许的字符，替换空白为下划线，限制长度
    s = s.strip()
    s = re.sub(r"[\\/:*?\"<>|]", "", s)
    s = re.sub(r"\s+", " ", s)
    s = s.replace(" ", "_")
    if len(s) > max_len:
        s = s[:max_len]
    return s


def extract_fragment_from_source(source: str) -> str:
    # 从第一个句点之后取片段
    if "." in source:
        rest = source.split(".", 1)[1].strip()
    else:
        rest = source.strip()

    # 如果存在像 [C] [J] 之类的标注或其它分隔符，截断在它们之前
    # 优先检测 '[' 后面紧跟大写字母的情况
    m = re.search(r"\[[A-Z]", rest)
    if m:
        rest = rest[: m.start()].strip()

    # 其他常见分隔符
    for sep in ("//", "[", "（", "(", "\n"):
        idx = rest.find(sep)
        if idx != -1:
            rest = rest[:idx].strip()

    # 如仍为空，回退到整个 source 的前 60 个字符
    if not rest:
        rest = source[:60]

    # 进一步清理前后空白并去掉尾部逗号或句号
    rest = rest.strip().rstrip('.,;:')
    return rest


def arxiv_pdf_url(arxiv_url: str) -> Optional[str]:
    if not arxiv_url:
        return None
    # arXiv 页面 URL 通常包含 /abs/ 或 /pdf/
    if "/abs/" in arxiv_url:
        pdf = arxiv_url.replace("/abs/", "/pdf/")
        if not pdf.lower().endswith('.pdf'):
            pdf = pdf.rstrip('/') + '.pdf'
        # 使用 https 优先
        pdf = re.sub(r"^http:", "https:", pdf, flags=re.IGNORECASE)
        return pdf
    if "/pdf/" in arxiv_url:
        pdf = arxiv_url
        if not pdf.lower().endswith('.pdf'):
            pdf = pdf.rstrip('/') + '.pdf'
        pdf = re.sub(r"^http:", "https:", pdf, flags=re.IGNORECASE)
        return pdf
    # 其他形式，尝试直接加上 /pdf/ 前缀
    try:
        base = arxiv_url.rstrip('/')
        return re.sub(r"^http:", "https:", base, flags=re.IGNORECASE) + '/pdf'
    except Exception:
        return None


def download_file(url: str, dest: str) -> bool:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
        with open(dest, 'wb') as f:
            f.write(data)
        return True
    except Exception as e:
        print(f"下载失败 {url}: {e}", file=sys.stderr)
        return False


def main():
    if not os.path.exists(INPUT):
        print(f"未找到 {INPUT}")
        sys.exit(2)

    os.makedirs(OUT_DIR, exist_ok=True)

    with open(INPUT, 'r', encoding='utf-8') as f:
        items = json.load(f)

    total = len(items)
    print(f"解析到 {total} 条条目，开始下载...")

    for idx, it in enumerate(items, 1):
        source = it.get('source', '')
        arxiv_url = it.get('arxiv_url')

        print(f"[{idx}/{total}] {source}")
        if not arxiv_url:
            print("  跳过：未提供 arxiv_url")
            continue

        pdf_url = arxiv_pdf_url(arxiv_url)
        if not pdf_url:
            print("  无法构造 PDF URL，跳过")
            continue

        fragment = extract_fragment_from_source(source)
        fname_base = safe_filename(fragment)
        if not fname_base:
            fname_base = f"paper_{idx}"

        # 添加 arXiv id 后缀以避免重复
        arxiv_id = arxiv_url.rstrip('/').split('/')[-1]
        filename = f"{fname_base}_{arxiv_id}.pdf"
        dest_path = os.path.join(OUT_DIR, filename)

        if os.path.exists(dest_path):
            print(f"  已存在，跳过: {dest_path}")
            continue

        print(f"  下载 {pdf_url} -> {dest_path}")
        ok = download_file(pdf_url, dest_path)
        if not ok:
            # 尝试把 abs 页面转换为 https://arxiv.org/pdf/<id>.pdf（更稳健的构造）
            fallback = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
            if fallback != pdf_url:
                print(f"  尝试备用 URL {fallback}")
                ok = download_file(fallback, dest_path)

        if ok:
            print(f"  已保存: {dest_path}")
        else:
            print(f"  下载失败: {arxiv_id}")

        # 礼貌限速
        time.sleep(0.6)

    print("处理完成。所有文件保存到目录：", OUT_DIR)


if __name__ == '__main__':
    main()
