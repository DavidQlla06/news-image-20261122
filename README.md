# The World in One Image — Sunday, 22 November 2026

A one-page newspaper front page summing up the world news of Sunday
22 November 2026, built for the make.fun competition
`news-image-20261122`.

## Stories on the page

- **Lead:** Iran strikes a US air base in Kuwait and targets Bahrain,
  as tanker incidents near Hormuz widen the Gulf attacks.
- COP31 climate talks deadlocked over fossil fuels.
- Mexican forces capture cartel boss 'El Chapo Isidro'.
- Russian missile strike on Kryvyi Rih kills two, injures about 60.
- Magnitude 6.9 earthquake shakes Peru's Andes.
- Estonia to close its border with Russia.
- Air Niugini plane lands safely after an engine fire warning.

## How it works

- `stories.json` holds the day's stories (kicker, headline, summary,
  pictogram motif).
- `generate.py` draws the 1024x1024 front page with Pillow: masthead,
  lead panel, a 2x2 story grid and a bottom strip. Every pictogram is
  drawn from shapes in code; nothing is downloaded.
- `main.py` copies the committed `entry.png` to `MAKEFUN_OUTPUT_DIR`
  (or `/output`).

The output is deterministic: the same `stories.json` always produces
byte-identical `entry.png`.

## Run it

```
python3 generate.py          # writes ./entry.png (needs Pillow)
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see `LICENSE`.

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/DavidQlla06/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/DavidQlla06/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
