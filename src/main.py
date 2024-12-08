import os
import shutil


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


def main():
    copy_clean_tree("static", "public")


if __name__ == "__main__":
    main()
