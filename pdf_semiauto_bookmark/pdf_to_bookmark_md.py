from .summarize_bookmark import insert_heading_counts_front_matter
from .format_bookmark import md_to_bookmark, bookmark_list_to_md


def generate_bookmark_from_text(file_path, all_text):
    bookmark_list = md_to_bookmark(all_text)
    bookmark_list = insert_heading_counts_front_matter(bookmark_list)
    with open(file_path.with_suffix(".md"), "w", encoding="utf-8") as f:
        f.write(bookmark_list)
    print("Notion: Bookmarks saved to " + str(file_path.with_suffix(".md.")))


def export_existing_bookmark(file_path, bookmark):
    bookmark_list = insert_heading_counts_front_matter(bookmark_list_to_md(bookmark))
    with open(file_path.with_suffix(".md"), "w", encoding="utf-8") as f:
        f.write(bookmark_list)
    print(
        "Notion: This PDF already has bookmarks. Bookmarks saved to "
        + str(file_path.with_suffix(".md."))
    )
