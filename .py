from pathlib import Path
import argparse
from PIL import Image

# Supported input formats
SUPPORTED_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".bmp",
    ".gif",
    ".tiff",
    ".tif",
    ".ico",
    ".avif",
}


def main():
    parser = argparse.ArgumentParser(
        description="Resize images to a square and convert them to PNG."
    )
    parser.add_argument(
        "--size",
        type=int,
        default=128,
        help="Output width and height in pixels (default: 128).",
    )
    args = parser.parse_args()

    if args.size <= 0:
        parser.error("--size must be greater than zero.")

    # Always work relative to this script's location
    folder = Path(__file__).resolve().parent
    output_folder = folder / "output"
    output_folder.mkdir(exist_ok=True)

    images = [
        file
        for file in folder.iterdir()
        if file.is_file()
        and file.suffix.lower() in SUPPORTED_EXTENSIONS
        and file.parent != output_folder
    ]

    if not images:
        print("No supported images found.")
        return

    for image_path in images:
        try:
            with Image.open(image_path) as img:
                # Preserve transparency when present
                has_alpha = img.mode in ("RGBA", "LA") or "transparency" in img.info

                img = img.convert("RGBA" if has_alpha else "RGB")

                # Enforce an exact square size
                img = img.resize((args.size, args.size), Image.Resampling.LANCZOS)

                # Convert every output to PNG
                output_path = output_folder / (image_path.stem + ".png")

                img.save(output_path, format="PNG")

                print(f"✓ {image_path.name} -> output/{output_path.name}")

        except Exception as error:
            print(f"✗ Failed to process {image_path.name}: {error}")

    print(f"\nDone! Processed {len(images)} image(s).")
    print(f"Output folder: {output_folder}")


if __name__ == "__main__":
    main()
