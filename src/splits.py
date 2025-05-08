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

def generate_split_names(stories, segment_dir="res/splits/", glitched_gamma=True):
    split_names = []

    for story in stories:
        if story == "Gamma":
            fname = f"gamma_{'glitched' if glitched_gamma else 'linear'}.xml"
        else:
            fname = f"{story.lower().replace(' ', '')}.xml"
        segment_path = Path(segment_dir) / fname

        if not segment_path.exists():
            raise FileNotFoundError(f"Segment file not found: {segment_path}")

        tree = ET.parse(segment_path)
        root = tree.getroot()

        for segment in root.findall("Segment")[1:]:
            name_elem = segment.find("Name")
            if name_elem is None or not name_elem.text:
                continue
            # Skip Start Story segments (Mostly here because of Super Sonic)
            if name_elem.text.startswith("Start"):
                continue
            name = name_elem.text.strip()
            name = re.sub(r"^\{.*?\}\s*", "", name)  # Remove {...} prefix
            name = name.lstrip("-").strip()          # Remove leading dash/space
            split_names.append(name)

    return split_names

def generate_split_names_txt(stories, segment_dir="res/splits/", output_path=None, glitched_gamma=True):
    names = generate_split_names(stories, segment_dir, glitched_gamma)

    if not output_path:
        base = "_".join(s.lower().replace(" ", "") for s in stories)
        prefix = ""
        if "Gamma" in stories:
            prefix = "glitched_" if glitched_gamma else "linear_"
        output_path = f"{prefix}{base}.txt"

    with open(output_path, "w", encoding="utf-8") as f:
        for name in names:
            f.write(name + "\n")

    return output_path


if __name__ == "__main__":
    stories_string = input("Enter stories, comma separated: ")
    stories = [story.strip().title() for story in stories_string.split(",")]

    generate_livesplit_file(stories)
    generate_split_names_txt(stories)

    if "Gamma" in stories:
        generate_livesplit_file(stories, glitched_gamma=False)
        generate_split_names_txt(stories, glitched_gamma=False)
