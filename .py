from pathlib import Path
import argparse

from PIL import Image, ImageDraw, ImageColor

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
        description="Resize images to a square, add an inner border, and convert to PNG."
    )
    parser.add_argument(
        "--size", type=int, default=128, help="Output width and height (default: 128)."
    )
    parser.add_argument(
        "--border-color",
        default="#111",
        help="Border color in hex or a Pillow-supported color name (default: #111).",
    )
    parser.add_argument(
        "--border-thickness",
        type=int,
        default=4,
        help="Inner border thickness in pixels (default: 4).",
    )
    args = parser.parse_args()

    if args.size <= 0:
        parser.error("--size must be greater than zero.")

    if args.border_thickness < 0:
        parser.error("--border-thickness cannot be negative.")

    if args.border_thickness * 2 > args.size:
        parser.error("Border thickness cannot exceed half the image size.")

    try:
        border_color = ImageColor.getcolor(args.border_color, "RGBA")
    except ValueError:
        parser.error(f"Invalid border color: {args.border_color}")

    folder = Path(__file__).resolve().parent
    output_folder = folder / "output"
    output_folder.mkdir(exist_ok=True)

    images = [
        file
        for file in folder.iterdir()
        if file.is_file() and file.suffix.lower() in SUPPORTED_EXTENSIONS
    ]

    if not images:
        print("No supported images found.")
        return

    processed = 0

    for image_path in images:
        try:
            with Image.open(image_path) as source:
                # Use the first frame for animated images.
                source.seek(0)

                # Preserve transparency and enforce a square canvas.
                img = source.convert("RGBA")
                img = img.resize((args.size, args.size), Image.Resampling.LANCZOS)

                # Draw the border inside the existing canvas.
                if args.border_thickness > 0:
                    draw = ImageDraw.Draw(img)
                    draw.rectangle(
                        (0, 0, args.size - 1, args.size - 1),
                        outline=border_color,
                        width=args.border_thickness,
                    )

                output_path = output_folder / f"{image_path.stem}.png"
                img.save(output_path, format="PNG")

                processed += 1
                print(f"✓ {image_path.name} -> output/{output_path.name}")

        except Exception as error:
            print(f"✗ Failed: {image_path.name}: {error}")

    print(f"\nDone! Processed {processed}/{len(images)} image(s).")
    print(f"Output: {output_folder}")


if __name__ == "__main__":
    main()
