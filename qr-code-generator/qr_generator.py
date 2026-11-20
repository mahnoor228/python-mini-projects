#!/usr/bin/env python3
"""Generate a QR code image from text or a URL.

Usage:
    python qr_generator.py "https://example.com"
    python qr_generator.py "Hello, world!" -o hello.png
    python qr_generator.py "https://example.com" --fill-color black

Needs the qrcode library (with Pillow for image output):
    pip install -r requirements.txt
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import qrcode
    from qrcode.constants import ERROR_CORRECT_M
except ImportError:
    print(
        "Error: the 'qrcode' library is not installed.\n"
        "Install it with: pip install -r requirements.txt",
        file=sys.stderr,
    )
    raise SystemExit(1)


def generate_qr_code(
    text: str,
    file_name: str,
    fill_color: str = "#6aff9b",
    back_color: str = "white",
    box_size: int = 10,
    border: int = 4,
) -> Path:
    """Generate a QR code for text and save it as an image file.

    Returns the path of the saved image.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=ERROR_CORRECT_M,
        box_size=box_size,
        border=border,
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    output = Path(file_name)
    img.save(output)
    return output


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate a QR code image from text or a URL."
    )
    parser.add_argument("text", help="text or URL to encode in the QR code")
    parser.add_argument("-o", "--output", default="qr_code.png",
                        help="output image file (default: qr_code.png)")
    parser.add_argument("--fill-color", default="#6aff9b",
                        help="QR module color (default: #6aff9b green)")
    parser.add_argument("--back-color", default="white",
                        help="background color (default: white)")
    parser.add_argument("--box-size", type=int, default=10,
                        help="pixels per QR module (default: 10)")
    parser.add_argument("--border", type=int, default=4,
                        help="modules of quiet-zone border (default: 4)")
    args = parser.parse_args(argv)

    output = generate_qr_code(
        args.text,
        args.output,
        fill_color=args.fill_color,
        back_color=args.back_color,
        box_size=args.box_size,
        border=args.border,
    )
    print(f"QR code saved as {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
