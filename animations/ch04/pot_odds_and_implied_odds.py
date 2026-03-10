"""
Chapter 4 — Playing the Odds: Pot Odds and Implied Odds
========================================================

Manim animation covering all key concepts from Chapter 4 of
"The Mathematics of Poker" by Bill Chen & Jerrod Ankenman.

Topics covered:
  1. Exploitive play — maximize EV against opponent's strategy
  2. Pot odds — the ratio between pot size and cost to call
  3. Made hand vs draw example (AA vs flush draw)
  4. Pot odds formula and break-even equity
  5. Multi-street pot odds considerations
  6. Implied odds — future money from completed draws
  7. Bluffing — pure bluffs, semi-bluffs, and value bets
  8. Bluff math — indifference thresholds (Example 4.8)
  9. Key takeaways

See script.md for the full narration script with timestamps.

RENDER
------
    pip install manim
    # Low quality preview:
    manim -pql animations/ch04/pot_odds_and_implied_odds.py PotOddsAndImpliedOdds
    # High quality render:
    manim -qh animations/ch04/pot_odds_and_implied_odds.py PotOddsAndImpliedOdds
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


class PotOddsAndImpliedOdds(Scene):
    """Full Chapter 4 animation — Pot Odds & Implied Odds."""

    def construct(self):
        self.camera.background_color = DARKBG
        self.play_title()
        self.play_exploitive_intro()
        self.play_pot_odds_concept()
        self.play_made_vs_draw()
        self.play_pot_odds_formula()
        self.play_multi_street_odds()
        self.play_implied_odds()
        self.play_bluffing_intro()
        self.play_bluff_math()
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

    # ── 1. Title ──

    def play_title(self):
        title = Text("Pot Odds & Implied Odds", font_size=48,
                      color=WHITE, weight=BOLD)
        subtitle = Text("The Mathematics of Poker — Chapter 4",
                        font_size=24, color=SOFTWHITE)
        subtitle.next_to(title, DOWN, buff=0.4)

        suits = Text("♠ ♥ ♦ ♣", font_size=36, color=CRIMSON)
        suits.next_to(subtitle, DOWN, buff=0.6)

        quote = Text(
            '"Exploitive play means maximizing your own\n'
            'expected value given your opponent\'s strategy."',
            font_size=18, color=SLATE, slant=ITALIC,
        )
        quote.next_to(suits, DOWN, buff=0.6)

        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle, shift=UP * 0.3), run_time=0.8)
        self.play(FadeIn(suits), run_time=0.5)
        self.play(FadeIn(quote, shift=UP * 0.2), run_time=0.8)
        self.wait(2)
        self.clear_all(title, subtitle, suits, quote)

    # ── 2. Exploitive play intro ──

    def play_exploitive_intro(self):
        header = self.section_header("Exploitive Play")

        # Show decision tree: player faces choice, picks highest EV
        desc = Text(
            "At every decision point, choose the action\n"
            "with the highest expected value.",
            font_size=22, color=SOFTWHITE, line_spacing=1.3,
        )
        desc.shift(UP * 1.0)
        self.play(FadeIn(desc, shift=UP * 0.2), run_time=0.8)

        # Three action boxes
        actions = VGroup()
        ev_values = [("+$12.50", TEAL), ("+$3.00", SLATE), ("-$8.00", CRIMSON)]
        action_names = ["Call", "Fold", "Raise"]
        for i, (ev, color) in enumerate(ev_values):
            box = RoundedRectangle(
                width=2.8, height=1.6, corner_radius=0.1,
                fill_color=NAVY, fill_opacity=0.9,
                stroke_color=color, stroke_width=2,
            )
            name = Text(action_names[i], font_size=22, color=SOFTWHITE, weight=BOLD)
            ev_text = Text(f"EV = {ev}", font_size=20, color=color, weight=BOLD)
            name.move_to(box.get_center() + UP * 0.25)
            ev_text.move_to(box.get_center() + DOWN * 0.25)
            actions.add(VGroup(box, name, ev_text))

        actions.arrange(RIGHT, buff=0.5)
        actions.shift(DOWN * 1.0)

        for action in actions:
            self.play(FadeIn(action, shift=UP * 0.2), run_time=0.6)

        # Highlight the best action
        highlight = RoundedRectangle(
            width=3.0, height=1.8, corner_radius=0.12,
            stroke_color=TEAL, stroke_width=4,
            fill_opacity=0,
        )
        highlight.move_to(actions[0])
        best_label = Text("Best action!", font_size=18, color=TEAL, weight=BOLD)
        best_label.next_to(highlight, DOWN, buff=0.2)

        self.play(Create(highlight), FadeIn(best_label), run_time=0.8)
        self.wait(2)
        self.clear_all(header, desc, actions, highlight, best_label)

    # ── 3. Pot odds concept ──

    def play_pot_odds_concept(self):
        header = self.section_header("Pot Odds")

        # Visual pot with chips
        pot_box = RoundedRectangle(
            width=3.0, height=1.8, corner_radius=0.15,
            fill_color=CHARCOAL, fill_opacity=0.8,
            stroke_color=GOLD, stroke_width=2,
        )
        pot_box.shift(UP * 0.8 + LEFT * 2.5)
        pot_label = Text("POT", font_size=20, color=GOLD, weight=BOLD)
        pot_label.move_to(pot_box.get_center() + UP * 0.35)
        pot_amount = Text("$100", font_size=32, color=WHITE, weight=BOLD)
        pot_amount.move_to(pot_box.get_center() + DOWN * 0.15)

        # Cost to call
        call_box = RoundedRectangle(
            width=2.4, height=1.4, corner_radius=0.12,
            fill_color=CHARCOAL, fill_opacity=0.8,
            stroke_color=CRIMSON, stroke_width=2,
        )
        call_box.shift(UP * 0.8 + RIGHT * 2.5)
        call_label = Text("Cost to Call", font_size=18, color=CRIMSON, weight=BOLD)
        call_label.move_to(call_box.get_center() + UP * 0.25)
        call_amount = Text("$20", font_size=28, color=WHITE, weight=BOLD)
        call_amount.move_to(call_box.get_center() + DOWN * 0.15)

        self.play(
            FadeIn(pot_box), FadeIn(pot_label), FadeIn(pot_amount),
            FadeIn(call_box), FadeIn(call_label), FadeIn(call_amount),
            run_time=1.0,
        )

        # Arrow showing the ratio
        arrow = Arrow(
            call_box.get_bottom() + DOWN * 0.2,
            pot_box.get_bottom() + DOWN * 0.2,
            color=SLATE, stroke_width=2, buff=0.2,
        )
        ratio_text = Text("Pot odds = 5:1", font_size=22, color=GOLD, weight=BOLD)
        ratio_text.next_to(VGroup(pot_box, call_box), DOWN, buff=0.8)

        self.play(GrowArrow(arrow), FadeIn(ratio_text), run_time=0.8)

        # The rule
        rule_box = RoundedRectangle(
            width=10, height=1.4, corner_radius=0.12,
            fill_color=NAVY, fill_opacity=0.9,
            stroke_color=TEAL, stroke_width=2,
        )
        rule_box.to_edge(DOWN, buff=0.4)
        rule = MathTex(
            r"\text{Call if } P(\text{win})",
            r">",
            r"\frac{\text{Cost}}{\text{Pot} + \text{Cost}}",
            r"= \frac{20}{120} = 16.7\%",
            font_size=28,
        )
        rule[0].set_color(TEAL)
        rule[2].set_color(GOLD)
        rule[3].set_color(SOFTWHITE)
        rule.move_to(rule_box)

        self.play(FadeIn(rule_box), Write(rule), run_time=1.2)
        self.wait(2.5)
        self.clear_all(header, pot_box, pot_label, pot_amount,
                        call_box, call_label, call_amount,
                        arrow, ratio_text, rule_box, rule)

    # ── 4. Made hand vs draw (Example 4.2) ──

    def play_made_vs_draw(self):
        header = self.section_header("Example: AA vs Flush Draw")

        # Board cards
        board_label = Text("Board:", font_size=20, color=SLATE)
        board_label.shift(UP * 2.2 + LEFT * 5)
        board_cards = VGroup(
            self.make_card("K", "♥", CRIMSON),
            self.make_card("7", "♣", CHARCOAL),
            self.make_card("3", "♠", CHARCOAL),
            self.make_card("2", "♥", CRIMSON),
        ).arrange(RIGHT, buff=0.15)
        board_cards.next_to(board_label, RIGHT, buff=0.3)

        # Player A hand
        a_label = Text("Player A:", font_size=18, color=TEAL)
        a_label.shift(UP * 0.7 + LEFT * 5)
        a_cards = VGroup(
            self.make_card("A", "♦", CRIMSON),
            self.make_card("A", "♣", CHARCOAL),
        ).arrange(RIGHT, buff=0.1)
        a_cards.next_to(a_label, RIGHT, buff=0.2)
        a_desc = Text("(overpair)", font_size=16, color=SLATE)
        a_desc.next_to(a_cards, RIGHT, buff=0.2)

        # Player B hand
        b_label = Text("Player B:", font_size=18, color=CRIMSON)
        b_label.shift(DOWN * 0.2 + LEFT * 5)
        b_cards = VGroup(
            self.make_card("9", "♥", CRIMSON),
            self.make_card("8", "♥", CRIMSON),
        ).arrange(RIGHT, buff=0.1)
        b_cards.next_to(b_label, RIGHT, buff=0.2)
        b_desc = Text("(flush draw)", font_size=16, color=SLATE)
        b_desc.next_to(b_cards, RIGHT, buff=0.2)

        self.play(
            FadeIn(board_label), *[FadeIn(c, shift=DOWN * 0.2) for c in board_cards],
            run_time=0.8,
        )
        self.play(
            FadeIn(a_label), FadeIn(a_cards), FadeIn(a_desc),
            FadeIn(b_label), FadeIn(b_cards), FadeIn(b_desc),
            run_time=0.8,
        )

        # Game info
        info = VGroup(
            Text("Pot: $400  |  Bet: $60  |  Limit $30-60", font_size=20, color=GOLD),
            Text("B has 9 hearts out of 44 unknown cards", font_size=18, color=SOFTWHITE),
        ).arrange(DOWN, buff=0.15)
        info.shift(DOWN * 1.1)
        self.play(FadeIn(info), run_time=0.6)

        # EV calculation
        ev_box = RoundedRectangle(
            width=10, height=1.8, corner_radius=0.15,
            fill_color=NAVY, fill_opacity=0.9,
            stroke_color=TEAL, stroke_width=2,
        )
        ev_box.to_edge(DOWN, buff=0.3)

        ev_calc = MathTex(
            r"\text{EV}_{\text{call}}",
            r"= \frac{9}{44}",
            r"\times \$520",
            r"- \frac{35}{44}",
            r"\times \$60",
            font_size=26,
        )
        ev_calc[0].set_color(TEAL)
        ev_calc[1].set_color(GOLD)
        ev_calc[3].set_color(CRIMSON)

        ev_result = MathTex(
            r"= \$106.36 - \$47.73 = +\$46.36",
            font_size=26, color=TEAL,
        )
        ev_group = VGroup(ev_calc, ev_result).arrange(DOWN, buff=0.15)
        ev_group.move_to(ev_box)

        self.play(FadeIn(ev_box), Write(ev_calc), run_time=1.2)
        self.play(Write(ev_result), run_time=0.8)

        verdict = Text("Calling is +EV!", font_size=20, color=TEAL, weight=BOLD)
        verdict.next_to(ev_box, UP, buff=0.15).shift(RIGHT * 3.5)
        self.play(FadeIn(verdict), run_time=0.5)
        self.wait(2.5)
        self.clear_all(header, board_label, board_cards,
                        a_label, a_cards, a_desc,
                        b_label, b_cards, b_desc,
                        info, ev_box, ev_group, verdict)

    # ── 5. Pot odds formula ──

    def play_pot_odds_formula(self):
        header = self.section_header("The Pot Odds Formula")

        # Main formula
        formula = MathTex(
            r"\text{Call if: }",
            r"\text{Equity}",
            r">",
            r"\frac{\text{Bet}}{\text{Pot} + \text{Bet}}",
            font_size=36,
        )
        formula[1].set_color(TEAL)
        formula[3].set_color(GOLD)
        formula.shift(UP * 1.0)

        self.play(Write(formula), run_time=1.5)

        # Break-even equity examples table
        table_title = Text("Break-Even Equity by Pot Odds",
                           font_size=22, color=SLATE, weight=BOLD)
        table_title.next_to(formula, DOWN, buff=0.6)
        self.play(FadeIn(table_title), run_time=0.5)

        # Show several examples as rows
        examples = [
            ("2:1", "33.3%"),
            ("3:1", "25.0%"),
            ("4:1", "20.0%"),
            ("5:1", "16.7%"),
            ("9:1", "10.0%"),
        ]
        rows = VGroup()
        for odds, equity in examples:
            odds_text = Text(f"Pot odds {odds}", font_size=20, color=GOLD)
            arrow = Text("  -->  ", font_size=20, color=SLATE)
            eq_text = Text(f"Need {equity} equity", font_size=20, color=TEAL)
            row = VGroup(odds_text, arrow, eq_text).arrange(RIGHT, buff=0.15)
            rows.add(row)

        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        rows.next_to(table_title, DOWN, buff=0.3)

        for row in rows:
            self.play(FadeIn(row, shift=RIGHT * 0.2), run_time=0.4)

        note = Text(
            "Better pot odds = you need less equity to call profitably.",
            font_size=18, color=CRIMSON,
        )
        note.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note), run_time=0.6)
        self.wait(2.5)
        self.clear_all(header, formula, table_title, rows, note)

    # ── 6. Multi-street pot odds ──

    def play_multi_street_odds(self):
        header = self.section_header("Pot Odds Across Multiple Streets")

        # Setup
        setup = VGroup(
            Text("Pot: $135  |  Bet: $30  |  9 outs on the flop",
                 font_size=20, color=SOFTWHITE),
        )
        setup.shift(UP * 1.8)
        self.play(FadeIn(setup), run_time=0.6)

        # Flop calculation
        flop_box = RoundedRectangle(
            width=5.5, height=2.2, corner_radius=0.12,
            fill_color=NAVY, fill_opacity=0.9,
            stroke_color=TEAL, stroke_width=2,
        )
        flop_box.shift(LEFT * 3 + DOWN * 0.3)
        flop_title = Text("Flop Decision", font_size=20, color=TEAL, weight=BOLD)
        flop_title.move_to(flop_box.get_center() + UP * 0.7)
        flop_calc = VGroup(
            MathTex(r"\text{Need: } \frac{30}{165} = 18.2\%", font_size=22, color=GOLD),
            MathTex(r"\text{Have: } \frac{9}{47} = 19.1\%", font_size=22, color=TEAL),
            Text("Has odds to call!", font_size=18, color=TEAL, weight=BOLD),
        ).arrange(DOWN, buff=0.15)
        flop_calc.move_to(flop_box.get_center() + DOWN * 0.15)

        # Turn calculation
        turn_box = RoundedRectangle(
            width=5.5, height=2.2, corner_radius=0.12,
            fill_color=NAVY, fill_opacity=0.9,
            stroke_color=CRIMSON, stroke_width=2,
        )
        turn_box.shift(RIGHT * 3 + DOWN * 0.3)
        turn_title = Text("Turn Decision", font_size=20, color=CRIMSON, weight=BOLD)
        turn_title.move_to(turn_box.get_center() + UP * 0.7)
        turn_calc = VGroup(
            MathTex(r"\text{Need: } \frac{60}{255} = 23.5\%", font_size=22, color=GOLD),
            MathTex(r"\text{Have: } \frac{9}{46} = 19.6\%", font_size=22, color=CRIMSON),
            Text("No longer has odds!", font_size=18, color=CRIMSON, weight=BOLD),
        ).arrange(DOWN, buff=0.15)
        turn_calc.move_to(turn_box.get_center() + DOWN * 0.15)

        self.play(FadeIn(flop_box), FadeIn(flop_title), run_time=0.6)
        for item in flop_calc:
            self.play(FadeIn(item), run_time=0.5)

        self.play(FadeIn(turn_box), FadeIn(turn_title), run_time=0.6)
        for item in turn_calc:
            self.play(FadeIn(item), run_time=0.5)

        # Warning
        warning = Text(
            "Having odds on the flop does NOT mean you have odds on the turn.",
            font_size=18, color=GOLD,
        )
        warning.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(warning), run_time=0.6)
        self.wait(2.5)
        self.clear_all(header, setup, flop_box, flop_title, flop_calc,
                        turn_box, turn_title, turn_calc, warning)

    # ── 7. Implied odds ──

    def play_implied_odds(self):
        header = self.section_header("Implied Odds")

        # Concept explanation
        desc = Text(
            "Implied odds account for money you expect to win\n"
            "on future streets when your draw completes.",
            font_size=22, color=SOFTWHITE, line_spacing=1.3,
        )
        desc.shift(UP * 1.5)
        self.play(FadeIn(desc, shift=UP * 0.2), run_time=0.8)

        # Before vs after
        # Current pot
        current_box = RoundedRectangle(
            width=3.5, height=2.0, corner_radius=0.12,
            fill_color=NAVY, fill_opacity=0.9,
            stroke_color=SLATE, stroke_width=2,
        )
        current_box.shift(LEFT * 3.5 + DOWN * 0.5)
        current_title = Text("Current Pot", font_size=18, color=SLATE, weight=BOLD)
        current_title.move_to(current_box.get_center() + UP * 0.55)
        current_amt = Text("$135", font_size=28, color=WHITE, weight=BOLD)
        current_amt.move_to(current_box.get_center())
        current_note = Text("Not enough odds", font_size=16, color=CRIMSON)
        current_note.move_to(current_box.get_center() + DOWN * 0.5)

        # Arrow
        plus_arrow = Text("  +  ", font_size=36, color=GOLD, weight=BOLD)
        plus_arrow.move_to(DOWN * 0.5)

        # Future bets
        future_box = RoundedRectangle(
            width=3.5, height=2.0, corner_radius=0.12,
            fill_color=NAVY, fill_opacity=0.9,
            stroke_color=GOLD, stroke_width=2,
        )
        future_box.shift(RIGHT * 3.5 + DOWN * 0.5)
        future_title = Text("Future Bets", font_size=18, color=GOLD, weight=BOLD)
        future_title.move_to(future_box.get_center() + UP * 0.55)
        future_amt = Text("$180+", font_size=28, color=GOLD, weight=BOLD)
        future_amt.move_to(future_box.get_center())
        future_note = Text("When draw hits", font_size=16, color=SLATE)
        future_note.move_to(future_box.get_center() + DOWN * 0.5)

        self.play(
            FadeIn(current_box), FadeIn(current_title),
            FadeIn(current_amt), FadeIn(current_note),
            run_time=0.8,
        )
        self.play(FadeIn(plus_arrow), run_time=0.4)
        self.play(
            FadeIn(future_box), FadeIn(future_title),
            FadeIn(future_amt), FadeIn(future_note),
            run_time=0.8,
        )

        # Effective pot
        eff_box = RoundedRectangle(
            width=10, height=1.4, corner_radius=0.12,
            fill_color=NAVY, fill_opacity=0.9,
            stroke_color=TEAL, stroke_width=2,
        )
        eff_box.to_edge(DOWN, buff=0.3)
        eff_text = MathTex(
            r"\text{Effective Pot} = \$135 + \$180 = \$315",
            r"\quad \Rightarrow \quad",
            r"\text{Now the call is +EV!}",
            font_size=26,
        )
        eff_text[0].set_color(GOLD)
        eff_text[2].set_color(TEAL)
        eff_text.move_to(eff_box)

        self.play(FadeIn(eff_box), Write(eff_text), run_time=1.2)
        self.wait(2.5)
        self.clear_all(header, desc, current_box, current_title, current_amt,
                        current_note, plus_arrow, future_box, future_title,
                        future_amt, future_note, eff_box, eff_text)

    # ── 8. Bluffing intro ──

    def play_bluffing_intro(self):
        header = self.section_header("Types of Bets")

        # Three categories as a spectrum
        categories = VGroup()
        data = [
            ("Pure Bluff", "No chance of winning\nif called", CRIMSON),
            ("Semi-Bluff", "Can improve to best\nhand if called", GOLD),
            ("Value Bet", "Already the best hand;\nwant a call", TEAL),
        ]

        for name, desc, color in data:
            box = RoundedRectangle(
                width=3.5, height=2.8, corner_radius=0.12,
                fill_color=NAVY, fill_opacity=0.9,
                stroke_color=color, stroke_width=2,
            )
            title = Text(name, font_size=22, color=color, weight=BOLD)
            title.move_to(box.get_center() + UP * 0.7)
            description = Text(desc, font_size=16, color=SOFTWHITE, line_spacing=1.2)
            description.move_to(box.get_center() + DOWN * 0.2)
            categories.add(VGroup(box, title, description))

        categories.arrange(RIGHT, buff=0.4)
        categories.shift(DOWN * 0.2)

        # Spectrum line
        spectrum_line = Line(LEFT * 5, RIGHT * 5, color=SLATE, stroke_width=2)
        spectrum_line.shift(DOWN * 2.5)
        left_label = Text("Bluff", font_size=16, color=CRIMSON)
        left_label.next_to(spectrum_line, LEFT, buff=0.1).shift(DOWN * 0.3)
        right_label = Text("Value", font_size=16, color=TEAL)
        right_label.next_to(spectrum_line, RIGHT, buff=0.1).shift(DOWN * 0.3)

        self.play(Create(spectrum_line), FadeIn(left_label), FadeIn(right_label),
                  run_time=0.6)

        for cat in categories:
            self.play(FadeIn(cat, shift=UP * 0.2), run_time=0.7)

        self.wait(2.5)
        self.clear_all(header, categories, spectrum_line, left_label, right_label)

    # ── 9. Bluff math (Example 4.8) ──

    def play_bluff_math(self):
        header = self.section_header("Bluff Math: Indifference")

        # Setup
        setup = VGroup(
            Text("Stud game  |  Pot: $655  |  A bets: $80", font_size=20, color=SOFTWHITE),
            Text("B missed flush draw — should B bluff?", font_size=20, color=GOLD),
        ).arrange(DOWN, buff=0.15)
        setup.shift(UP * 1.6)
        self.play(FadeIn(setup), run_time=0.8)

        # B's bluff EV
        b_title = Text("B's Bluff EV:", font_size=20, color=CRIMSON, weight=BOLD)
        b_title.shift(UP * 0.5 + LEFT * 3)
        b_eq = MathTex(
            r"\text{EV} = P(\text{A folds}) \times \$655",
            r"- P(\text{A calls}) \times \$80",
            font_size=22, color=SOFTWHITE,
        )
        b_eq.next_to(b_title, DOWN, buff=0.2)

        b_result = MathTex(
            r"\text{Bluff is +EV if A folds} > \frac{80}{735} = 10.9\%",
            font_size=22, color=CRIMSON,
        )
        b_result.next_to(b_eq, DOWN, buff=0.2)

        self.play(FadeIn(b_title), Write(b_eq), run_time=1.0)
        self.play(FadeIn(b_result), run_time=0.6)

        # A's calling threshold
        a_title = Text("A's Call Threshold:", font_size=20, color=TEAL, weight=BOLD)
        a_title.shift(DOWN * 1.0 + LEFT * 3)
        a_eq = MathTex(
            r"\text{A should call if } P(\text{B bluffs})",
            r"> \frac{80}{735+80} = 2.2\%",
            font_size=22,
        )
        a_eq[0].set_color(SOFTWHITE)
        a_eq[1].set_color(TEAL)
        a_eq.next_to(a_title, DOWN, buff=0.2)

        self.play(FadeIn(a_title), Write(a_eq), run_time=1.0)

        # Summary box
        summary_box = RoundedRectangle(
            width=10, height=1.6, corner_radius=0.12,
            fill_color=NAVY, fill_opacity=0.9,
            stroke_color=GOLD, stroke_width=2,
        )
        summary_box.to_edge(DOWN, buff=0.3)
        summary = VGroup(
            Text("B bluffs > 2.2% of the time --> A must call to prevent exploitation",
                 font_size=16, color=TEAL),
            Text("A calls < 89.1% of the time --> B should bluff all missed draws",
                 font_size=16, color=CRIMSON),
        ).arrange(DOWN, buff=0.15)
        summary.move_to(summary_box)

        self.play(FadeIn(summary_box), FadeIn(summary), run_time=0.8)
        self.wait(2.5)
        self.clear_all(header, setup, b_title, b_eq, b_result,
                        a_title, a_eq, summary_box, summary)

    # ── 10. Key takeaways ──

    def play_key_takeaways(self):
        lines = VGroup(
            Text("Key Concepts — Chapter 4", font_size=36,
                 color=GOLD, weight=BOLD),
            Text("", font_size=10),
            Text("1.  Pot odds: compare cost-to-call vs potential pot won",
                 font_size=22, color=SOFTWHITE),
            Text("2.  Call if equity > bet / (pot + bet)",
                 font_size=22, color=SOFTWHITE),
            Text("3.  Flop odds do not guarantee turn odds — re-evaluate each street",
                 font_size=22, color=SOFTWHITE),
            Text("4.  Implied odds: factor in future bets when your draw completes",
                 font_size=22, color=SOFTWHITE),
            Text("5.  Bluffs exploit opponents who fold too often; calls exploit bluffers",
                 font_size=22, color=SOFTWHITE),
            Text("", font_size=14),
            Text("Know your odds. Every street. Every decision.",
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
