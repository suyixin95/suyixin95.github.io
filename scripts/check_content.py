"""Validate editable content before Jekyll builds it. No network requests."""
from datetime import date
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit

import yaml


class UniqueLoader(yaml.SafeLoader):
    pass


def unique_mapping(loader, node):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node)
        if key in result:
            raise ValueError(f"duplicate YAML key: {key}")
        result[key] = loader.construct_object(value_node)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def validate(root):
    errors = []

    def error(path, message):
        errors.append(f"{path}: {message}")

    def load(path, front_matter=False):
        try:
            text = (root / path).read_text(encoding="utf-8")
            if front_matter:
                match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.S)
                if not match:
                    raise ValueError("missing YAML front matter")
                text = match[1]
            data = yaml.load(text, Loader=UniqueLoader)
            if not isinstance(data, dict):
                raise ValueError("expected a YAML mapping")
            return data
        except (OSError, ValueError, yaml.YAMLError) as exc:
            error(path, str(exc))
            return {}

    def required(data, fields, path):
        for field in fields:
            value = data
            for part in field.split("."):
                value = value.get(part) if isinstance(value, dict) else None
            if not isinstance(value, str) or not value.strip():
                error(path, f"{field} must be non-empty text")

    def https(value, path, field):
        try:
            parsed = urlsplit(str(value))
            if parsed.scheme == "https" and parsed.netloc:
                return parsed.netloc
        except ValueError:
            pass
        error(path, f"{field} must use an absolute https:// URL")
        return ""

    def local_asset(value, path):
        value = str(value)
        target = (root / value.lstrip("/")).resolve()
        if not value.startswith("/") or not target.is_relative_to(root) or not target.is_file():
            error(path, f"missing or invalid local asset: {value}")

    config = load("_config.yml")
    site_host = https(config.get("url", ""), "_config.yml", "url")
    cname = root / "CNAME"
    if cname.exists() and site_host != cname.read_text().strip():
        error("_config.yml", "url must match CNAME")
    profile_path = "_data/profile.yml"
    profile = load(profile_path)
    required(profile, ["name", "email", "avatar", "degree.en", "degree.zh", "current.employer",
                       "current.employer_url", "current.role.en", "current.role.zh", "current.since",
                       "current.summary.en", "current.summary.zh"], profile_path)
    if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", str(profile.get("email", ""))):
        error(profile_path, "email must be a valid email address")
    try:
        date.fromisoformat(str(profile.get("updated_on", "")))
    except ValueError:
        error(profile_path, "updated_on must be a real date in YYYY-MM-DD format")
    for field in ["avatar", "wechat_image"]:
        if profile.get(field):
            local_asset(profile[field], profile_path)
    current = profile.get("current", {})
    if isinstance(current, dict):
        https(current.get("employer_url", ""), profile_path, "current.employer_url")
    links = profile.get("links", [])
    if not isinstance(links, list):
        error(profile_path, "links must be a list")
        links = []
    for link in links:
        if not isinstance(link, dict):
            error(profile_path, "each link must have label and url")
            continue
        required(link, ["label", "url"], profile_path)
        https(link.get("url", ""), profile_path, "links.url")

    routes = {}

    def output_path(route):
        if route.endswith("/"):
            return route + "index.html"
        return route if route.endswith(".html") else route + ".html"

    def add_route(route, path):
        if not isinstance(route, str) or not route.startswith("/") or route.startswith("//") or ".." in route.split("/"):
            error(path, f"invalid route: {route}")
            return
        key = output_path(route)
        if key in routes:
            error(path, f"duplicate route {route}, already used by {routes[key]}")
        routes[key] = path

    for directory in ["_pages", "_publications"]:
        for path in sorted((root / directory).glob("*.md")):
            relative = path.relative_to(root).as_posix()
            data = load(relative, front_matter=True)
            required(data, ["title", "permalink"], relative)
            add_route(data.get("permalink"), relative)
            redirects = data.get("redirect_from", [])
            if isinstance(redirects, str):
                redirects = [redirects]
            if not isinstance(redirects, list):
                error(relative, "redirect_from must be a list")
                redirects = []
            for route in redirects:
                add_route(route, relative)
            if directory == "_publications":
                required(data, ["venue", "citation"], relative)
                if type(data.get("year")) is not int or not 1900 <= data["year"] <= 2100:
                    error(relative, "year must be a number between 1900 and 2100")
                if data.get("category") not in ["manuscripts", "conferences"]:
                    error(relative, "category must be manuscripts or conferences")
                if "selected" in data and not isinstance(data["selected"], bool):
                    error(relative, "selected must be true or false (without quotes)")
                if data.get("paperurl"):
                    https(data["paperurl"], relative, "paperurl")
                if "date" in data:
                    try:
                        date.fromisoformat(str(data["date"]))
                    except ValueError:
                        error(relative, "date must be YYYY-MM-DD")
            text = path.read_text(encoding="utf-8")
            for asset in re.findall(r"/images/[\w.\-/]+", text):
                local_asset(asset, relative)

    navigation = load("_data/navigation.yml").get("main", [])
    if not isinstance(navigation, list):
        error("_data/navigation.yml", "main must be a list")
        navigation = []
    for item in navigation:
        if not isinstance(item, dict):
            error("_data/navigation.yml", "each item must have title and url")
            continue
        required(item, ["title", "url"], "_data/navigation.yml")
        route = str(item.get("url", ""))
        if output_path(route) not in routes:
            error("_data/navigation.yml", f"unknown navigation target: {route}")
    return errors


if __name__ == "__main__":
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    errors = validate(root)
    print("\n".join(errors) if errors else "Content checks passed.")
    sys.exit(bool(errors))
