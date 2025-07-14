import re


def count_headings(markdown_text):
    counts = {}
    for match in re.finditer(r"^(#{1,6})\s+", markdown_text, flags=re.MULTILINE):
        heading = match.group(1)
        counts[heading] = counts.get(heading, 0) + 1
    return counts


def insert_heading_counts_front_matter(markdown_text):
    counts = count_headings(markdown_text)

    # フロントマターを抽出
    front_matter_match = re.match(r"^---\n(.*?)\n---\n", markdown_text, flags=re.DOTALL)
    if front_matter_match:
        front_matter = front_matter_match.group(1)
        rest_of_text = markdown_text[front_matter_match.end() :]
    else:
        front_matter = ""
        rest_of_text = markdown_text

    # 見出しの数を追記
    count_lines = [
        f"number of {level}: {counts[level]}"
        for level in sorted(counts.keys(), key=lambda x: len(x))
    ]
    if front_matter:
        new_front_matter = (
            "---\n" + front_matter + "\n" + "\n".join(count_lines) + "\n---\n\n"
        )
    else:
        new_front_matter = "---\n" + "\n".join(count_lines) + "\n---\n\n"

    return new_front_matter + rest_of_text
