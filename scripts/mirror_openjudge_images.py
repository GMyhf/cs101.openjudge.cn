#!/usr/bin/env python3
"""Mirror every remote image referenced by the downloaded OpenJudge HTML."""
from __future__ import annotations

import argparse
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
from html.parser import HTMLParser
import json
import mimetypes
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OPENJUDGE = ROOT / "data" / "openjudge"
STATIC_IMAGES = ROOT / "static" / "openjudge" / "images"
MIRROR_DIR = STATIC_IMAGES / "mirror"
MANIFEST = STATIC_IMAGES / "manifest.json"
HTML_DIRS = (OPENJUDGE / "pages", OPENJUDGE / "books")
USER_AGENT = "CS101 local image mirror"

CONTENT_EXTENSIONS = {
    "image/jpeg": ".jpg",
    "image/jpg": ".jpg",
    "image/png": ".png",
    "image/gif": ".gif",
    "image/bmp": ".bmp",
    "image/x-ms-bmp": ".bmp",
    "image/webp": ".webp",
    "image/svg+xml": ".svg",
}
EXTENSION_CONTENT_TYPES = {
    ".jpg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".bmp": "image/bmp",
    ".webp": "image/webp",
    ".svg": "image/svg+xml",
}


class ImageSources(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.sources: list[str] = []
        self.formulas: dict[str, str] = {}

    def handle_starttag(self, tag, attrs):
        if tag.lower() != "img":
            return
        attributes = dict(attrs)
        source = attributes.get("src")
        if source:
            source = source.strip()
            self.sources.append(source)
            if urlparse(source).hostname == "upload.wikimedia.org" and attributes.get("alt"):
                self.formulas[source] = attributes["alt"].strip()


def html_files():
    return [path for folder in HTML_DIRS for path in sorted(folder.glob("*.html"))]


def collect_remote_images(paths=None):
    references: dict[str, set[str]] = {}
    for path in paths or html_files():
        parser = ImageSources()
        parser.feed(path.read_text(encoding="utf-8", errors="replace"))
        for source in parser.sources:
            if urlparse(source).scheme.lower() not in {"http", "https"}:
                continue
            references.setdefault(source, set()).add(str(path.relative_to(ROOT)))
    return references


def collect_wikimedia_formulas(paths=None):
    formulas = {}
    for path in paths or html_files():
        parser = ImageSources()
        parser.feed(path.read_text(encoding="utf-8", errors="replace"))
        formulas.update(parser.formulas)
    return formulas


def image_extension(content_type, data):
    mime = content_type.split(";", 1)[0].strip().lower()
    # Several legacy OpenJudge URLs end in .jpg and report image/jpeg while
    # actually serving GIF or PNG bytes. The payload signature is authoritative.
    if data.startswith(b"\xff\xd8\xff"):
        return ".jpg"
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return ".png"
    if data.startswith((b"GIF87a", b"GIF89a")):
        return ".gif"
    if data.startswith(b"BM"):
        return ".bmp"
    if data.startswith(b"RIFF") and data[8:12] == b"WEBP":
        return ".webp"
    if b"<svg" in data[:1024].lower():
        return ".svg"
    if mime in CONTENT_EXTENSIONS:
        return CONTENT_EXTENSIONS[mime]
    guessed = mimetypes.guess_extension(mime, strict=False)
    detail = f", guessed {guessed}" if guessed else ""
    raise ValueError(f"response is not a recognized image ({mime or 'no content type'}{detail})")


def validate_image(data, extension):
    signatures = {
        ".jpg": data.startswith(b"\xff\xd8\xff"),
        ".png": data.startswith(b"\x89PNG\r\n\x1a\n"),
        ".gif": data.startswith((b"GIF87a", b"GIF89a")),
        ".bmp": data.startswith(b"BM"),
        ".webp": data.startswith(b"RIFF") and data[8:12] == b"WEBP",
        ".svg": b"<svg" in data[:1024].lower(),
    }
    if not data or not signatures.get(extension, False):
        raise ValueError(f"invalid {extension} image payload ({len(data)} bytes)")


def render_wikimedia_formula(formula):
    check_url = "https://wikimedia.org/api/rest_v1/media/math/check/tex"
    request = Request(
        check_url,
        data=urlencode({"q": formula}).encode(),
        headers={"User-Agent": USER_AGENT, "Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    with urlopen(request, timeout=30) as response:
        resource = response.headers.get("x-resource-location")
    if not resource:
        raise ValueError("Wikimedia math response has no resource location")
    render_url = f"https://wikimedia.org/api/rest_v1/media/math/render/png/{resource}"
    request = Request(render_url, headers={"User-Agent": USER_AGENT, "Accept": "image/png"})
    with urlopen(request, timeout=30) as response:
        data = response.read()
        content_type = response.headers.get("Content-Type", "")
    extension = image_extension(content_type, data)
    validate_image(data, extension)
    return data, extension, render_url, content_type.split(";", 1)[0].strip().lower()


def fetch_image(source, formula=None):
    attempts = [source]
    if source.startswith("http://"):
        attempts.append("https://" + source[len("http://"):])
    errors = []
    for url in attempts:
        request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "image/*"})
        try:
            with urlopen(request, timeout=30) as response:
                data = response.read()
                content_type = response.headers.get("Content-Type", "")
            extension = image_extension(content_type, data)
            validate_image(data, extension)
            return data, extension, url, content_type.split(";", 1)[0].strip().lower()
        except (HTTPError, URLError, TimeoutError, ValueError) as error:
            errors.append(f"{url}: {error}")
    if formula:
        try:
            return render_wikimedia_formula(formula)
        except (HTTPError, URLError, TimeoutError, ValueError) as error:
            errors.append(f"Wikimedia formula {formula!r}: {error}")
    raise RuntimeError("; ".join(errors))


def load_manifest():
    if not MANIFEST.is_file():
        return {}
    return json.loads(MANIFEST.read_text(encoding="utf-8")).get("assets", {})


def local_file(local_url):
    return ROOT / local_url.lstrip("/")


def reusable_entry(source, entry):
    if not entry or not isinstance(entry, dict):
        return None
    path = local_file(entry.get("path", ""))
    if not path.is_file():
        return None
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest != entry.get("sha256") or len(data) != entry.get("bytes"):
        return None
    validate_image(data, path.suffix.lower())
    return data, path, digest


def manifest_entry(source, references, data, path, digest, fetched_from, content_type):
    actual_content_type = EXTENSION_CONTENT_TYPES[path.suffix.lower()]
    entry = {
        "path": "/" + path.relative_to(ROOT).as_posix(),
        "bytes": len(data),
        "sha256": digest,
        "content_type": actual_content_type,
        "fetched_from": fetched_from,
        "reference_count": len(references[source]),
        "example_pages": sorted(references[source])[:8],
    }
    if content_type and content_type != actual_content_type:
        entry["source_content_type"] = content_type
    return entry


def mirror_all(max_workers=12):
    references = collect_remote_images()
    formulas = collect_wikimedia_formulas()
    previous = load_manifest()
    assets = {}
    pending = []

    # Keep the already-reviewed first asset at its readable path.
    seeded = {
        "http://media.openjudge.cn/images/1003/hangover.jpg":
            STATIC_IMAGES / "1003" / "hangover.jpg",
    }
    for source in sorted(references):
        reused = reusable_entry(source, previous.get(source))
        if reused:
            data, path, digest = reused
            old = previous[source]
            assets[source] = manifest_entry(source, references, data, path, digest,
                                            old.get("fetched_from", source),
                                            old.get("source_content_type", old.get("content_type", "")))
            continue
        path = seeded.get(source)
        if path and path.is_file():
            data = path.read_bytes()
            extension = path.suffix.lower()
            validate_image(data, extension)
            digest = hashlib.sha256(data).hexdigest()
            assets[source] = manifest_entry(source, references, data, path, digest, source,
                                            "image/jpeg")
            continue
        pending.append(source)

    MIRROR_DIR.mkdir(parents=True, exist_ok=True)
    failures = {}
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {
            pool.submit(fetch_image, source, formulas.get(source)): source
            for source in pending
        }
        for index, future in enumerate(as_completed(futures), 1):
            source = futures[future]
            try:
                data, extension, fetched_from, content_type = future.result()
                digest = hashlib.sha256(data).hexdigest()
                path = MIRROR_DIR / f"{digest[:24]}{extension}"
                if not path.exists():
                    path.write_bytes(data)
                assets[source] = manifest_entry(source, references, data, path, digest,
                                                fetched_from, content_type)
                print(f"[{index:3d}/{len(pending)}] {len(data):8d} {source}", flush=True)
            except Exception as error:
                failures[source] = str(error)
                print(f"FAILED {source}: {error}", flush=True)

    if failures:
        raise RuntimeError("image mirroring failed:\n" +
                           "\n".join(f"- {url}: {error}" for url, error in sorted(failures.items())))

    payload = {
        "generated_by": "scripts/mirror_openjudge_images.py",
        "html_files": len(html_files()),
        "remote_urls": len(references),
        "total_references": sum(len(paths) for paths in references.values()),
        "assets": {source: assets[source] for source in sorted(assets)},
    }
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    temporary = MANIFEST.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(MANIFEST)
    print(f"mirrored {len(assets)} remote images into {STATIC_IMAGES}")
    return payload


def check_manifest():
    references = collect_remote_images()
    assets = load_manifest()
    problems = []
    if set(assets) != set(references):
        for source in sorted(set(references) - set(assets)):
            problems.append(f"missing manifest entry: {source}")
        for source in sorted(set(assets) - set(references)):
            problems.append(f"stale manifest entry: {source}")
    for source, entry in assets.items():
        try:
            if reusable_entry(source, entry) is None:
                problems.append(f"missing or changed local image: {source}")
        except ValueError as error:
            problems.append(f"invalid local image: {source}: {error}")
    return problems


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="verify the manifest without network access")
    parser.add_argument("--workers", type=int, default=12)
    options = parser.parse_args()
    if options.check:
        problems = check_manifest()
        if problems:
            print("\n".join(problems))
            return 1
        print(f"image manifest is complete: {len(load_manifest())} remote URLs")
        return 0
    mirror_all(options.workers)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
