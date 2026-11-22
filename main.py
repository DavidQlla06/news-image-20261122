"""Entry point for news-image-20261122.

Copies the committed entry.png to the output directory
(MAKEFUN_OUTPUT_DIR if set, else /output). Deterministic: the same
repository always produces the same bytes.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    dest_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(dest_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(dest_dir, "entry.png")
    if os.path.abspath(src) != os.path.abspath(dst):
        shutil.copyfile(src, dst)
    print("entry.png written to", dst)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
