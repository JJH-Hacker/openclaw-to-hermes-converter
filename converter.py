import json
import shutil
import zipfile
import tempfile
from pathlib import Path
import yaml

def convert_skill(source_path: Path, dest_dir: Path):
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    # Handle zip/.skill files
    temp_dir = None
    if source_path.is_file() and (source_path.suffix == '.skill' or source_path.suffix == '.zip'):
        temp_dir = tempfile.mkdtemp()
        with zipfile.ZipFile(source_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        source_dir = Path(temp_dir)
        # Often zip files have a single top-level directory. If so, go into it.
        contents = list(source_dir.iterdir())
        if len(contents) == 1 and contents[0].is_dir():
            source_dir = contents[0]
    else:
        source_dir = source_path

    try:
        # Check if it already has SKILL.md (already Hermes-compatible)
        if (source_dir / "SKILL.md").exists():
            print("Found native SKILL.md format! Copying as is...")
            for item in source_dir.iterdir():
                dest_item = dest_dir / item.name
                if item.is_dir():
                    shutil.copytree(item, dest_item, dirs_exist_ok=True)
                else:
                    shutil.copy2(item, dest_item)
            return

        # Heuristics to find metadata
        metadata = {
            "name": source_path.stem if source_path.is_file() else source_path.name,
            "description": "Converted from Openclaw format."
        }
        
        metadata_files = ["manifest.json", "config.json", "metadata.json"]
        for m_file in metadata_files:
            p = source_dir / m_file
            if p.exists():
                try:
                    with open(p, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        if "name" in data:
                            metadata["name"] = data["name"]
                        if "description" in data:
                            metadata["description"] = data["description"]
                        for k, v in data.items():
                            if k not in metadata and isinstance(v, (str, int, float, bool)):
                                metadata[k] = v
                    break
                except Exception as e:
                    print(f"Warning: Failed to parse {m_file}: {e}")

        # Heuristics to find YAML metadata
        yaml_files = ["config.yaml", "manifest.yaml"]
        for y_file in yaml_files:
            p = source_dir / y_file
            if p.exists():
                try:
                    with open(p, "r", encoding="utf-8") as f:
                        data = yaml.safe_load(f)
                        if data:
                            if "name" in data:
                                metadata["name"] = data["name"]
                            if "description" in data:
                                metadata["description"] = data["description"]
                            for k, v in data.items():
                                if k not in metadata and isinstance(v, (str, int, float, bool)):
                                    metadata[k] = v
                    break
                except Exception as e:
                    print(f"Warning: Failed to parse {y_file}: {e}")

        # Heuristics to find instructions
        instructions = ""
        instruction_files = ["instructions.txt", "prompt.txt", "README.md", "system_prompt.txt"]
        for i_file in instruction_files:
            p = source_dir / i_file
            if p.exists():
                try:
                    with open(p, "r", encoding="utf-8") as f:
                        instructions = f.read()
                    break
                except Exception as e:
                    print(f"Warning: Failed to read {i_file}: {e}")
                    
        if not instructions:
            instructions = "No explicit instructions file found during conversion. Please add instructions here."

        # Generate SKILL.md
        skill_md_path = dest_dir / "SKILL.md"
        with open(skill_md_path, "w", encoding="utf-8") as f:
            f.write("---\n")
            yaml.dump(metadata, f, default_flow_style=False, sort_keys=False)
            f.write("---\n\n")
            f.write(instructions)

        ignore_files = set(metadata_files + yaml_files + instruction_files)
        
        for item in source_dir.iterdir():
            if item.name in ignore_files:
                continue
                
            dest_item = dest_dir / item.name
            if item.is_dir():
                shutil.copytree(item, dest_item, dirs_exist_ok=True)
            else:
                shutil.copy2(item, dest_item)

    finally:
        if temp_dir is not None:
            shutil.rmtree(temp_dir)
