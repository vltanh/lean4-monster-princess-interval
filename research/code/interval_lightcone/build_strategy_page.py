"""Build the strategy page research/strategies.html (not committed; the same page is at vltanh.me/princess-monster-interval/).

    python3 research/code/interval_lightcone/build_strategy_page.py               # computes the data (about 20 s)
    python3 research/code/interval_lightcone/build_strategy_page.py --data D.json # reuses data from strategy_page_data.py

The page is one self-contained HTML file: strategy_page_template.html with the data embedded. `--fragment`
also writes the page without the document skeleton, for hosts that supply their own, and `--site DIR` writes it
as a folder for vltanh.me/princess-monster-interval/: index.html, style.css, app.js, data.json and field.bin
(the Princess's field, compressed), every file under the site's 500 KB limit.
"""
import argparse, base64, json, os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
RESEARCH = os.path.dirname(os.path.dirname(HERE))
TEMPLATE = os.path.join(HERE, "strategy_page_template.html")
OUT = os.path.join(RESEARCH, "strategies.html")
SKELETON = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>
</head>
<body>
__BODY__
</body>
</html>
"""


SITE_HEAD = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Princess and Monster Playground</title>
    <meta name="description" content="__DESC__" />
    <meta property="og:title" content="Princess and Monster Playground" />
    <meta property="og:description" content="__DESC__" />
    <meta property="og:url" content="https://vltanh.me/princess-monster-interval/" />
    <link
      rel="icon"
      href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Cline x1='3' y1='16' x2='29' y2='16' stroke='%231f2937' stroke-width='1.6'/%3E%3Ccircle cx='10' cy='16' r='4.2' fill='%232563eb'/%3E%3Ccircle cx='22' cy='16' r='4.2' fill='%23dc2626'/%3E%3C/svg%3E"
    />
__FONTS_AND_THEME__
    <link rel="stylesheet" href="style.css" />
    <script src="app.js" defer></script>
  </head>
  <body>
"""


def field_file(data):
    """The site's copy of the field: each time row as differences mod 2^16 along the radius, gzip-compressed.

    The inline page carries the field as base64 (2.8 MB); this file is about 67 KB, and the page decodes it with
    DecompressionStream.  Returns the data without the base64 and the bytes of field.bin."""
    import gzip
    import numpy as np
    d = json.loads(data)
    n = d["field"]["n"]
    q = np.frombuffer(base64.b64decode(d["field"]["b64"]), dtype="<u2").reshape(-1, n).astype(np.int64)
    delta = (np.diff(q, axis=1, prepend=0) % 65536).astype("<u2")
    assert np.array_equal(np.cumsum(delta.astype(np.int64), axis=1) % 65536, q)
    d["field"] = dict(n=n, file="field.bin")
    return json.dumps(d, separators=(",", ":")) + "\n", gzip.compress(delta.tobytes(), compresslevel=9, mtime=0)


def write_site(page, data, folder):
    """The same page as the other vltanh.me playgrounds lay theirs out: markup, stylesheet, script, and the data."""
    import re
    os.makedirs(folder, exist_ok=True)
    data, field = field_file(data)
    with open(os.path.join(folder, "field.bin"), "wb") as f:
        f.write(field)
    head_end = page.index("<style>")
    head = page[:head_end]
    desc = re.search(r'<meta name="description" content="([^"]*)"', head).group(1)
    fonts_theme = "\n".join("    " + line for line in head.splitlines()
                            if line.startswith("<link") or line.startswith("<script") or line.startswith("  ") or line.startswith("</script>"))
    css = page[head_end + len("<style>"):page.index("</style>")]
    markup = page[page.index("</style>") + len("</style>"):page.index('<script type="application/json"')]
    script = page[page.rindex("<script>") + len("<script>"):page.rindex("</script>")]
    with open(os.path.join(folder, "index.html"), "w") as f:
        f.write(SITE_HEAD.replace("__DESC__", desc).replace("__FONTS_AND_THEME__", fonts_theme) + markup.strip("\n") + "\n  </body>\n</html>\n")
    with open(os.path.join(folder, "style.css"), "w") as f:
        f.write(css.strip("\n") + "\n")
    with open(os.path.join(folder, "app.js"), "w") as f:
        f.write("// The Princess and Monster playground. Built by build_strategy_page.py from strategy_page_template.html.\n" + script.strip("\n") + "\n")
    with open(os.path.join(folder, "data.json"), "w") as f:
        f.write(data)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data")
    ap.add_argument("--out", default=OUT)
    ap.add_argument("--fragment")
    ap.add_argument("--site", help="also write the page as a site folder: index.html, style.css, app.js, data.json, field.bin")
    a = ap.parse_args()
    if a.data:
        data = open(a.data).read()
    else:
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "data.json")
            subprocess.run([sys.executable, os.path.join(HERE, "strategy_page_data.py"), "--out", path], check=True)
            data = open(path).read()
    json.loads(data)
    page = open(TEMPLATE).read()
    assert page.count("__STRATEGY_DATA__") == 1
    body = page.replace("__STRATEGY_DATA__", data.replace("</", "<\\/"))
    body = body.replace('href="/projects/"', 'href="https://vltanh.me/projects/"')   # outside the site, link to it
    with open(a.out, "w") as f:
        f.write(SKELETON.replace("__BODY__", body))
    if a.fragment:
        with open(a.fragment, "w") as f:
            f.write(body)
    if a.site:
        write_site(page, data, a.site)
    print("wrote", a.out, "(%.2f MB)" % (os.path.getsize(a.out) / 1e6), "and", a.fragment or "no fragment")


if __name__ == "__main__":
    main()
