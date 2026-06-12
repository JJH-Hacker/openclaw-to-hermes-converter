# Openclaw ➔ Hermes Skill Converter

A fast, heuristic-based converter that seamlessly translates agent skills from the Openclaw ecosystem to the Hermes agent format (adhering to the `agentskills.io` standard).

## Features

- **Cross-Platform GUI App**: A gorgeous PyQt6 native application with drag-and-drop support, available for both **Windows** and **macOS**.
- **`.skill` Zip Support**: Automatically unzips `.skill` or `.zip` archives on the fly.
- **Native Format Detection**: Automatically detects if the Openclaw skill already contains a `SKILL.md` (native format) and copies it intelligently.
- **Legacy Conversion**: Scans for legacy Openclaw metadata files (`manifest.json`, `config.yaml`, `metadata.json`) and legacy instructions (`instructions.txt`, `prompt.txt`, `README.md`), and transforms them into YAML frontmatter and Markdown content.
- **ZIP Export**: Export converted skills to standard `.zip` files easily.

## Download / Installation (Ready to Use)

You don't need to install Python to run this! You can download the pre-built executables directly from the [GitHub Actions](https://github.com/JJH-Hacker/openclaw-to-hermes-converter/actions) tab.

1. Go to the **Actions** tab.
2. Click on the latest successful workflow run (e.g., "Add UI improvements and GitHub Actions...").
3. Scroll down to the **Artifacts** section at the bottom.
4. Download the version for your operating system:
   - **`SkillConverter-Windows`** (contains the `.exe` file for Windows)
   - **`SkillConverter-Mac`** (contains the `.app` bundle for macOS)
5. Extract the downloaded zip file and run the application!

## Running from Source (Developers)

If you prefer to run the application from source using Python:

1. Install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Run the GUI application:
   ```bash
   python app.py
   ```

### Command Line Interface (CLI)
You can also run the converter without the GUI:
```bash
python main.py -s /path/to/openclaw.skill
```
This will automatically generate a new Hermes-compatible folder named `openclaw_hermes` next to the original file.

## How to Build Executables Locally

If you want to build the standalone executables yourself:

**macOS:**
```bash
chmod +x build_app.sh
./build_app.sh
```
You'll find `SkillConverter.app` in the `dist/` directory.

**Windows:**
```bash
pyinstaller --windowed --onefile --name "SkillConverter" app.py
```
You'll find `SkillConverter.exe` in the `dist/` directory.
