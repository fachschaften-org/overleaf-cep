import xml.etree.ElementTree as ET
from tempfile import NamedTemporaryFile
from pathlib import Path
import subprocess
import yaml

class SVG:
    def __init__(self, content):
        self.root = ET.fromstring(content)
    
    def __str__(self):
        svg = ET.tostring(self.root, encoding='utf-8').decode('utf-8')
        return svg.replace('xmlns="http://www.w3.org/2000/svg"', 'xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"')
    
    def get_width(self):
        return int(float(self.root.get('width').split("pt")[0].split("px")[0]))
    def get_height(self):
        return int(float(self.root.get('height').split("pt")[0].split("px")[0]))
    
    def resize(self, width, height):
        self.root.set('width', str(width))
        self.root.set('height', str(height))
        return self
    
    def color(self, color):
        for elem in self.root.iter():
            if 'fill' in elem.attrib:
                elem.set('fill', color)
            if 'stroke' in elem.attrib:
                elem.set('stroke', color)
        return self
    
    def square_bg(self, color):
        size = max(self.get_width(), self.get_height())
        padding = 1/8*size  # 12.5% padding
        new_size = size + 2 * padding
        new_root = ET.Element('svg', {
            'width': str(new_size),
            'height': str(new_size),
            'viewBox': f'0 0 {new_size} {new_size}'
        })
        new_root.append(ET.Element('rect', {
            'x': '0',
            'y': '0',
            'width': str(new_size),
            'height': str(new_size),
            'fill': color
        }))
        self.root.set('x', str((new_size - self.get_width()) / 2))
        self.root.set('y', str((new_size - self.get_height()) / 2))
        new_root.append(self.root)
        self.root = new_root
        return self
    
    def circle_bg(self, color):
        size = max(self.get_width(), self.get_height())
        padding = 1/8*size  # 12.5% padding
        new_size = size + 2 * padding
        new_root = ET.Element('svg', {
            'width': str(new_size),
            'height': str(new_size),
            'viewBox': f'0 0 {new_size} {new_size}'
        })
        new_root.append(ET.Element('circle', {
            'cx': str(new_size / 2),
            'cy': str(new_size / 2),
            'r': str(new_size / 2),
            'fill': color
        }))
        self.root.set('x', str((new_size - self.get_width()) / 2))
        self.root.set('y', str((new_size - self.get_height()) / 2))
        new_root.append(self.root)
        self.root = new_root
        return self
    
    def overlay(self, overlay):
        overlay_root = ET.fromstring(overlay)
        self.root.append(overlay_root)
        return self

    def to_svg(self, filename):
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        with open(filename, 'w') as f:
            f.write(str(self))

    def to_png(self, filename):
        with NamedTemporaryFile(suffix='.svg', delete=True) as temp_svg:
            self.to_svg(temp_svg.name)
            temp_svg.flush()
            Path(filename).parent.mkdir(parents=True, exist_ok=True)
            subprocess.run([
                "magick",
                "-background", "none",
                temp_svg.name,
                "-resize", f"{self.root.get('width')}x{self.root.get('height')}",
                "-gravity", "center",
                "-extent", f"{self.root.get('width')}x{self.root.get('height')}",
                filename
            ], check=True)
    
    def to_ico(self, filename):
        self.to_png(filename)  # just works, as magick auto-detects the output format based on the file extension
    
PROJECT_DIR = Path(__file__).parent.parent.parent
CONFIG = yaml.safe_load(Path("config.yml").read_text())

LOGO = Path("logo.svg").read_text()
LOGO_FULL = Path("logo_full.svg").read_text()

OVERLAY_CHECK_PATH = '<path fill="#000" d="m9.615 12.032 2.75-2.921a.31.31 0 0 1 .26-.111q.146 0 .26.122a.395.395 0 0 1 0 .555l-3 3.2a.349.349 0 0 1-.531 0l-1.24-1.322a.395.395 0 0 1 0-.556.35.35 0 0 1 .261-.122q.146 0 .26.122z"/>'
OVERLAY_COMPILING_PATH = '<path fill="#000" d="M9.1 11.4q0 .4.158.742.167.341.442.583V12.5q0-.125.083-.208A.3.3 0 0 1 10 12.2a.27.27 0 0 1 .208.092.27.27 0 0 1 .092.208v1q0 .125-.092.217A.28.28 0 0 1 10 13.8H9a.3.3 0 0 1-.217-.083.3.3 0 0 1-.083-.217q0-.125.083-.208A.3.3 0 0 1 9 13.2h.317a2.6 2.6 0 0 1-.6-.792A2.4 2.4 0 0 1 8.5 11.4q0-.708.367-1.275.366-.575.966-.867a.22.22 0 0 1 .217 0 .28.28 0 0 1 .15.167.3.3 0 0 1-.008.233.3.3 0 0 1-.15.167 1.8 1.8 0 0 0-.684.65q-.258.408-.258.925m3.6 0a1.7 1.7 0 0 0-.167-.742 1.7 1.7 0 0 0-.433-.583v.225q0 .125-.092.217a.28.28 0 0 1-.208.083.3.3 0 0 1-.217-.083.3.3 0 0 1-.083-.217v-1q0-.125.083-.208A.3.3 0 0 1 11.8 9h1a.27.27 0 0 1 .208.092.27.27 0 0 1 .092.208q0 .125-.092.217a.28.28 0 0 1-.208.083h-.317q.376.333.592.8.225.459.225 1 0 .708-.367 1.283a2.36 2.36 0 0 1-.966.859.23.23 0 0 1-.217.008.3.3 0 0 1-.15-.175.35.35 0 0 1-.008-.225.3.3 0 0 1 .15-.167q.425-.225.691-.641a1.7 1.7 0 0 0 .267-.942"/>'
OVERLAY_ERROR_PATH = '<path fill="#000" d="m10.5 12.064-1.814 1.814a.38.38 0 0 1-.277.122.43.43 0 0 1-.276-.133.38.38 0 0 1-.122-.276q0-.166.122-.288L9.936 11.5 8.122 9.686A.38.38 0 0 1 8 9.409a.44.44 0 0 1 .133-.287A.38.38 0 0 1 8.409 9q.166 0 .288.122l1.803 1.814 1.814-1.814A.38.38 0 0 1 12.591 9q.165 0 .287.122a.4.4 0 0 1 .122.287q0 .156-.122.277L11.064 11.5l1.814 1.814a.38.38 0 0 1 .122.277q0 .155-.122.276a.4.4 0 0 1-.287.122.38.38 0 0 1-.277-.122z"/>'

def build_overlay(path, size):
    return f"""
        <svg width="{size}" height="{size}" viewBox="0 0 16 16">
            <circle cx="10.5" cy="11.5" r="3.5" fill="#fff"/>
            {path}
        </svg>
    """

def get_max_size(svg):
    return max(svg.get_width(), svg.get_height())

def get_source(source):
    if source == "logo":
        return LOGO
    elif source == "logo_full":
        return LOGO_FULL
    else:
        raise ValueError(f"Unknown source: {source}")
def apply_filter(svg, filter_name):
    if filter_name == "bg_square_white":
        return svg.square_bg("#FFFFFF")
    elif filter_name == "bg_circle_white":
        return svg.circle_bg("#FFFFFF")
    elif filter_name == "color_mask":
        return svg.color("#000000")
    elif filter_name == "color_black":
        return svg.color("#1b222c")
    elif filter_name == "color_grey":
        return svg.color("#9b9b9b")
    elif filter_name == "color_white":
        return svg.color("#FFFFFF")
    elif filter_name == "overlay_compiled":
        return svg.overlay(build_overlay(OVERLAY_CHECK_PATH, get_max_size(svg)))
    elif filter_name == "overlay_compiling":
        return svg.overlay(build_overlay(OVERLAY_COMPILING_PATH, get_max_size(svg)))
    elif filter_name == "overlay_error":
        return svg.overlay(build_overlay(OVERLAY_ERROR_PATH, get_max_size(svg)))
    else:
        raise ValueError(f"Unknown filter: {filter_name}")
def resize(svg, resolution):
    width, height = map(int, resolution.split("x"))
    return svg.resize(width, height)
def save(svg, filename):
    if filename.endswith(".png"):
        svg.to_png(filename)
    elif filename.endswith(".svg"):
        svg.to_svg(filename)
    elif filename.endswith(".ico"):
        svg.to_ico(filename)
    else:
        raise ValueError(f"Unknown file extension for {filename}")


ET.register_namespace("", "http://www.w3.org/2000/svg")

for image_path in CONFIG["images"]:
    print(f"Processing {image_path}...", end="")
    image = CONFIG["images"][image_path]
    svg = SVG(get_source(image["source"]))
    for f in image.get("filter", []):
        svg = apply_filter(svg, f)
    svg = resize(svg, image["resolution"])
    save(svg, str(PROJECT_DIR / image_path))
    print(" done.")
