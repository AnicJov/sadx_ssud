from pathlib import Path
import xml.etree.ElementTree as ET
import re

def generate_livesplit_file(stories, template_path="res/splits/template.lss", segment_dir="res/splits/", output_path=None, glitched_gamma=True):
    tree = ET.parse(template_path)
    root = tree.getroot()

    segments = root.find("Segments")
    if segments is None:
        raise ValueError("Template is missing <Segments> element.")

    segments.clear()

    for i, story in enumerate(stories):
        if story == "Gamma":
            segment_path = Path(segment_dir) / f"gamma_{"glitched" if glitched_gamma else "linear"}.xml"
        else: 
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
        if "Gamma" in stories:
            output_path = ("glitched_" if glitched_gamma else "linear_") + ("_".join(story.lower().replace(" ", "") for story in stories)) + ".lss"
        else:
            output_path = ("_".join(story.lower().replace(" ", "") for story in stories)) + ".lss"

    tree.write(output_path, encoding="UTF-8", xml_declaration=True)

    return output_path


def generate_split_names_txt(stories, segment_dir="res/splits/", output_path=None, glitched_gamma=True):
    split_names = []

    for story in stories:
        if story == "Gamma":
            segment_path = Path(segment_dir) / f"gamma_{'glitched' if glitched_gamma else 'linear'}.xml"
        else:
            segment_path = Path(segment_dir) / f"{story.lower().replace(' ', '')}.xml"

        if not segment_path.exists():
            raise FileNotFoundError(f"Segment file not found: {segment_path}")
        
        segment_tree = ET.parse(segment_path)
        segment_root = segment_tree.getroot()

        segments = segment_root.findall("Segment")
        for segment in segments[1:]:  # Skip the first segment
            name_elem = segment.find("Name")
            if name_elem is not None:
                name = name_elem.text.strip()
                # Remove leading dash and any prefix in curly braces
                name = re.sub(r"^\{.*?\}\s*", "", name)  # Remove {...} at the start
                name = name.lstrip("-").strip()         # Remove leading dashes/spaces
                split_names.append(name)

    if not output_path:
        if "Gamma" in stories:
            output_path = ("glitched_" if glitched_gamma else "linear_") + ("_".join(story.lower().replace(" ", "") for story in stories)) + ".txt"
        else:
            output_path = ("_".join(story.lower().replace(" ", "") for story in stories)) + ".txt"

    with open(output_path, "w", encoding="utf-8") as f:
        for name in split_names:
            f.write(name + "\n")


if __name__ == "__main__":
    stories_string = input("Enter stories, comma separated: ")
    stories = [story.strip().title() for story in stories_string.split(",")]

    generate_livesplit_file(stories)
    generate_split_names_txt(stories)

    if "Gamma" in stories:
        generate_livesplit_file(stories, glitched_gamma=False)
        generate_split_names_txt(stories, glitched_gamma=False)
