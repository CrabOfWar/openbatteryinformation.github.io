"""Build obi-site.zip: the static web files, ready for Cloudflare Pages upload."""
import os
import shutil
import zipfile

WEB = ["index.html", "obi.html", "setup.html", "download.html", "LICENSE"]
DIRS = ["css", "js", "firmware", "assets"]

staging = "_site"
zip_name = "obi-site.zip"

shutil.rmtree(staging, ignore_errors=True)
if os.path.exists(zip_name):
    os.remove(zip_name)
os.makedirs(staging)

for f in WEB:
    shutil.copy2(f, staging)
for d in DIRS:
    shutil.copytree(d, os.path.join(staging, d))

count = 0
with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as z:
    for root, _, files in os.walk(staging):
        for name in files:
            full = os.path.join(root, name)
            arc = os.path.relpath(full, staging).replace(os.sep, "/")
            z.write(full, arc)
            count += 1

shutil.rmtree(staging, ignore_errors=True)

with zipfile.ZipFile(zip_name) as z:
    bad = z.testzip()
    names = sorted(z.namelist())
print(f"wrote {zip_name}: {count} files, {os.path.getsize(zip_name) / 1048576:.1f} MB, integrity={'ok' if bad is None else bad}")
print("root entries:", ", ".join(n for n in names if "/" not in n))
