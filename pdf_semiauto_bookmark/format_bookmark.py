import re


# 入力：複数行テキスト、出力：見出し以外削除された複数行テキスト
def filter_texts(text):
    raw_texts = []
    text = re.sub(r"\n{2,}", "\n", text)
    for line in text.split("\n"):
        if re.match(r"^#+ .*", line):
            raw_texts.append(line)
    filtered_texts = "\n".join(raw_texts)

    return filtered_texts


def adjust_md_headings(md_text):
    # 正規表現で全ての見出しを見つける
    headings = re.findall(r"^(#{1,6})\s+", md_text, flags=re.MULTILINE)

    if not headings:
        return md_text  # 見出しがなければそのまま返す

    # 見出しの深さの最小値を取得
    min_level = min(len(h) for h in headings)

    # 最上位がすでに#であれば変更不要
    if min_level == 1:
        return md_text

    # 各行を処理
    def replace_heading(match):
        hashes = match.group(1)
        new_level = len(hashes) - (min_level - 1)
        if new_level < 1:
            new_level = 1
        return "#" * new_level + " "

    # 見出し行のみランクを調整
    adjusted_text = re.sub(
        r"^(#{1,6})(\s+)", lambda m: replace_heading(m), md_text, flags=re.MULTILINE
    )
    return adjusted_text


# 入力：ページごとのテキストチャンク、出力：ランク調整後の見出しだけページごとにまとめた複数行テキスト（空白ページあり）
def md_to_bookmark(all_text):
    md_text = []
    for page in all_text:
        sections_text = filter_texts(page["text"])
        md_text.append(
            "<!-- page " + str(page["metadata"]["page"]) + " -->\n" + sections_text
        )

    md_text = "\n".join(md_text)
    md_text = adjust_md_headings(md_text)

    return md_text


def bookmark_list_to_md(bookmark_list):
    """
    入力: [[level:int, title:str, page:int], ...]
    出力: 指定フォーマットのマークダウンテキスト
    """
    from collections import defaultdict

    # ページごとに見出しをまとめる
    page_dict = defaultdict(list)
    for level, title, page in bookmark_list:
        page_dict[page].append((level, title))

    # ページ番号で昇順に並べる
    md_lines = []
    for page in sorted(page_dict.keys()):
        md_lines.append(f"<!-- page {page} -->")
        for level, title in page_dict[page]:
            md_lines.append(f"{'#' * level} {title}")

    return "\n".join(md_lines)
