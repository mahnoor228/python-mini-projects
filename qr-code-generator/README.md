# QR Code Generator

Turns any text or URL into a QR code image — point your phone camera at it
and it opens the link.

## How to run

```bash
pip install -r requirements.txt
python qr_generator.py "https://example.com"
python qr_generator.py "Hello, world!" -o hello.png
python qr_generator.py "https://example.com" --fill-color black
```

## Options

| Argument | Default | What it does |
| --- | --- | --- |
| `text` | — | Text or URL to encode in the QR code. |
| `-o`, `--output` | `qr_code.png` | Output image file. |
| `--fill-color` | `#6aff9b` | QR module color. |
| `--back-color` | `white` | Background color. |
| `--box-size` | `10` | Pixels per QR module. |
| `--border` | `4` | Modules of quiet-zone border. |

## Requirements

Python 3.10+ and the `qrcode` library (with Pillow for image output):

```bash
pip install -r requirements.txt
```

This is the only project in the repo that needs an install — everything
else is standard library only.
