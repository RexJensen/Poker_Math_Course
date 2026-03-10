# Poker Math Course

A structured online course based on *The Mathematics of Poker* by Bill Chen and Jerrod Ankenman.

## About the Course

This course covers the mathematical foundations of poker strategy, organized into five parts:

1. **Basics** — Probability, expectation, variance, and Bayes' theorem
2. **Exploitive Play** — Pot odds, hand reading, online tells, and accurate play
3. **Optimal Play** — Game theory, bet sizing, multi-street games, and case studies
4. **Risk** — Risk of ruin, Kelly criterion, and bankroll management
5. **Other Topics** — Tournaments, multiplayer games, and putting it all together

## Getting Started

Open `index.html` in your browser to view the course table of contents and navigate to individual chapters.

## Structure

```
├── index.html              # Main course page with table of contents
├── css/style.css           # Site styles (dark poker theme)
├── js/main.js              # Progress bar & video toggles
├── chapters/               # Individual chapter PDFs
│   ├── chapter-01.pdf … chapter-30.pdf
│   ├── appendix-ch15.pdf, appendix-ch16.pdf
│   ├── front-matter.pdf, back-matter.pdf
│   └── ...
├── animations/             # Manim animations per chapter
│   ├── ch01/
│   │   ├── probability_and_expectation.py   # Manim source
│   │   ├── script.md                        # Narration script
│   │   └── video/                           # Rendered .mp4
│   ├── ch03/
│   │   ├── bayes_hand_reading.py
│   │   └── video/
│   └── ...                 # Future chapters follow same pattern
├── The_Mathematics_of_Poker.pdf
└── CLAUDE.md
```

## Animations

Each chapter can have an accompanying Manim animation that visualizes key concepts.

**Per-chapter layout:**
- `animations/chXX/` — one folder per chapter
  - `*.py` — Manim scene source code
  - `script.md` — Narration / voiceover script with timestamps
  - `video/` — Final rendered `.mp4` files (checked into git)

**Rendering an animation:**
```bash
pip install manim
# Low quality preview:
manim -pql animations/ch01/probability_and_expectation.py ProbabilityAndExpectation
# High quality render:
manim -qh animations/ch01/probability_and_expectation.py ProbabilityAndExpectation
```

## License

This project is for educational purposes. The content of *The Mathematics of Poker* is the intellectual property of its authors.
