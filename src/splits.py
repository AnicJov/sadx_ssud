from pathlib import Path
import xml.etree.ElementTree as ET

def generate_livesplit_file(stories, template_path="res/splits/template.lss", segment_dir="res/splits/", output_path=None):
    tree = ET.parse(template_path)
    root = tree.getroot()

    segments = root.find("Segments")
    if segments is None:
        raise ValueError("Template is missing <Segments> element.")

    segments.clear()

    for i, story in enumerate(stories):
        segment_path = Path(segment_dir) / f"{story.lower().replace(' ', '')}.xml"
        if not segment_path.exists():
            raise FileNotFoundError(f"Segment file not found: {segment_path}")
        
        segment_tree = ET.parse(segment_path)
        segment_root = segment_tree.getroot()

        for j, segment in enumerate(segment_root.findall("Segment")):
            if i == 0 and j == 0:
                continue
            segments.append(segment)
    
    if not output_path:
        output_path = ("_".join(story.lower().replace(" ", "") for story in stories)) + ".lss"

    tree.write(output_path, encoding="UTF-8", xml_declaration=True)
