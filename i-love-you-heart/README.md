# I Love You in 20 Languages — Heart in the Terminal

Prints "I love you" in 20 languages, one language per row, arranged so the
lines form a heart. It prints line by line, in alternating
red and pink, then lists all 20 languages with pronunciations.

## How to run

```bash
python heart.py            # line-by-line
python heart.py --fast     # print the whole heart at once
python heart.py --no-color --no-legend
```

## Options

| Flag | Default | What it does |
| --- | --- | --- |
| `--fast` | off | Print the whole heart at once, no delay. |
| `--delay` | 0.35 | Seconds between lines. |
| `--no-color` | off | Print without colour. |
| `--no-legend` | off | Skip the language list at the end. |

## How it works

The heart shape comes from the classic heart curve
`(x^2 + y^2 - 1)^3 - x^2 * y^3 <= 0`, sampled on a 72 x 25 grid.
That grid has exactly 20 non-empty rows, one for each language.
Each row is filled by repeating that row's phrase until it fills the
heart's width at that height. Wide CJK characters are counted as
two terminal columns so the shape stays aligned.

## Requirements

Python 3.10+, standard library only — no installs needed.
