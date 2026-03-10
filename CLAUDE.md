# Poker Math Course Website

## Project Overview
A static website for a course based on "The Mathematics of Poker" by Bill Chen and Jerrod Ankenman. The site serves as a structured learning platform with chapter-by-chapter navigation and downloadable PDF content.

## Project Structure
```
Poker_Math_Course/
├── index.html              # Main page with table of contents
├── css/
│   └── style.css           # Site styles
├── js/
│   └── main.js             # Interactive functionality
├── chapters/               # Individual chapter PDFs
│   ├── chapter-01.pdf
│   ├── ...
│   └── chapter-30.pdf
├── The_Mathematics_of_Poker.pdf  # Full source PDF
├── CLAUDE.md               # This file
└── README.md
```

## Development Notes
- This is a static site — no build step required
- Open `index.html` directly in a browser or use any static file server
- Chapter PDFs are split from the main PDF using page ranges defined in the splitting script
- CSS uses a card/poker-themed dark color scheme
