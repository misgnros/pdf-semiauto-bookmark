import re


def parse_markdown(filepath):
    result = []
    current_page = None
    in_front_matter = False

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if line == "---":
                in_front_matter = not in_front_matter
                continue
            if in_front_matter or not line:
                continue

            page_match = re.match(r"<!--\s*page\s*(\d+)\s*-->", line)
            if page_match:
                current_page = int(page_match.group(1))
                continue

            heading_match = re.match(r"^(#+)\s*(.+)", line)
            if heading_match and current_page is not None:
                level = len(heading_match.group(1))
                text = heading_match.group(2).strip()
                result.append([level, text, current_page])

    return result
