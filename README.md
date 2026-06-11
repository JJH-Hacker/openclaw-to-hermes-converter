# Openclaw ➔ Hermes Skill Converter

A fast, heuristic-based converter that seamlessly translates agent skills from the Openclaw ecosystem to the Hermes agent format (adhering to the `agentskills.io` standard).

## Features

- **Mac App Support**: A gorgeous PyQt6 native Mac application with drag-and-drop support.
- **`.skill` Zip Support**: Automatically unzips `.skill` or `.zip` archives on the fly.
- **Native Format Detection**: Automatically detects if the Openclaw skill already contains a `SKILL.md` (native format) and copies it intelligently.
- **Legacy Conversion**: Scans for legacy Openclaw metadata files (`manifest.json`, `config.yaml`, `metadata.json`) and legacy instructions (`instructions.txt`, `prompt.txt`, `README.md`), and transforms them into YAML frontmatter and Markdown content.
- **ZIP Export**: Export converted skills to standard `.zip` files easily.

## How to Run the GUI App

1. Install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   python app.py
   ```
3. Drag and drop any `.skill` file or folder!

## How to Build the Mac App

Run the included build script to package the script into a standalone Mac `.app` bundle:

```bash
chmod +x build_app.sh
./build_app.sh
```

You'll find `SkillConverter.app` in the `dist/` directory.

## CLI Usage

If you prefer the command line:

```bash
python main.py -s /path/to/openclaw.skill
```
This will automatically generate a new Hermes-compatible folder named `openclaw_hermes` next to the original file.
