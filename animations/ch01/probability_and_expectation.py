"""
Chapter 1 — Decisions Under Risk: Probability and Expectation
=============================================================

Manim animation covering all key concepts from Chapter 1 of
"The Mathematics of Poker" by Bill Chen & Jerrod Ankenman.

Topics covered:
  1. Utility vs money (why we simplify)
  2. Definition of probability (frequentist / limit definition)
  3. Counting: pocket aces (dependent events)
  4. Mutually exclusive events (addition rule)
  5. Independent vs dependent events
  6. Inclusion-exclusion principle (hearts OR aces)
  7. Flopping a flush (chain of conditional probabilities)
  8. Probability distributions (coin, die, poker hands)
  9. Expected value — fair bet, favorable bet, bad bet
 10. Additivity of EV
 11. Key takeaways

See script.md for the full narration script with timestamps.

RENDER
------
    pip install manim
    # Low quality preview:
    manim -pql animations/ch01/probability_and_expectation.py ProbabilityAndExpectation
    # High quality render:
    manim -qh animations/ch01/probability_and_expectation.py ProbabilityAndExpectation
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


class ProbabilityAndExpectation(Scene):
    """Full Chapter 1 animation — Probability & Expected Value."""

    def construct(self):
        self.camera.background_color = DARKBG
        self.play_title()
        self.play_utility_simplification()
        self.play_probability_definition()
        self.play_pocket_aces()
        self.play_mutually_exclusive()
        self.play_independent_vs_dependent()
        self.play_inclusion_exclusion()
        self.play_flush_probability()
        self.play_probability_distributions()
        self.play_expected_value_intro()
        self.play_ev_favorable()
        self.play_ev_bad_bet()
        self.play_ev_additive()
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
        title = Text("Probability & Expectation", font_size=48,
                      color=WHITE, weight=BOLD)
        subtitle = Text("The Mathematics of Poker — Chapter 1",
                        font_size=24, color=SOFTWHITE)
        subtitle.next_to(title, DOWN, buff=0.4)

        suits = Text("♠ ♥ ♦ ♣", font_size=36, color=CRIMSON)
        suits.next_to(subtitle, DOWN, buff=0.6)

        quote = Text(
            '"Maximizing total money won in poker requires\n'
            'that a player maximize the expected value of his decisions."',
            font_size=18, color=SLATE, slant=ITALIC,
        )
        quote.next_to(suits, DOWN, buff=0.6)

        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle, shift=UP * 0.3), run_time=0.8)
        self.play(FadeIn(suits), run_time=0.5)
        self.play(FadeIn(quote, shift=UP * 0.2), run_time=0.8)
        self.wait(2)
        self.clear_all(title, subtitle, suits, quote)

    # ── 1. Utility simplification ──

    def play_utility_simplification(self):
        header = self.section_header("Why Money, Not Utility?")

        # Utility curve
        axes = Axes(
            x_range=[0, 10, 2], y_range=[0, 1.1, 0.25],
            x_length=5, y_length=3,
            axis_config={"color": SOFTWHITE, "font_size": 20},
            tips=False,
        ).shift(LEFT * 0.5 + DOWN * 0.3)

        x_label = Text("Dollars (millions)", font_size=16, color=SOFTWHITE)
        x_label.next_to(axes.x_axis, DOWN, buff=0.25)
        y_label = Text("Utility", font_size=16, color=SOFTWHITE)
        y_label.next_to(axes.y_axis, UP, buff=0.15)

        curve = axes.plot(lambda x: 1 - np.exp(-0.4 * x), x_range=[0, 10],
                          color=TEAL, stroke_width=3)
        linear = axes.plot(lambda x: x / 10, x_range=[0, 10],
                           color=SLATE, stroke_width=2, stroke_opacity=0.5)
        lin_label = Text("Linear (money)", font_size=14, color=SLATE)
        lin_label.next_to(linear, UP, buff=0.1).shift(RIGHT * 0.5)
        curve_label = Text("Actual utility", font_size=14, color=TEAL)
        curve_label.next_to(curve.point_from_proportion(0.65), UP, buff=0.15)

        note = Text(
            "Assumption: players are well-bankrolled.\n"
            "Money won ≈ utility gained.",
            font_size=18, color=SOFTWHITE, line_spacing=1.3,
        )
        note.to_edge(RIGHT, buff=0.6).shift(DOWN * 0.3)

        arrow = Arrow(
            curve.point_from_proportion(0.5),
            note.get_left() + LEFT * 0.1,
            color=GOLD, stroke_width=2, buff=0.2,
        )

        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=1)
        self.play(Create(linear), FadeIn(lin_label), run_time=0.8)
        self.play(Create(curve), FadeIn(curve_label), run_time=1)
        self.play(GrowArrow(arrow), FadeIn(note), run_time=0.8)
        self.wait(2.5)
        self.clear_all(header, axes, x_label, y_label, curve, linear,
                        lin_label, curve_label, note, arrow)

    # ── 2. Probability definition ──

    def play_probability_definition(self):
        header = self.section_header("What Is Probability?")

        defn = MathTex(
            r"p(x)", r"=", r"\lim_{n \to \infty}", r"\frac{n_0}{n}",
            font_size=44,
        )
        defn[0].set_color(TEAL)
        defn[3].set_color(GOLD)
        defn.shift(UP * 0.5)

        legend = VGroup(
            MathTex(r"n", font_size=28, color=SOFTWHITE),
            Text(" = number of trials", font_size=20, color=SOFTWHITE),
        ).arrange(RIGHT, buff=0.15)
        legend2 = VGroup(
            MathTex(r"n_0", font_size=28, color=GOLD),
            Text(" = occurrences of event x", font_size=20, color=SOFTWHITE),
        ).arrange(RIGHT, buff=0.15)
        legend_group = VGroup(legend, legend2).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        legend_group.next_to(defn, DOWN, buff=0.6)

        example = Text(
            "Deal millions of holdem hands → fraction with\n"
            "pocket aces converges on a specific number.",
            font_size=18, color=SLATE, line_spacing=1.3,
        )
        example.next_to(legend_group, DOWN, buff=0.5)

        self.play(Write(defn), run_time=1.5)
        self.play(FadeIn(legend_group), run_time=0.6)
        self.play(FadeIn(example, shift=UP * 0.2), run_time=0.8)
        self.wait(2.5)
        self.clear_all(header, defn, legend_group, example)

    # ── 3. Pocket aces calculation ──

    def play_pocket_aces(self):
        header = self.section_header("Counting: Pocket Aces")

        # Show two cards
        card_a = self.make_card("A", "♠", WHITE)
        card_b = self.make_card("A", "♥", CRIMSON)
        cards = VGroup(card_a, card_b).arrange(RIGHT, buff=0.3)
        cards.shift(UP * 2 + LEFT * 4)

        self.play(*[FadeIn(c, shift=DOWN * 0.3) for c in cards], run_time=0.8)

        # Step-by-step calculation
        steps = VGroup(
            MathTex(r"\text{Event A: first card is an ace}", font_size=26, color=SOFTWHITE),
            MathTex(r"p(A) = \frac{4}{52} = \frac{1}{13}", font_size=30, color=TEAL),
            MathTex(r"\text{Event B: second card is an ace}", font_size=26, color=SOFTWHITE),
            MathTex(r"p(B|A) = \frac{3}{51} = \frac{1}{17}", font_size=30, color=GOLD),
            MathTex(r"\text{These are \textbf{dependent} events!}", font_size=26, color=CRIMSON),
        )
        steps.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        steps.next_to(cards, DOWN, buff=0.5).shift(RIGHT * 2.5)

        for step in steps:
            self.play(FadeIn(step, shift=RIGHT * 0.3), run_time=0.7)
            self.wait(0.5)

        # Final formula
        formula_box = RoundedRectangle(
            width=8, height=1.8, corner_radius=0.15,
            fill_color=NAVY, fill_opacity=0.9,
            stroke_color=GOLD, stroke_width=2,
        ).to_edge(DOWN, buff=0.4)

        formula = MathTex(
            r"p(A \cap B)", r"=", r"p(A)", r"\cdot", r"p(B|A)",
            r"=", r"\frac{1}{13}", r"\cdot", r"\frac{1}{17}",
            r"=", r"\frac{1}{221}",
            font_size=32,
        )
        formula[0].set_color(TEAL)
        formula[2].set_color(TEAL)
        formula[4].set_color(GOLD)
        formula[10].set_color(CRIMSON)
        formula.move_to(formula_box.get_center())

        self.play(FadeIn(formula_box), Write(formula), run_time=1.5)
        self.wait(2.5)
        self.clear_all(header, cards, steps, formula_box, formula)

    # ── 4. Mutually exclusive events ──

    def play_mutually_exclusive(self):
        header = self.section_header("Mutually Exclusive Events")

        # Venn diagram — no overlap
        c1 = Circle(radius=1.2, color=CRIMSON, fill_opacity=0.2, stroke_width=3)
        c1.shift(LEFT * 1.0 + DOWN * 0.2)
        c2 = Circle(radius=1.2, color=TEAL, fill_opacity=0.2, stroke_width=3)
        c2.shift(RIGHT * 1.0 + DOWN * 0.2)
        # Move them far enough apart to not overlap
        c1.shift(LEFT * 0.5)
        c2.shift(RIGHT * 0.5)

        l1 = Text("A♠", font_size=28, color=CRIMSON, weight=BOLD)
        l1.move_to(c1)
        l2 = Text("A♥", font_size=28, color=TEAL, weight=BOLD)
        l2.move_to(c2)
        no_overlap = Text("No overlap!", font_size=18, color=SLATE)
        no_overlap.next_to(VGroup(c1, c2), UP, buff=0.3)

        self.play(Create(c1), Create(c2), FadeIn(l1), FadeIn(l2), run_time=1)
        self.play(FadeIn(no_overlap), run_time=0.5)

        formula = MathTex(
            r"p(A \cup B) = p(A) + p(B)",
            font_size=32, color=SOFTWHITE,
        ).shift(DOWN * 2)

        example = MathTex(
            r"p(\{AA, KK, QQ\})",
            r"= \frac{1}{221} + \frac{1}{221} + \frac{1}{221}",
            r"= \frac{3}{221}",
            font_size=28,
        )
        example[0].set_color(GOLD)
        example[2].set_color(TEAL)
        example.next_to(formula, DOWN, buff=0.4)

        self.play(Write(formula), run_time=1)
        self.play(FadeIn(example), run_time=0.8)
        self.wait(2.5)
        self.clear_all(header, c1, c2, l1, l2, no_overlap, formula, example)

    # ── 5. Independent vs dependent ──

    def play_independent_vs_dependent(self):
        header = self.section_header("Independent vs Dependent Events")

        # Two columns
        ind_title = Text("Independent", font_size=26, color=TEAL, weight=BOLD)
        dep_title = Text("Dependent", font_size=26, color=CRIMSON, weight=BOLD)
        ind_title.shift(LEFT * 3 + UP * 1.5)
        dep_title.shift(RIGHT * 3 + UP * 1.5)

        ind_ex = Text("Two dice rolls", font_size=20, color=SOFTWHITE)
        ind_ex.next_to(ind_title, DOWN, buff=0.3)
        ind_form = MathTex(
            r"p(A \cap B) = p(A) \cdot p(B)",
            font_size=26, color=TEAL,
        )
        ind_form.next_to(ind_ex, DOWN, buff=0.3)
        ind_calc = MathTex(
            r"\frac{1}{6} \cdot \frac{1}{6} = \frac{1}{36}",
            font_size=26, color=SOFTWHITE,
        )
        ind_calc.next_to(ind_form, DOWN, buff=0.3)

        dep_ex = Text("Cards without replacement", font_size=20, color=SOFTWHITE)
        dep_ex.next_to(dep_title, DOWN, buff=0.3)
        dep_form = MathTex(
            r"p(A \cap B) = p(A) \cdot p(B|A)",
            font_size=26, color=CRIMSON,
        )
        dep_form.next_to(dep_ex, DOWN, buff=0.3)
        dep_calc = MathTex(
            r"\frac{4}{52} \cdot \frac{3}{51} = \frac{1}{221}",
            font_size=26, color=SOFTWHITE,
        )
        dep_calc.next_to(dep_form, DOWN, buff=0.3)

        divider = Line(UP * 1.8, DOWN * 1.2, color=SLATE, stroke_width=1)

        self.play(
            FadeIn(ind_title), FadeIn(dep_title), Create(divider),
            run_time=0.8,
        )
        self.play(FadeIn(ind_ex), FadeIn(dep_ex), run_time=0.6)
        self.play(Write(ind_form), Write(dep_form), run_time=1)
        self.play(FadeIn(ind_calc), FadeIn(dep_calc), run_time=0.8)

        key = Text(
            "Key: does knowing A change the probability of B?",
            font_size=20, color=GOLD,
        )
        key.to_edge(DOWN, buff=0.6)
        self.play(FadeIn(key), run_time=0.6)
        self.wait(2.5)
        self.clear_all(header, ind_title, dep_title, ind_ex, dep_ex,
                        ind_form, dep_form, ind_calc, dep_calc, divider, key)

    # ── 6. Inclusion-exclusion ──

    def play_inclusion_exclusion(self):
        header = self.section_header("Inclusion-Exclusion Principle")

        # Overlapping Venn diagram
        c1 = Circle(radius=1.3, color=CRIMSON, fill_opacity=0.15, stroke_width=3)
        c1.shift(LEFT * 0.7 + UP * 0.2)
        c2 = Circle(radius=1.3, color=TEAL, fill_opacity=0.15, stroke_width=3)
        c2.shift(RIGHT * 0.7 + UP * 0.2)

        l1 = Text("Hearts\n13/52", font_size=18, color=CRIMSON)
        l1.move_to(c1.get_center() + LEFT * 0.5)
        l2 = Text("Aces\n4/52", font_size=18, color=TEAL)
        l2.move_to(c2.get_center() + RIGHT * 0.5)
        overlap = Text("A♥\n1/52", font_size=16, color=GOLD, weight=BOLD)
        overlap.move_to((c1.get_center() + c2.get_center()) / 2)

        self.play(Create(c1), Create(c2), run_time=0.8)
        self.play(FadeIn(l1), FadeIn(l2), FadeIn(overlap), run_time=0.8)

        formula = MathTex(
            r"p(A \cup B)", r"=", r"p(A)", r"+", r"p(B)", r"-", r"p(A \cap B)",
            font_size=30,
        )
        formula[0].set_color(SOFTWHITE)
        formula[2].set_color(CRIMSON)
        formula[4].set_color(TEAL)
        formula[6].set_color(GOLD)
        formula.shift(DOWN * 1.8)

        calc = MathTex(
            r"= \frac{13}{52} + \frac{4}{52} - \frac{1}{52} = \frac{16}{52} = \frac{4}{13}",
            font_size=28, color=SOFTWHITE,
        )
        calc.next_to(formula, DOWN, buff=0.3)

        self.play(Write(formula), run_time=1.2)
        self.play(FadeIn(calc), run_time=0.8)
        self.wait(2.5)
        self.clear_all(header, c1, c2, l1, l2, overlap, formula, calc)

    # ── 7. Flopping a flush ──

    def play_flush_probability(self):
        header = self.section_header("Flopping a Flush")

        # Show suited hole cards
        h1 = self.make_card("K", "♥", CRIMSON)
        h2 = self.make_card("9", "♥", CRIMSON)
        hole = VGroup(h1, h2).arrange(RIGHT, buff=0.2)
        hole.shift(UP * 2.2 + LEFT * 4)
        hole_label = Text("Suited hand", font_size=16, color=SOFTWHITE)
        hole_label.next_to(hole, DOWN, buff=0.15)

        self.play(FadeIn(hole), FadeIn(hole_label), run_time=0.8)

        # Chain of conditional probabilities
        steps = VGroup(
            MathTex(r"\text{11 hearts remain in 50 cards}", font_size=22, color=SOFTWHITE),
            MathTex(r"p(\text{1st flop card} \heartsuit) = \frac{11}{50}",
                     font_size=26, color=CRIMSON),
            MathTex(r"p(\text{2nd} \heartsuit \mid \text{1st} \heartsuit) = \frac{10}{49}",
                     font_size=26, color=CRIMSON),
            MathTex(r"p(\text{3rd} \heartsuit \mid \text{1st,2nd} \heartsuit) = \frac{9}{48}",
                     font_size=26, color=CRIMSON),
        )
        steps.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        steps.shift(RIGHT * 1 + UP * 0.8)

        for step in steps:
            self.play(FadeIn(step, shift=RIGHT * 0.2), run_time=0.6)
            self.wait(0.3)

        result_box = RoundedRectangle(
            width=9, height=1.4, corner_radius=0.15,
            fill_color=NAVY, fill_opacity=0.9,
            stroke_color=TEAL, stroke_width=2,
        ).to_edge(DOWN, buff=0.4)

        result = MathTex(
            r"p(\text{flush}) = \frac{11}{50} \cdot \frac{10}{49} \cdot \frac{9}{48}"
            r"= \frac{33}{3920} \approx 0.84\%",
            font_size=28,
        )
        result.set_color(TEAL)
        result.move_to(result_box)

        self.play(FadeIn(result_box), Write(result), run_time=1.2)
        self.wait(2.5)
        self.clear_all(header, hole, hole_label, steps, result_box, result)

    # ── 8. Probability distributions ──

    def play_probability_distributions(self):
        header = self.section_header("Probability Distributions")

        # Coin flip
        coin_title = Text("Coin Flip", font_size=22, color=TEAL, weight=BOLD)
        coin_title.shift(UP * 1.8 + LEFT * 4)
        coin = MathTex(
            r"C = \{(\text{H}, \tfrac{1}{2}),\; (\text{T}, \tfrac{1}{2})\}",
            font_size=26, color=SOFTWHITE,
        )
        coin.next_to(coin_title, DOWN, buff=0.2)

        # Die roll with bar chart
        die_title = Text("Die Roll", font_size=22, color=GOLD, weight=BOLD)
        die_title.shift(UP * 1.8 + RIGHT * 2)

        bars = VGroup()
        bar_labels = VGroup()
        for i in range(6):
            rect = Rectangle(
                width=0.5, height=1.2,
                fill_color=GOLD, fill_opacity=0.7,
                stroke_color=WHITE, stroke_width=1,
            )
            rect.move_to(RIGHT * (i * 0.7 - 0.5) + DOWN * 0.2)
            label = Text(str(i + 1), font_size=16, color=SOFTWHITE)
            label.next_to(rect, DOWN, buff=0.1)
            bars.add(rect)
            bar_labels.add(label)

        die_group = VGroup(bars, bar_labels)
        die_group.next_to(die_title, DOWN, buff=0.3)
        die_eq = MathTex(r"\text{Each face: } \frac{1}{6}", font_size=20, color=SOFTWHITE)
        die_eq.next_to(die_group, DOWN, buff=0.2)

        self.play(FadeIn(coin_title), Write(coin), run_time=0.8)
        self.play(
            FadeIn(die_title),
            *[GrowFromEdge(b, DOWN) for b in bars],
            *[FadeIn(l) for l in bar_labels],
            run_time=1,
        )
        self.play(FadeIn(die_eq), run_time=0.5)

        # Poker application
        poker_note = Text(
            "In poker: a probability distribution represents\n"
            "the range of hands an opponent could hold.",
            font_size=20, color=SLATE, line_spacing=1.3,
        )
        poker_note.to_edge(DOWN, buff=0.6)
        poker_ex = MathTex(
            r"H = \{AA,\; KK,\; QQ,\; AKs,\; AKo\}",
            font_size=26, color=CRIMSON,
        )
        poker_ex.next_to(poker_note, UP, buff=0.3)

        self.play(FadeIn(poker_ex), FadeIn(poker_note), run_time=0.8)
        self.wait(2.5)
        self.clear_all(header, coin_title, coin, die_title, die_group,
                        die_eq, poker_ex, poker_note)

    # ── 9. Expected value intro ──

    def play_expected_value_intro(self):
        header = self.section_header("Expected Value: The Core Concept")

        formula = MathTex(
            r"\langle P \rangle", r"=", r"\sum_{i=1}^{n}", r"p_i", r"\cdot", r"x_i",
            font_size=40,
        )
        formula[0].set_color(TEAL)
        formula[3].set_color(GOLD)
        formula[5].set_color(CRIMSON)
        formula.shift(UP * 1.2)

        legend = VGroup(
            VGroup(MathTex(r"p_i", font_size=24, color=GOLD),
                   Text(" = probability of outcome i", font_size=18, color=SOFTWHITE)
                   ).arrange(RIGHT, buff=0.1),
            VGroup(MathTex(r"x_i", font_size=24, color=CRIMSON),
                   Text(" = value of outcome i", font_size=18, color=SOFTWHITE)
                   ).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        legend.next_to(formula, DOWN, buff=0.5)

        self.play(Write(formula), run_time=1.5)
        self.play(FadeIn(legend), run_time=0.6)
        self.wait(1)

        # Fair coin flip example
        example_title = Text("Fair $10 coin flip:", font_size=22, color=GOLD, weight=BOLD)
        example_title.shift(DOWN * 0.8)
        ev_calc = MathTex(
            r"\langle B \rangle = \frac{1}{2}(+\$10) + \frac{1}{2}(-\$10) = \$0",
            font_size=28, color=SOFTWHITE,
        )
        ev_calc.next_to(example_title, DOWN, buff=0.3)

        verdict = Text("Break even on average.", font_size=20, color=SLATE)
        verdict.next_to(ev_calc, DOWN, buff=0.3)

        self.play(FadeIn(example_title), run_time=0.5)
        self.play(Write(ev_calc), run_time=1.2)
        self.play(FadeIn(verdict), run_time=0.5)
        self.wait(2)
        self.clear_all(header, formula, legend, example_title, ev_calc, verdict)

    # ── 10. Favorable bet ──

    def play_ev_favorable(self):
        header = self.section_header("A Favorable Bet (+EV)")

        desc = Text(
            "Win $11 on heads, lose $10 on tails.",
            font_size=22, color=SOFTWHITE,
        )
        desc.shift(UP * 1.5)

        calc = MathTex(
            r"\langle B_n \rangle",
            r"= \frac{1}{2}(+\$11) + \frac{1}{2}(-\$10)",
            font_size=30,
        )
        calc[0].set_color(TEAL)
        calc.next_to(desc, DOWN, buff=0.5)

        result = MathTex(
            r"\langle B_n \rangle = +\$0.50 \text{ per flip}",
            font_size=32, color=TEAL,
        )
        result.next_to(calc, DOWN, buff=0.4)

        verdict_box = RoundedRectangle(
            width=7, height=1.0, corner_radius=0.12,
            fill_color=NAVY, fill_opacity=0.9,
            stroke_color=TEAL, stroke_width=2,
        )
        verdict_text = Text("Always take this bet!", font_size=24,
                            color=TEAL, weight=BOLD)
        verdict_box.next_to(result, DOWN, buff=0.4)
        verdict_text.move_to(verdict_box)

        self.play(FadeIn(desc), run_time=0.6)
        self.play(Write(calc), run_time=1)
        self.play(Write(result), run_time=0.8)
        self.play(FadeIn(verdict_box), FadeIn(verdict_text), run_time=0.6)
        self.wait(2)
        self.clear_all(header, desc, calc, result, verdict_box, verdict_text)

    # ── 11. Bad bet ──

    def play_ev_bad_bet(self):
        header = self.section_header("A Bad Bet (−EV)")

        desc = Text(
            "Win $30 on double sixes, lose $1 otherwise.",
            font_size=22, color=SOFTWHITE,
        )
        desc.shift(UP * 1.5)

        calc = MathTex(
            r"\langle B_d \rangle",
            r"= \frac{1}{36}(+\$30) + \frac{35}{36}(-\$1)",
            font_size=30,
        )
        calc[0].set_color(CRIMSON)
        calc.next_to(desc, DOWN, buff=0.5)

        result = MathTex(
            r"\langle B_d \rangle = -\$\frac{5}{36} \approx -\$0.14",
            font_size=32, color=CRIMSON,
        )
        result.next_to(calc, DOWN, buff=0.4)

        verdict_box = RoundedRectangle(
            width=8, height=1.0, corner_radius=0.12,
            fill_color=NAVY, fill_opacity=0.9,
            stroke_color=CRIMSON, stroke_width=2,
        )
        verdict_text = Text("Don't take this bet. (This is on every craps table!)",
                            font_size=20, color=CRIMSON, weight=BOLD)
        verdict_box.next_to(result, DOWN, buff=0.4)
        verdict_text.move_to(verdict_box)

        self.play(FadeIn(desc), run_time=0.6)
        self.play(Write(calc), run_time=1)
        self.play(Write(result), run_time=0.8)
        self.play(FadeIn(verdict_box), FadeIn(verdict_text), run_time=0.6)
        self.wait(2)
        self.clear_all(header, desc, calc, result, verdict_box, verdict_text)

    # ── 12. EV is additive ──

    def play_ev_additive(self):
        header = self.section_header("Expected Value Is Additive")

        # Animated bar chart of cumulative EV
        formula = MathTex(
            r"\langle \text{Total} \rangle = \sum_{i=1}^{n} \langle \text{Bet}_i \rangle",
            font_size=36, color=SOFTWHITE,
        )
        formula.shift(UP * 1.5)
        self.play(Write(formula), run_time=1)

        # Show sequence of bets accumulating
        bets = [+0.50, +0.50, +0.50, -0.14, +0.50, +0.50]
        labels_text = ["+$0.50", "+$0.50", "+$0.50", "−$0.14", "+$0.50", "+$0.50"]
        cumulative = []
        running = 0
        for b in bets:
            running += b
            cumulative.append(running)

        bar_group = VGroup()
        cum_labels = VGroup()
        bet_labels = VGroup()
        max_h = 3.0
        max_val = max(cumulative)

        for i, (c, bl) in enumerate(zip(cumulative, labels_text)):
            h = max(c / max_val * max_h, 0.05)
            color = TEAL if bets[i] > 0 else CRIMSON
            rect = Rectangle(
                width=0.8, height=h,
                fill_color=color, fill_opacity=0.75,
                stroke_color=WHITE, stroke_width=1,
            )
            x_pos = (i - 2.5) * 1.1
            rect.move_to(np.array([x_pos, -1.8 + h / 2, 0]))

            bl_mob = Text(bl, font_size=14, color=color)
            bl_mob.next_to(rect, DOWN, buff=0.1)

            cl = Text(f"${c:.2f}", font_size=14, color=WHITE, weight=BOLD)
            cl.next_to(rect, UP, buff=0.08)

            bar_group.add(rect)
            bet_labels.add(bl_mob)
            cum_labels.add(cl)

        for i in range(len(bets)):
            self.play(
                GrowFromEdge(bar_group[i], DOWN),
                FadeIn(bet_labels[i]),
                FadeIn(cum_labels[i]),
                run_time=0.5,
            )

        note = Text(
            "Casinos profit from millions of −EV bets.\n"
            "Poker players profit from consistent +EV decisions.",
            font_size=18, color=GOLD, line_spacing=1.3,
        )
        note.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(note), run_time=0.6)
        self.wait(2.5)
        self.clear_all(header, formula, bar_group, bet_labels, cum_labels, note)

    # ── 13. Key takeaways ──

    def play_key_takeaways(self):
        lines = VGroup(
            Text("Key Concepts — Chapter 1", font_size=36,
                 color=GOLD, weight=BOLD),
            Text("", font_size=10),
            Text("1.  Probability = long-run frequency of an event",
                 font_size=22, color=SOFTWHITE),
            Text("2.  Distributions pair all outcomes with probabilities",
                 font_size=22, color=SOFTWHITE),
            Text("3.  EV = sum of (probability × value) for each outcome",
                 font_size=22, color=SOFTWHITE),
            Text("4.  Expected value is additive across decisions",
                 font_size=22, color=SOFTWHITE),
            Text("5.  A math player's goal: maximize total EV",
                 font_size=22, color=SOFTWHITE),
            Text("", font_size=14),
            Text("This is the foundation for everything that follows.",
                 font_size=26, color=CRIMSON, weight=BOLD),
        )
        lines.arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        lines[0].move_to(lines[0].get_center())  # keep title centered
        lines[0].set_x(0)
        lines[-1].set_x(0)
        lines.move_to(ORIGIN)

        for line in lines:
            self.play(FadeIn(line, shift=UP * 0.15), run_time=0.5)

        self.wait(3)
        self.play(FadeOut(lines), run_time=1)
