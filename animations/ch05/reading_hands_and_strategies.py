"""
Chapter 5 — Scientific Tarot: Reading Hands and Strategies
==========================================================

Manim animation covering all key concepts from Chapter 5 of
"The Mathematics of Poker" by Bill Chen & Jerrod Ankenman.

Topics covered:
  1. Hand reading as Bayesian inference vs single-hand guessing
  2. The A8 vs AK satellite story — distributional thinking
  3. Range narrowing through progressive action
  4. Four types of information sources for reads
  5. Sample size limitations (~100 showdowns in 1000 hands)
  6. Player archetypes: Maniac, Rock, Calling Station
  7. Tells as Bayesian process — P(bluff|tell) with false positives
  8. Confirmation bias and pattern illusions
  9. Key takeaways

See script.md for the full narration script with timestamps.

RENDER
------
    pip install manim
    # Low quality preview:
    manim -pql animations/ch05/reading_hands_and_strategies.py ReadingHandsAndStrategies
    # High quality render:
    manim -qh animations/ch05/reading_hands_and_strategies.py ReadingHandsAndStrategies
"""

from manim import *
import numpy as np

# ── Shared poker-themed palette ──
CRIMSON   = "#c9362c"
GOLD      = "#d4a017"
TEAL      = "#2eaf7d"
SLATE     = "#5a7d9a"
CHARCOAL  = "#3a3a3a"
DARKBG    = "#1a1a2e"
SOFTWHITE = "#e0e0e0"
NAVY      = "#0d1b2a"


class ReadingHandsAndStrategies(Scene):
    """Full Chapter 5 animation — Reading Hands & Strategies."""

    def construct(self):
        self.camera.background_color = DARKBG
        self.play_title()
        self.play_single_hand_fallacy()
        self.play_distributional_thinking()
        self.play_range_narrowing()
        self.play_information_sources()
        self.play_sample_size_problem()
        self.play_player_archetypes()
        self.play_tells_as_bayes()
        self.play_key_takeaways()

    # ───────────────────── helpers ─────────────────────

    def section_header(self, text, color=GOLD):
        """Fade in a section header, wait, then fade out."""
        header = Text(text, font_size=32, color=color, weight=BOLD)
        header.to_edge(UP, buff=0.4)
        self.play(FadeIn(header, shift=DOWN * 0.2), run_time=0.6)
        return header

    def clear_all(self, *mobjects, run_time=0.6):
        if mobjects:
            self.play(*[FadeOut(m) for m in mobjects], run_time=run_time)

    def make_card(self, rank, suit, suit_color):
        """Create a playing-card Mobject."""
        bg = RoundedRectangle(
            width=0.9, height=1.3, corner_radius=0.07,
            fill_color="#f5f5f0", fill_opacity=1.0,
            stroke_color="#333", stroke_width=2,
        )
        r = Text(rank, font_size=28, color="#111", weight=BOLD)
        s = Text(suit, font_size=24, color=suit_color)
        r.move_to(bg.get_center() + UP * 0.18)
        s.move_to(bg.get_center() + DOWN * 0.22)
        return VGroup(bg, r, s)

    # ───────────────────── scenes ─────────────────────

    def play_title(self):
        title = Text("Reading Hands & Strategies", font_size=48,
                      color=WHITE, weight=BOLD)
        subtitle = Text("The Mathematics of Poker — Chapter 5",
                        font_size=24, color=SOFTWHITE)
        subtitle.next_to(title, DOWN, buff=0.4)

        suits = Text("♠ ♥ ♦ ♣", font_size=36, color=CRIMSON)
        suits.next_to(subtitle, DOWN, buff=0.6)

        quote = Text(
            '"Hand reading is not psychic guesswork —\n'
            'it is Bayesian inference applied to incomplete information."',
            font_size=18, color=SLATE, slant=ITALIC,
        )
        quote.next_to(suits, DOWN, buff=0.6)

        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle, shift=UP * 0.3), run_time=0.8)
        self.play(FadeIn(suits), run_time=0.5)
        self.play(FadeIn(quote, shift=UP * 0.2), run_time=0.8)
        self.wait(2)
        self.clear_all(title, subtitle, suits, quote)

    # ── 1. Single hand fallacy ──

    def play_single_hand_fallacy(self):
        header = self.section_header("The Single-Hand Fallacy")

        # LEFT side: the WRONG approach
        wrong_title = Text("WRONG", font_size=26, color=CRIMSON, weight=BOLD)
        wrong_title.shift(LEFT * 3.5 + UP * 1.5)

        wrong_box = RoundedRectangle(
            width=4.5, height=3.5, corner_radius=0.15,
            fill_color=NAVY, fill_opacity=0.8,
            stroke_color=CRIMSON, stroke_width=2,
        )
        wrong_box.next_to(wrong_title, DOWN, buff=0.3)

        wrong_text = Text(
            '"He has AK."',
            font_size=22, color=CRIMSON, weight=BOLD,
        )
        wrong_text.move_to(wrong_box.get_center() + UP * 0.8)

        ak_cards = VGroup(
            self.make_card("A", "♠", WHITE),
            self.make_card("K", "♥", CRIMSON),
        ).arrange(RIGHT, buff=0.2)
        ak_cards.move_to(wrong_box.get_center())

        wrong_note = Text(
            "Single point estimate\nFragile, often wrong",
            font_size=16, color=SLATE, line_spacing=1.3,
        )
        wrong_note.move_to(wrong_box.get_center() + DOWN * 1.0)

        # Cross out
        cross1 = Line(
            wrong_box.get_corner(UL) + RIGHT * 0.2 + DOWN * 0.2,
            wrong_box.get_corner(DR) + LEFT * 0.2 + UP * 0.2,
            color=CRIMSON, stroke_width=4,
        )
        cross2 = Line(
            wrong_box.get_corner(UR) + LEFT * 0.2 + DOWN * 0.2,
            wrong_box.get_corner(DL) + RIGHT * 0.2 + UP * 0.2,
            color=CRIMSON, stroke_width=4,
        )

        # RIGHT side: the RIGHT approach
        right_title = Text("RIGHT", font_size=26, color=TEAL, weight=BOLD)
        right_title.shift(RIGHT * 3.5 + UP * 1.5)

        right_box = RoundedRectangle(
            width=4.5, height=3.5, corner_radius=0.15,
            fill_color=NAVY, fill_opacity=0.8,
            stroke_color=TEAL, stroke_width=2,
        )
        right_box.next_to(right_title, DOWN, buff=0.3)

        right_text = Text(
            '"He has a RANGE."',
            font_size=22, color=TEAL, weight=BOLD,
        )
        right_text.move_to(right_box.get_center() + UP * 0.8)

        range_hands = Text(
            "AA  KK  QQ  AKs\nAKo  AQs  JJ  TT\nAQo  KQs  99  ...",
            font_size=18, color=SOFTWHITE, line_spacing=1.2,
        )
        range_hands.move_to(right_box.get_center() + DOWN * 0.1)

        right_note = Text(
            "Probability distribution\nRobust, updatable",
            font_size=16, color=SLATE, line_spacing=1.3,
        )
        right_note.move_to(right_box.get_center() + DOWN * 1.0)

        # Animate
        self.play(FadeIn(wrong_title), FadeIn(wrong_box), run_time=0.6)
        self.play(FadeIn(wrong_text), FadeIn(ak_cards), FadeIn(wrong_note),
                  run_time=0.8)
        self.wait(0.5)
        self.play(Create(cross1), Create(cross2), run_time=0.6)

        self.play(FadeIn(right_title), FadeIn(right_box), run_time=0.6)
        self.play(FadeIn(right_text), FadeIn(range_hands), FadeIn(right_note),
                  run_time=0.8)
        self.wait(2)
        self.clear_all(header, wrong_title, wrong_box, wrong_text, ak_cards,
                        wrong_note, cross1, cross2,
                        right_title, right_box, right_text, range_hands,
                        right_note)

    # ── 2. Distributional thinking ──

    def play_distributional_thinking(self):
        header = self.section_header("Distributional Thinking")

        # The A8 vs AK satellite story
        story_title = Text(
            "The Satellite Story: A8 vs AK",
            font_size=24, color=GOLD, weight=BOLD,
        )
        story_title.shift(UP * 1.5)

        # Show the hero's hand
        hero_cards = VGroup(
            self.make_card("A", "♦", CRIMSON),
            self.make_card("8", "♦", CRIMSON),
        ).arrange(RIGHT, buff=0.2)
        hero_cards.shift(LEFT * 4 + DOWN * 0.2)
        hero_label = Text("Hero: A8", font_size=18, color=SOFTWHITE)
        hero_label.next_to(hero_cards, DOWN, buff=0.2)

        # Show the opponent's actual hand
        villain_cards = VGroup(
            self.make_card("A", "♠", WHITE),
            self.make_card("K", "♠", WHITE),
        ).arrange(RIGHT, buff=0.2)
        villain_cards.shift(RIGHT * 4 + DOWN * 0.2)
        villain_label = Text("Villain: AK", font_size=18, color=SOFTWHITE)
        villain_label.next_to(villain_cards, DOWN, buff=0.2)

        self.play(FadeIn(story_title), run_time=0.6)
        self.play(FadeIn(hero_cards), FadeIn(hero_label), run_time=0.8)
        self.play(FadeIn(villain_cards), FadeIn(villain_label), run_time=0.8)
        self.wait(0.5)

        # Key insight
        insight_box = RoundedRectangle(
            width=8, height=2.2, corner_radius=0.15,
            fill_color=NAVY, fill_opacity=0.9,
            stroke_color=TEAL, stroke_width=2,
        ).to_edge(DOWN, buff=0.4)

        insight_text = VGroup(
            Text("The call was CORRECT against villain's full range,",
                 font_size=20, color=SOFTWHITE),
            Text("even though villain happened to hold AK specifically.",
                 font_size=20, color=SOFTWHITE),
            Text("", font_size=8),
            Text("Evaluate decisions against ranges, not results.",
                 font_size=22, color=TEAL, weight=BOLD),
        ).arrange(DOWN, buff=0.15)
        insight_text.move_to(insight_box.get_center())

        self.play(FadeIn(insight_box), run_time=0.4)
        self.play(FadeIn(insight_text), run_time=1.0)
        self.wait(2)
        self.clear_all(header, story_title, hero_cards, hero_label,
                        villain_cards, villain_label, insight_box, insight_text)

    # ── 3. Range narrowing ──

    def play_range_narrowing(self):
        header = self.section_header("Range Narrowing Through Actions")

        # Define hand categories with colors
        hand_labels = [
            "AA", "KK", "QQ", "JJ", "TT", "99",
            "AKs", "AKo", "AQs", "AQo", "KQs", "KQo",
            "AJs", "KJs", "QJs", "JTs", "T9s", "98s",
        ]

        # Create a grid of hand rectangles
        grid = VGroup()
        hand_rects = []
        cols = 6
        for i, label in enumerate(hand_labels):
            row = i // cols
            col = i % cols
            rect = RoundedRectangle(
                width=1.0, height=0.6, corner_radius=0.05,
                fill_color=TEAL, fill_opacity=0.7,
                stroke_color=SOFTWHITE, stroke_width=1,
            )
            txt = Text(label, font_size=14, color=WHITE, weight=BOLD)
            txt.move_to(rect.get_center())
            cell = VGroup(rect, txt)
            cell.move_to(np.array([
                (col - 2.5) * 1.15,
                (1.0 - row) * 0.75 + 0.5,
                0
            ]))
            grid.add(cell)
            hand_rects.append(rect)

        full_label = Text(
            "Full opening range (18 hand types)",
            font_size=18, color=SOFTWHITE,
        )
        full_label.to_edge(DOWN, buff=1.8)

        self.play(
            *[FadeIn(cell, shift=UP * 0.1) for cell in grid],
            FadeIn(full_label),
            run_time=1.0,
        )
        self.wait(1)

        # Step 1: Opponent raises preflop — eliminate weakest hands
        step1 = Text("Opponent RAISES preflop", font_size=20,
                      color=GOLD, weight=BOLD)
        step1.to_edge(DOWN, buff=1.2)

        # Fade out the bottom row (weaker suited connectors)
        eliminate_1 = [12, 13, 14, 15, 16, 17]  # AJs, KJs, QJs, JTs, T9s, 98s
        self.play(
            FadeOut(full_label),
            FadeIn(step1),
            *[grid[i][0].animate.set_fill(CHARCOAL, opacity=0.2) for i in eliminate_1],
            *[grid[i][1].animate.set_opacity(0.2) for i in eliminate_1],
            run_time=1.0,
        )
        self.wait(1)

        # Step 2: Bets flop on A-7-2 rainbow
        step2 = Text("Bets flop: A-7-2 rainbow", font_size=20,
                      color=GOLD, weight=BOLD)
        step2.to_edge(DOWN, buff=1.2)

        # Eliminate mid pairs without an ace
        eliminate_2 = [4, 5, 10, 11]  # TT, 99, KQs, KQo
        self.play(
            FadeOut(step1),
            FadeIn(step2),
            *[grid[i][0].animate.set_fill(CHARCOAL, opacity=0.2) for i in eliminate_2],
            *[grid[i][1].animate.set_opacity(0.2) for i in eliminate_2],
            run_time=1.0,
        )
        self.wait(1)

        # Step 3: Bets turn aggressively
        step3 = Text("Bets turn aggressively", font_size=20,
                      color=GOLD, weight=BOLD)
        step3.to_edge(DOWN, buff=1.2)

        # Eliminate more — only premiums remain
        eliminate_3 = [3, 8, 9]  # JJ, AQs, AQo
        self.play(
            FadeOut(step2),
            FadeIn(step3),
            *[grid[i][0].animate.set_fill(CHARCOAL, opacity=0.2) for i in eliminate_3],
            *[grid[i][1].animate.set_opacity(0.2) for i in eliminate_3],
            run_time=1.0,
        )
        self.wait(0.5)

        # Highlight remaining
        remaining = [0, 1, 2, 6, 7]  # AA, KK, QQ, AKs, AKo
        result_label = Text(
            "Remaining: AA, KK, QQ, AKs, AKo",
            font_size=20, color=TEAL, weight=BOLD,
        )
        result_label.to_edge(DOWN, buff=0.5)

        self.play(
            FadeIn(result_label),
            *[grid[i][0].animate.set_fill(CRIMSON, opacity=0.8) for i in remaining],
            run_time=0.8,
        )
        self.wait(2)
        self.clear_all(header, grid, step3, result_label)

    # ── 4. Information sources ──

    def play_information_sources(self):
        header = self.section_header("Four Types of Evidence")

        sources = [
            ("1. Direct Evidence", "Showdown results", "Most reliable, least frequent", TEAL),
            ("2. Opponent-Controlled", "Voluntary card shows", "Biased sample — beware!", GOLD),
            ("3. Indirect Evidence", "Betting patterns & frequencies", "Large sample needed", CRIMSON),
            ("4. Classification", "Player type correlation", "Rough heuristic only", SLATE),
        ]

        cards = VGroup()
        for i, (title, desc, note, color) in enumerate(sources):
            box = RoundedRectangle(
                width=5.5, height=1.2, corner_radius=0.1,
                fill_color=NAVY, fill_opacity=0.9,
                stroke_color=color, stroke_width=2,
            )
            t = Text(title, font_size=20, color=color, weight=BOLD)
            t.move_to(box.get_center() + UP * 0.25 + LEFT * 1.0)
            d = Text(desc, font_size=16, color=SOFTWHITE)
            d.move_to(box.get_center() + DOWN * 0.1 + LEFT * 1.0)
            n = Text(note, font_size=14, color=SLATE, slant=ITALIC)
            n.move_to(box.get_center() + DOWN * 0.35 + LEFT * 1.0)
            card = VGroup(box, t, d, n)
            cards.add(card)

        cards.arrange(DOWN, buff=0.15)
        cards.move_to(ORIGIN + DOWN * 0.2)

        for card in cards:
            self.play(FadeIn(card, shift=RIGHT * 0.3), run_time=0.7)
            self.wait(0.3)

        self.wait(2)
        self.clear_all(header, cards)

    # ── 5. Sample size problem ──

    def play_sample_size_problem(self):
        header = self.section_header("The Sample Size Problem")

        # Key statistic
        stat1 = Text("1,000 hands played", font_size=28, color=SOFTWHITE)
        stat1.shift(UP * 2)

        arrow1 = Arrow(
            stat1.get_bottom(), stat1.get_bottom() + DOWN * 0.8,
            color=GOLD, stroke_width=2, buff=0.1,
        )

        stat2 = Text("~ 100 showdowns", font_size=28, color=GOLD, weight=BOLD)
        stat2.next_to(arrow1, DOWN, buff=0.1)

        self.play(FadeIn(stat1), run_time=0.6)
        self.play(GrowArrow(arrow1), run_time=0.4)
        self.play(FadeIn(stat2), run_time=0.6)
        self.wait(1)

        # Confidence interval visualization
        ci_title = Text(
            "If opponent raises 10% UTG, 95% CI:",
            font_size=20, color=SOFTWHITE,
        )
        ci_title.shift(DOWN * 0.3)

        # Draw a number line for the CI
        line = Line(LEFT * 4, RIGHT * 4, color=SOFTWHITE, stroke_width=2)
        line.shift(DOWN * 1.2)

        # Tick marks at key percentages
        ticks = VGroup()
        tick_labels = VGroup()
        for pct in [0, 4, 10, 16, 20]:
            x_pos = (pct / 20) * 8 - 4
            tick = Line(
                np.array([x_pos, -1.05, 0]),
                np.array([x_pos, -1.35, 0]),
                color=SOFTWHITE, stroke_width=2,
            )
            label = Text(f"{pct}%", font_size=14, color=SOFTWHITE)
            label.next_to(tick, DOWN, buff=0.1)
            ticks.add(tick)
            tick_labels.add(label)

        # CI range highlight
        ci_left = (4 / 20) * 8 - 4
        ci_right = (16 / 20) * 8 - 4
        ci_bar = Line(
            np.array([ci_left, -1.2, 0]),
            np.array([ci_right, -1.2, 0]),
            color=CRIMSON, stroke_width=8,
        )

        # True value marker
        true_x = (10 / 20) * 8 - 4
        true_dot = Circle(
            radius=0.1, color=TEAL,
            fill_color=TEAL, fill_opacity=1.0,
        )
        true_dot.move_to(np.array([true_x, -1.2, 0]))

        ci_label = Text(
            "95% CI: [4%, 16%]",
            font_size=22, color=CRIMSON, weight=BOLD,
        )
        ci_label.shift(DOWN * 2.0)

        warning = Text(
            "We cannot distinguish tight from loose!",
            font_size=20, color=GOLD, weight=BOLD,
        )
        warning.shift(DOWN * 2.6)

        self.play(FadeIn(ci_title), run_time=0.5)
        self.play(Create(line), run_time=0.5)
        self.play(
            *[Create(t) for t in ticks],
            *[FadeIn(l) for l in tick_labels],
            run_time=0.6,
        )
        self.play(Create(ci_bar), run_time=0.8)
        self.play(FadeIn(true_dot), run_time=0.3)
        self.play(FadeIn(ci_label), run_time=0.5)
        self.play(FadeIn(warning), run_time=0.6)
        self.wait(2.5)
        self.clear_all(header, stat1, arrow1, stat2, ci_title,
                        line, ticks, tick_labels, ci_bar, true_dot,
                        ci_label, warning)

    # ── 6. Player archetypes ──

    def play_player_archetypes(self):
        header = self.section_header("Player Archetypes")

        archetypes = [
            (
                "MANIAC",
                "Loose-Aggressive",
                "Plays too many hands\nBets and raises often",
                "Exploit: Trap with\nstrong hands",
                CRIMSON,
            ),
            (
                "ROCK",
                "Tight-Passive",
                "Plays very few hands\nRarely bluffs",
                "Exploit: Steal pots\nand fold to raises",
                SLATE,
            ),
            (
                "CALLING STATION",
                "Loose-Passive",
                "Calls with anything\nRarely raises or folds",
                "Exploit: Value bet\nrelentlessly",
                GOLD,
            ),
        ]

        columns = VGroup()
        for name, style, desc, exploit, color in archetypes:
            box = RoundedRectangle(
                width=3.8, height=4.5, corner_radius=0.15,
                fill_color=NAVY, fill_opacity=0.9,
                stroke_color=color, stroke_width=3,
            )
            name_txt = Text(name, font_size=22, color=color, weight=BOLD)
            name_txt.move_to(box.get_top() + DOWN * 0.4)

            style_txt = Text(style, font_size=16, color=SOFTWHITE, slant=ITALIC)
            style_txt.next_to(name_txt, DOWN, buff=0.2)

            divider = Line(LEFT * 1.5, RIGHT * 1.5, color=color, stroke_width=1)
            divider.next_to(style_txt, DOWN, buff=0.2)

            desc_txt = Text(desc, font_size=14, color=SOFTWHITE, line_spacing=1.2)
            desc_txt.next_to(divider, DOWN, buff=0.25)

            exploit_label = Text("Counter-strategy:", font_size=13,
                                  color=color, weight=BOLD)
            exploit_label.next_to(desc_txt, DOWN, buff=0.3)

            exploit_txt = Text(exploit, font_size=14, color=SOFTWHITE,
                               line_spacing=1.2)
            exploit_txt.next_to(exploit_label, DOWN, buff=0.15)

            col = VGroup(box, name_txt, style_txt, divider,
                         desc_txt, exploit_label, exploit_txt)
            columns.add(col)

        columns.arrange(RIGHT, buff=0.3)
        columns.move_to(ORIGIN + DOWN * 0.2)

        for col in columns:
            self.play(FadeIn(col, shift=UP * 0.2), run_time=0.8)
            self.wait(0.5)

        self.wait(2)
        self.clear_all(header, columns)

    # ── 7. Tells as Bayes ──

    def play_tells_as_bayes(self):
        header = self.section_header("Tells as Bayesian Inference")

        # Bayes formula
        formula = MathTex(
            r"P(\text{bluff} \mid \text{tell})",
            r"=",
            r"\frac{P(\text{tell} \mid \text{bluff}) \cdot P(\text{bluff})}"
            r"{P(\text{tell})}",
            font_size=34,
        )
        formula[0].set_color(TEAL)
        formula.shift(UP * 1.8)

        self.play(Write(formula), run_time=1.5)
        self.wait(1)

        # Numerical example — medical diagnosis analogy
        example_title = Text(
            "Example: \"Shaking hands\" tell",
            font_size=22, color=GOLD, weight=BOLD,
        )
        example_title.shift(UP * 0.6)

        params = VGroup(
            MathTex(r"P(\text{tell} \mid \text{bluff}) = 0.80",
                    font_size=24, color=SOFTWHITE),
            MathTex(r"P(\text{bluff}) = 0.10",
                    font_size=24, color=SOFTWHITE),
            MathTex(r"P(\text{tell} \mid \text{not bluff}) = 0.30",
                    font_size=24, color=SLATE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        params.shift(DOWN * 0.2)

        self.play(FadeIn(example_title), run_time=0.5)
        for p in params:
            self.play(FadeIn(p, shift=RIGHT * 0.2), run_time=0.5)

        # Calculate P(tell)
        p_tell = MathTex(
            r"P(\text{tell}) = 0.80 \times 0.10 + 0.30 \times 0.90 = 0.35",
            font_size=22, color=SLATE,
        )
        p_tell.shift(DOWN * 1.3)

        result = MathTex(
            r"P(\text{bluff} \mid \text{tell}) = \frac{0.08}{0.35} \approx 22.9\%",
            font_size=28, color=TEAL,
        )
        result.shift(DOWN * 2.0)

        warning = Text(
            "False positives dramatically reduce tell reliability!",
            font_size=18, color=CRIMSON, weight=BOLD,
        )
        warning.shift(DOWN * 2.7)

        self.play(FadeIn(p_tell), run_time=0.8)
        self.play(Write(result), run_time=1.0)
        self.play(FadeIn(warning), run_time=0.6)
        self.wait(2.5)
        self.clear_all(header, formula, example_title, params,
                        p_tell, result, warning)

    # ── 8. Key takeaways ──

    def play_key_takeaways(self):
        lines = VGroup(
            Text("Key Concepts — Chapter 5", font_size=36,
                 color=GOLD, weight=BOLD),
            Text("", font_size=10),
            Text("1.  Think in distributions, not single hands",
                 font_size=22, color=SOFTWHITE),
            Text("2.  Narrow ranges with each action — Bayesian updating",
                 font_size=22, color=SOFTWHITE),
            Text("3.  Small samples make reads unreliable (wide CIs)",
                 font_size=22, color=SOFTWHITE),
            Text("4.  Classify opponents but stay flexible",
                 font_size=22, color=SOFTWHITE),
            Text("5.  Tells are Bayesian — false positives kill accuracy",
                 font_size=22, color=SOFTWHITE),
            Text("", font_size=14),
            Text("Hand reading is science, not intuition.",
                 font_size=26, color=CRIMSON, weight=BOLD),
        )
        lines.arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        lines[0].set_x(0)
        lines[-1].set_x(0)
        lines.move_to(ORIGIN)

        for line in lines:
            self.play(FadeIn(line, shift=UP * 0.15), run_time=0.5)

        self.wait(3)
        self.play(FadeOut(lines), run_time=1)
