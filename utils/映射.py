#!/usr/bin/env python3
"""
从工作目录下的 `文档列表` 读取每条记录，尝试从记录中提取 arXiv id（若有），
否则使用 arXiv API 搜索候选论文，生成映射表并输出为 `arxiv_mappings.json`。

用法: 在包含 `文档列表` 的目录运行 `python 下载.py`
"""

import re
import time
import json
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional


INPUT_FILE = "文档列表"
OUTPUT_FILE = "arxiv_mappings.json"


def split_paragraphs(text: str) -> List[str]:
	# 按空行分割为若干记录（每篇论文一条）
	parts = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
	return parts


def find_arxiv_id(text: str) -> Optional[str]:
	# 支持多种格式：arXiv:2302.13971, arXiv: 2302.13971, 2311.09488 等
	m = re.search(r"arXiv\s*[:]?\s*([0-9]{4}\.\d{4,5}(v\d+)?)", text, re.IGNORECASE)
	if m:
		return m.group(1)
	# 也考虑形如 2311.09488 (年份+编号)，但避免误报太短的数字串
	m2 = re.search(r"(?<!\d)([0-9]{4}\.\d{4,5}(v\d+)?)(?!\d)", text)
	if m2:
		return m2.group(1)
	return None


def query_arxiv(query: str, max_results: int = 1) -> List[Dict[str, str]]:
	base = "http://export.arxiv.org/api/query?"
	q = f'all:"{query}"'
	params = {
		"search_query": q,
		"start": "0",
		"max_results": str(max_results),
	}
	url = base + urllib.parse.urlencode(params)
	# 设置 User-Agent 避免被拒绝
	req = urllib.request.Request(url, headers={"User-Agent": "arXiv-mapper/1.0"})
	try:
		with urllib.request.urlopen(req, timeout=15) as resp:
			data = resp.read()
	except Exception as e:
		print(f"网络请求失败: {e}", file=sys.stderr)
		return []

	try:
		root = ET.fromstring(data)
	except ET.ParseError:
		print("无法解析 arXiv 返回的 XML", file=sys.stderr)
		return []

	ns = {"atom": "http://www.w3.org/2005/Atom"}
	entries = []
	for entry in root.findall("atom:entry", ns):
		eid = entry.find("atom:id", ns)
		title = entry.find("atom:title", ns)
		if eid is None:
			continue
		eid_text = eid.text.strip() if eid.text else None
		title_text = title.text.strip().replace("\n", " ") if title is not None and title.text else None
		entries.append({"id": eid_text, "title": title_text})
	return entries


def extract_title_after_first_dot(text: str) -> str:
	"""从记录中取第一个句点之后的片段，直到遇到常见分隔符（'//', '[', '(' 等）。"""
	if "." in text:
		rest = text.split(".", 1)[1].strip()
	else:
		rest = text.strip()

	# 按常见分隔符截断
	for sep in ("//", "[", "（", "(", "\n"):
		idx = rest.find(sep)
		if idx != -1:
			rest = rest[:idx].strip()
	# 去掉开头可能的非字母数字符号
	rest = re.sub(r'^[^A-Za-z0-9]+', '', rest)
	return rest[:240]


def build_mapping(paragraphs: List[str]) -> List[Dict[str, Optional[str]]]:
	results = []
	for i, p in enumerate(paragraphs, 1):
		brief = p.splitlines()[0][:240]
		arxiv_id = find_arxiv_id(p)
		if arxiv_id:
			arxiv_url = f"https://arxiv.org/abs/{arxiv_id}"
			results.append({"source": brief, "arxiv_url": arxiv_url, "arxiv_title": None})
			print(f"[{i}] 已检测到 arXiv id: {arxiv_id}")
			continue

		# 没有直接的 arXiv id，使用第一个句点之后的片段作为查询（更接近论文题目）
		query = extract_title_after_first_dot(p)
		print(f"[{i}] 使用片段搜索 arXiv: {query}")
		entries = query_arxiv(query, max_results=1)
		if entries:
			eid = entries[0].get("id")
			title = entries[0].get("title")
			results.append({"source": brief, "arxiv_url": eid, "arxiv_title": title})
			print(f"    -> 命中: {eid} 题目: {title}")
		else:
			results.append({"source": brief, "arxiv_url": None, "arxiv_title": None})
			print(f"    -> 未找到匹配的 arXiv 结果")

		time.sleep(0.6)  # 轻量限速，避免短时间内请求过多

	return results


def main(input_file: str = INPUT_FILE, output_file: str = OUTPUT_FILE):
	try:
		with open(input_file, "r", encoding="utf-8") as f:
			text = f.read()
	except FileNotFoundError:
		print(f"未找到输入文件: {input_file}", file=sys.stderr)
		sys.exit(2)

	paras = split_paragraphs(text)
	print(f"共解析到 {len(paras)} 条记录，开始查询 arXiv...")
	mapping = build_mapping(paras)

	# 生成按 arXiv URL 索引的字典（可能存在 None 的条目）
	output_list = mapping
	with open(output_file, "w", encoding="utf-8") as outf:
		json.dump(output_list, outf, ensure_ascii=False, indent=2)

	print(f"已写入映射文件: {output_file}")


if __name__ == "__main__":
	main()

