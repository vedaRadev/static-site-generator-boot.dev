import os
import shutil
from pathlib import Path
from utils import extract_title
from markdown_to_html import markdown_to_html


# yes shutil.copytree exists but I want to write this recursive function for fun
def copy_clean_tree(src: str, dst: str):
    if not os.path.exists(src):
        raise Exception(f"source {src} does not exist")

    if os.path.isfile(src):
        print(f"copied: {src} -> {dst}")
        shutil.copy(src, dst)
        return

    if os.path.exists(dst):
        print(f"removed: {dst}")
        shutil.rmtree(dst)

    os.mkdir(dst)
    print(f"created: {dst}")
    for name in os.listdir(src):
        src_path = os.path.join(src, name)
        dst_path = os.path.join(dst, name)
        copy_clean_tree(src_path, dst_path)


def generate_pages(template_path: Path, src_path: Path, dst_path: Path):
    if not os.path.isfile(src_path):
        for name in os.listdir(src_path):
            generate_pages(template_path, src_path / name, dst_path / name)
        return

    if src_path.suffix != ".md":
        return

    print(f"Generating page with template {template_path}: {src_path} -> {dst_path}")

    markdown = None
    with open(src_path, "r") as markdown_file:
        markdown = markdown_file.read()

    template = None
    with open(template_path, "r") as template_file:
        template = template_file.read()

    title = extract_title(markdown)
    html = markdown_to_html(markdown).to_html()
    generated = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    os.makedirs(os.path.dirname(dst_path), exist_ok = True)
    with open(dst_path.with_suffix(".html"), "w") as html_file:
        html_file.write(generated)


def main():
    copy_clean_tree("static", "public")
    generate_pages(Path("./template.html"), Path("./content"), Path("./public"))


if __name__ == "__main__":
    main()
