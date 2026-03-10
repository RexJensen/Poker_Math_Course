# Poker Math Course Website

## Project Overview
A static website for a course based on "The Mathematics of Poker" by Bill Chen and Jerrod Ankenman. The site serves as a structured learning platform with chapter-by-chapter navigation, downloadable PDF content, and animated video explanations.

## Project Structure
```
Poker_Math_Course/
├── index.html              # Main page with table of contents
├── css/
│   └── style.css           # Site styles (dark poker theme)
├── js/
│   └── main.js             # Progress bar & video toggle logic
├── chapters/               # Individual chapter PDFs
│   ├── chapter-01.pdf … chapter-30.pdf
│   └── appendix-*.pdf, front/back-matter.pdf
├── animations/             # Manim animations (one folder per chapter)
│   ├── ch01/
│   │   ├── *.py            # Manim scene source
│   │   ├── script.md       # Narration script with timestamps
│   │   └── video/*.mp4     # Rendered output (tracked in git)
│   ├── ch03/
│   │   └── ...
│   └── ...
├── The_Mathematics_of_Poker.pdf
├── CLAUDE.md               # This file
└── README.md
```

## Development Notes
- This is a static site — no build step required
- Open `index.html` directly in a browser or use any static file server
- Chapter PDFs are split from the main PDF using page ranges defined in the splitting script
- CSS uses a card/poker-themed dark color scheme

## Animation Conventions
- Each chapter animation lives in `animations/chXX/`
- Manim source `.py` file + narration `script.md` + rendered `video/*.mp4`
- Videos are embedded in `index.html` with a toggle button per chapter
- Use the shared color palette: CRIMSON (#c9362c), GOLD (#d4a017), TEAL (#2eaf7d), SLATE (#5a7d9a), DARKBG (#1a1a2e)
- Render command: `manim -ql animations/chXX/filename.py ClassName`
- The `media/` directory (Manim build cache) is gitignored; only final `.mp4` in `animations/chXX/video/` is committed
