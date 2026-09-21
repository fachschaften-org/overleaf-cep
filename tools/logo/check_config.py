import yaml
from pathlib import Path

try:
    CONFIG = yaml.safe_load(open("config.yml"))
except FileNotFoundError:
    CONFIG = {}

IMAGE_FORMATS = (".svg", ".png", ".ico", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff")
PROJECT_DIR = Path(__file__).parent.parent.parent.resolve()

IGNORED_PATHS = [
    "tools/logo",
    "services/clsi/test",
    "services/git-bridge/src/test",
    "services/history-v1/test",
    "services/web/test",
    "services/web/app/templates/project_files",
]
IGNORED_WEBIMG_PATHS = [
    "about",
    "advocates",
    "ai-assist",
    "brand",  # sharelatex brand
    "crests",
    "digital-science",
    "dropbox",
    "enterprise-page",
    "feature-page",
    "flags",
    "github",
    "material-icons",
    "onboarding",
    "other-brands",
    "references-search",
    "share-modal",
    "social",
    "subscriptions",
    "teasers",
    "third-party-icons",
    "third-party-references",
    "v1-import",
    "welcome-page",
    "website-redesign/gallery",
]
IGNORED_WEB_REDESIGN_STICKERS = [
    "arrow",
    "books",
    "brain",
    "campus",
    "clipboard",
    "cloud",
    "cog-pen",
    "collaborate",
    "curly-braces",
    "cursors",
    "data",
    "dna",
    "double-cloud",
    "double-column",
    "email",
    "eyes",
    "formatting",
    "globe-2",
    "globe-3",
    "globe-4",
    "globe",
    "graph-down",
    "graph-up",
    "house-tree",
    "hub",
    "journal",
    "life-preserve",
    "lightning",
    "lock",
    "lock-open",
    "math-symbols",
    "office-building",
    "parentheses",
    "pen",
    "phone",
    "pi",
    "presentations",
    "quotation-close",
    "quotation-open",
    "reports",
    "rocket",
    "secure-building",
    "simplified",
    "square-brackets",
    "support",
    "technical-writing",
    "test-tubes",
    "visual-editor",
    "waving-hand",
]

def is_relevant_image(file_path):
    if file.suffix.lower() not in IMAGE_FORMATS:
        return False
    for ignored in IGNORED_PATHS:
        if str(file_path).startswith(str(PROJECT_DIR / ignored)):
            return False
    for ignored in IGNORED_WEBIMG_PATHS:
        if str(file_path).startswith(str(PROJECT_DIR / "services/web/public/img" / ignored)+"/"):
            return False
    if str(file_path).startswith(str(PROJECT_DIR / "services/web/public/img/website-redesign/stickers")):
        WEB_REDESIGN_STICKER_COLORS = ["blue", "green", "purple", "red", "yellow", "grey", "pink", "tangerine"]
        WEB_REDESIGN_STICKER_SIZE = ["medium", "large"]
        for ignored in IGNORED_WEB_REDESIGN_STICKERS:
            for color in WEB_REDESIGN_STICKER_COLORS:
                if file_path == PROJECT_DIR / f"services/web/public/img/website-redesign/stickers/{ignored}-{color}.svg":
                    return False
                for size in WEB_REDESIGN_STICKER_SIZE:
                    if file_path == PROJECT_DIR / f"services/web/public/img/website-redesign/stickers/{ignored}-{color}-{size}.svg":
                        return False
        return False
    if str(file_path.relative_to(PROJECT_DIR)) in CONFIG.get("ignored_images", []):
        return False
    return True


# walk main directory and list all image-like files
for file in PROJECT_DIR.rglob("*"):
    relative_path = file.relative_to(PROJECT_DIR)
    if not is_relevant_image(file):
        continue
    config_size = CONFIG.get("images", {}).get(str(relative_path), {}).get("resolution")

    if str(relative_path).endswith(".svg"):
        import xml.etree.ElementTree as ET
        svg = ET.parse(file).getroot()
        if "width" in svg.attrib and "height" in svg.attrib:
            width = int(float(svg.attrib["width"].split("pt")[0].split("px")[0]))
            height = int(float(svg.attrib["height"].split("pt")[0].split("px")[0]))
        elif "viewBox" in svg.attrib:
            viewBox = svg.attrib["viewBox"].split()
            width = int(viewBox[2])
            height = int(viewBox[3])
        else:
            print(f"WARNING: cannot derive width/height of SVG {file.relative_to(PROJECT_DIR)}")
            width = None
            height = None
    else:
        from PIL import Image
        with Image.open(file) as img:
            width, height = img.size
    
    if config_size != f"{width}x{height}":
        print(f"WARNING: Image {file.relative_to(PROJECT_DIR)} has size {width}x{height}, but config.yml specifies {config_size}")
        print(f"  {file.relative_to(PROJECT_DIR)}:")
        print(f"    source: ???")
        print(f"    resolution: {width}x{height}")

