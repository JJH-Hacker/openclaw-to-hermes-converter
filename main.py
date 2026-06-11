import argparse
import sys
from pathlib import Path
from converter import convert_skill

def main():
    parser = argparse.ArgumentParser(
        description="Convert an Openclaw skill (directory or .skill zip) to a Hermes agent skill format."
    )
    parser.add_argument(
        "--source",
        "-s",
        required=True,
        type=Path,
        help="Path to the source Openclaw skill (directory or .skill/.zip file)."
    )
    parser.add_argument(
        "--dest",
        "-d",
        required=False,
        type=Path,
        help="Path to the destination Hermes skill directory. Defaults to {source_name}_hermes in the same directory."
    )

    args = parser.parse_args()

    source_path = args.source
    
    if args.dest:
        dest_dir = args.dest
    else:
        # Auto-generate destination: {name}_hermes
        name = source_path.stem if source_path.is_file() else source_path.name
        dest_dir = source_path.with_name(f"{name}_hermes")

    if not source_path.exists():
        print(f"Error: Source '{source_path}' does not exist.")
        sys.exit(1)

    print(f"Converting Openclaw skill from '{source_path}' to Hermes skill at '{dest_dir}'...")
    try:
        convert_skill(source_path, dest_dir)
        print("Conversion completed successfully!")
    except Exception as e:
        print(f"An error occurred during conversion: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
