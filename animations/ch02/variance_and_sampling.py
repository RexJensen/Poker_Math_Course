"""
Chapter 2 — Predicting the Future: Variance and Sample Outcomes
===============================================================

Manim animation covering all key concepts from Chapter 2 of
"The Mathematics of Poker" by Bill Chen & Jerrod Ankenman.

Topics covered:
  1. Variance — measuring dispersion from expected value
  2. Standard deviation — σ = √V, same units as EV
  3. Variance examples: coin flip (V=1) vs die roll (V=5)
  4. Variance is additive across trials; σ grows with √N
  5. The Normal Distribution — bell curve, Central Limit Theorem
  6. Z-scores: z = (x - μ) / σ
  7. Die game D2 example: EV=1/6, V≈6.806, 81.7% chance ahead after 200 trials
  8. Poker session example: 0.015 BB/hand, σ=2, wins only 55.17%
  9. Sample size table — 95% interval narrows relative to mean
 10. AK vs AQ impossibility (z = -23.8)
 11. Key takeaways

See script.md for the full narration script with timestamps.

RENDER
------
    pip install manim
    # Low quality preview:
    manim -pql animations/ch02/variance_and_sampling.py VarianceAndSampling
    # High quality render:
    manim -qh animations/ch02/variance_and_sampling.py VarianceAndSampling
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


class VarianceAndSampling(Scene):
    """Full Chapter 2 animation — Variance & Sample Outcomes."""

    def construct(self):
        self.camera.background_color = DARKBG
        self.play_title()
        self.play_variance_definition()
        self.play_variance_examples()
        self.play_standard_deviation()
        self.play_variance_additivity()
        self.play_normal_distribution()
        self.play_z_scores()
        self.play_die_game_example()
        self.play_poker_session()
        self.play_sample_size_table()
        self.play_ak_vs_aq()
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
        title = Text("Variance & Sample Outcomes", font_size=48,
                      color=WHITE, weight=BOLD)
        subtitle = Text("The Mathematics of Poker — Chapter 2",
                        font_size=24, color=SOFTWHITE)
        subtitle.next_to(title, DOWN, buff=0.4)

        suits = Text("♠ ♥ ♦ ♣", font_size=36, color=CRIMSON)
        suits.next_to(subtitle, DOWN, buff=0.6)

        quote = Text(
            '"Understanding the variance of a game is\n'
            'just as important as understanding the expectation."',
            font_size=18, color=SLATE, slant=ITALIC,
        )
        quote.next_to(suits, DOWN, buff=0.6)

        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle, shift=UP * 0.3), run_time=0.8)
        self.play(FadeIn(suits), run_time=0.5)
        self.play(FadeIn(quote, shift=UP * 0.2), run_time=0.8)
        self.wait(2)
        self.clear_all(title, subtitle, suits, quote)

    # ── 1. Variance definition ──

    def play_variance_definition(self):
        header = self.section_header("What Is Variance?")

        intro = Text(
            "EV tells us the average outcome.\n"
            "Variance tells us how spread out the outcomes are.",
            font_size=20, color=SOFTWHITE, line_spacing=1.3,
        )
        intro.shift(UP * 1.5)
        self.play(FadeIn(intro, shift=UP * 0.2), run_time=0.8)
        self.wait(1)

        formula = MathTex(
            r"V", r"=", r"\sum_{i=1}^{n}",
            r"p_i", r"\cdot",
            r"\left(", r"x_i", r"-", r"\langle P \rangle", r"\right)^2",
            font_size=40,
        )
        formula[0].set_color(TEAL)
        formula[3].set_color(GOLD)
        formula[6].set_color(CRIMSON)
        formula[8].set_color(CRIMSON)
        formula.shift(DOWN * 0.2)

        legend = VGroup(
            VGroup(MathTex(r"p_i", font_size=24, color=GOLD),
                   Text(" = probability of outcome i", font_size=18,
                        color=SOFTWHITE)).arrange(RIGHT, buff=0.1),
            VGroup(MathTex(r"x_i", font_size=24, color=CRIMSON),
                   Text(" = value of outcome i", font_size=18,
                        color=SOFTWHITE)).arrange(RIGHT, buff=0.1),
            VGroup(MathTex(r"\langle P \rangle", font_size=24, color=CRIMSON),
                   Text(" = expected value (mean)", font_size=18,
                        color=SOFTWHITE)).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        legend.next_to(formula, DOWN, buff=0.5)

        note = Text(
            "We square the distances so negatives don't cancel positives.",
            font_size=18, color=SLATE,
        )
        note.next_to(legend, DOWN, buff=0.4)

        self.play(Write(formula), run_time=1.5)
        self.play(FadeIn(legend), run_time=0.6)
        self.play(FadeIn(note, shift=UP * 0.15), run_time=0.6)
        self.wait(2)
        self.clear_all(header, intro, formula, legend, note)

    # ── 2. Variance examples ──

    def play_variance_examples(self):
        header = self.section_header("Variance Examples: Coin vs Die")

        # --- Coin flip (left side) ---
        coin_title = Text("Coin Flip", font_size=24, color=TEAL, weight=BOLD)
        coin_title.shift(UP * 1.8 + LEFT * 3.5)

        coin_dist = MathTex(
            r"\text{H} \to +1,\quad \text{T} \to -1",
            font_size=22, color=SOFTWHITE,
        )
        coin_dist.next_to(coin_title, DOWN, buff=0.25)

        coin_ev = MathTex(
            r"\langle P \rangle = 0",
            font_size=22, color=SOFTWHITE,
        )
        coin_ev.next_to(coin_dist, DOWN, buff=0.2)

        coin_calc = MathTex(
            r"V = \tfrac{1}{2}(1-0)^2 + \tfrac{1}{2}(-1-0)^2",
            font_size=22, color=SOFTWHITE,
        )
        coin_calc.next_to(coin_ev, DOWN, buff=0.2)

        coin_result = MathTex(
            r"V = 1",
            font_size=28, color=TEAL,
        )
        coin_result.next_to(coin_calc, DOWN, buff=0.25)

        coin_group = VGroup(coin_title, coin_dist, coin_ev, coin_calc, coin_result)

        # --- Die roll (right side) ---
        die_title = Text("Die Roll", font_size=24, color=GOLD, weight=BOLD)
        die_title.shift(UP * 1.8 + RIGHT * 3)

        die_dist = MathTex(
            r"\text{Each face } 1\text{-}6,\; p = \tfrac{1}{6}",
            font_size=22, color=SOFTWHITE,
        )
        die_dist.next_to(die_title, DOWN, buff=0.25)

        die_ev = MathTex(
            r"\langle P \rangle = 3.5",
            font_size=22, color=SOFTWHITE,
        )
        die_ev.next_to(die_dist, DOWN, buff=0.2)

        die_calc = MathTex(
            r"V = \tfrac{1}{6}\sum_{i=1}^{6}(i - 3.5)^2",
            font_size=22, color=SOFTWHITE,
        )
        die_calc.next_to(die_ev, DOWN, buff=0.2)

        die_result = MathTex(
            r"V \approx 2.917",
            font_size=28, color=GOLD,
        )
        die_result.next_to(die_calc, DOWN, buff=0.25)

        die_group = VGroup(die_title, die_dist, die_ev, die_calc, die_result)

        # Divider
        divider = Line(UP * 2.0, DOWN * 1.5, color=SLATE, stroke_width=1)

        # Comparison note
        note = Text(
            "Higher variance = more unpredictable outcomes.",
            font_size=20, color=SLATE,
        )
        note.to_edge(DOWN, buff=0.6)

        self.play(
            FadeIn(coin_title), FadeIn(die_title), Create(divider),
            run_time=0.8,
        )
        self.play(FadeIn(coin_dist), FadeIn(die_dist), run_time=0.6)
        self.play(FadeIn(coin_ev), FadeIn(die_ev), run_time=0.6)
        self.play(Write(coin_calc), Write(die_calc), run_time=1)
        self.play(Write(coin_result), Write(die_result), run_time=0.8)
        self.play(FadeIn(note), run_time=0.6)
        self.wait(2)
        self.clear_all(header, coin_group, die_group, divider, note)

    # ── 3. Standard deviation ──

    def play_standard_deviation(self):
        header = self.section_header("Standard Deviation")

        formula = MathTex(
            r"\sigma", r"=", r"\sqrt{V}",
            font_size=44,
        )
        formula[0].set_color(TEAL)
        formula[2].set_color(TEAL)
        formula.shift(UP * 1.0)

        self.play(Write(formula), run_time=1.2)

        why = Text(
            "Why not just use variance?",
            font_size=22, color=GOLD, weight=BOLD,
        )
        why.next_to(formula, DOWN, buff=0.6)
        self.play(FadeIn(why), run_time=0.5)

        reason = Text(
            "Variance is in squared units (dollars squared).\n"
            "Standard deviation is in the same units as EV (dollars).\n"
            "This makes comparison intuitive.",
            font_size=20, color=SOFTWHITE, line_spacing=1.3,
        )
        reason.next_to(why, DOWN, buff=0.4)
        self.play(FadeIn(reason, shift=UP * 0.2), run_time=0.8)

        examples = VGroup(
            MathTex(r"\text{Coin: } V = 1 \implies \sigma = 1",
                    font_size=24, color=TEAL),
            MathTex(r"\text{Die: } V \approx 2.917 \implies \sigma \approx 1.71",
                    font_size=24, color=GOLD),
        ).arrange(DOWN, buff=0.2)
        examples.next_to(reason, DOWN, buff=0.5)

        self.play(FadeIn(examples), run_time=0.8)
        self.wait(2)
        self.clear_all(header, formula, why, reason, examples)

    # ── 4. Variance additivity ──

    def play_variance_additivity(self):
        header = self.section_header("Variance Is Additive")

        var_formula = MathTex(
            r"V_N", r"=", r"N", r"\cdot", r"V",
            font_size=40,
        )
        var_formula[0].set_color(TEAL)
        var_formula[2].set_color(GOLD)
        var_formula[4].set_color(TEAL)
        var_formula.shift(UP * 1.5)

        self.play(Write(var_formula), run_time=1)

        sd_formula = MathTex(
            r"\sigma_N", r"=", r"\sigma", r"\sqrt{N}",
            font_size=40,
        )
        sd_formula[0].set_color(CRIMSON)
        sd_formula[2].set_color(TEAL)
        sd_formula[3].set_color(GOLD)
        sd_formula.next_to(var_formula, DOWN, buff=0.5)

        self.play(Write(sd_formula), run_time=1)

        # Key insight box
        insight_box = RoundedRectangle(
            width=10, height=1.6, corner_radius=0.15,
            fill_color=NAVY, fill_opacity=0.9,
            stroke_color=GOLD, stroke_width=2,
        ).shift(DOWN * 1.0)

        insight = VGroup(
            Text("Key insight:", font_size=20, color=GOLD, weight=BOLD),
            Text(
                "EV grows linearly with N trials,\n"
                "but standard deviation only grows with the square root of N.",
                font_size=18, color=SOFTWHITE, line_spacing=1.3,
            ),
        ).arrange(DOWN, buff=0.15)
        insight.move_to(insight_box)

        self.play(FadeIn(insight_box), FadeIn(insight), run_time=0.8)

        bottom_note = Text(
            "This is why the long run matters in poker.",
            font_size=20, color=SLATE,
        )
        bottom_note.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(bottom_note), run_time=0.6)
        self.wait(2.5)
        self.clear_all(header, var_formula, sd_formula,
                        insight_box, insight, bottom_note)

    # ── 5. Normal distribution ──

    def play_normal_distribution(self):
        header = self.section_header("The Normal Distribution (Bell Curve)")

        axes = Axes(
            x_range=[-4, 4, 1], y_range=[0, 0.45, 0.1],
            x_length=10, y_length=4,
            axis_config={"color": SOFTWHITE, "font_size": 18,
                         "include_ticks": False},
            tips=False,
        ).shift(DOWN * 0.3)

        # Bell curve
        bell = axes.plot(
            lambda x: (1 / np.sqrt(2 * np.pi)) * np.exp(-x**2 / 2),
            x_range=[-3.8, 3.8],
            color=TEAL, stroke_width=3,
        )

        self.play(Create(axes), run_time=0.8)
        self.play(Create(bell), run_time=1.2)

        # Mark mean
        mu_line = axes.get_vertical_line(
            axes.c2p(0, 0.399), color=GOLD, stroke_width=2,
        )
        mu_label = MathTex(r"\mu", font_size=28, color=GOLD)
        mu_label.next_to(axes.c2p(0, 0), DOWN, buff=0.2)
        self.play(Create(mu_line), FadeIn(mu_label), run_time=0.6)

        # Shade 1σ region (68%)
        area_1s = axes.get_area(bell, x_range=[-1, 1],
                                 color=TEAL, opacity=0.3)
        label_1s = Text("68%", font_size=20, color=TEAL, weight=BOLD)
        label_1s.move_to(axes.c2p(0, 0.15))
        s1_left = MathTex(r"-1\sigma", font_size=18, color=TEAL)
        s1_left.next_to(axes.c2p(-1, 0), DOWN, buff=0.2)
        s1_right = MathTex(r"+1\sigma", font_size=18, color=TEAL)
        s1_right.next_to(axes.c2p(1, 0), DOWN, buff=0.2)

        self.play(FadeIn(area_1s), FadeIn(label_1s),
                  FadeIn(s1_left), FadeIn(s1_right), run_time=0.8)
        self.wait(0.5)

        # Shade 2σ region (95.5%)
        area_2s = axes.get_area(bell, x_range=[-2, 2],
                                 color=GOLD, opacity=0.15)
        label_2s = Text("95.5%", font_size=18, color=GOLD, weight=BOLD)
        label_2s.move_to(axes.c2p(0, 0.06))
        s2_left = MathTex(r"-2\sigma", font_size=18, color=GOLD)
        s2_left.next_to(axes.c2p(-2, 0), DOWN, buff=0.2)
        s2_right = MathTex(r"+2\sigma", font_size=18, color=GOLD)
        s2_right.next_to(axes.c2p(2, 0), DOWN, buff=0.2)

        self.play(FadeIn(area_2s), FadeIn(label_2s),
                  FadeIn(s2_left), FadeIn(s2_right), run_time=0.8)
        self.wait(0.5)

        # Mark 3σ (99.7%)
        s3_left = MathTex(r"-3\sigma", font_size=18, color=CRIMSON)
        s3_left.next_to(axes.c2p(-3, 0), DOWN, buff=0.2)
        s3_right = MathTex(r"+3\sigma", font_size=18, color=CRIMSON)
        s3_right.next_to(axes.c2p(3, 0), DOWN, buff=0.2)
        label_3s = Text("99.7%", font_size=16, color=CRIMSON, weight=BOLD)
        label_3s.move_to(axes.c2p(0, -0.03))

        self.play(FadeIn(s3_left), FadeIn(s3_right),
                  FadeIn(label_3s), run_time=0.8)

        clt = Text(
            "Central Limit Theorem: the sum of many independent\n"
            "random variables tends toward a normal distribution.",
            font_size=16, color=SLATE, line_spacing=1.3,
        )
        clt.to_edge(DOWN, buff=0.2)
        self.play(FadeIn(clt), run_time=0.6)
        self.wait(2.5)
        self.clear_all(header, axes, bell, mu_line, mu_label,
                        area_1s, label_1s, s1_left, s1_right,
                        area_2s, label_2s, s2_left, s2_right,
                        s3_left, s3_right, label_3s, clt)

    # ── 6. Z-scores ──

    def play_z_scores(self):
        header = self.section_header("Z-Scores: Standardizing Results")

        formula = MathTex(
            r"z", r"=", r"\frac{x - \mu}{\sigma}",
            font_size=44,
        )
        formula[0].set_color(TEAL)
        formula[2].set_color(SOFTWHITE)
        formula.shift(UP * 1.2)

        self.play(Write(formula), run_time=1.2)

        legend = VGroup(
            VGroup(MathTex(r"x", font_size=24, color=SOFTWHITE),
                   Text(" = observed result", font_size=18,
                        color=SOFTWHITE)).arrange(RIGHT, buff=0.1),
            VGroup(MathTex(r"\mu", font_size=24, color=GOLD),
                   Text(" = expected value (mean)", font_size=18,
                        color=SOFTWHITE)).arrange(RIGHT, buff=0.1),
            VGroup(MathTex(r"\sigma", font_size=24, color=TEAL),
                   Text(" = standard deviation", font_size=18,
                        color=SOFTWHITE)).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        legend.next_to(formula, DOWN, buff=0.5)
        self.play(FadeIn(legend), run_time=0.6)

        interpretation = VGroup(
            Text("|z| < 1     → result is typical", font_size=20, color=TEAL),
            Text("|z| = 2     → result is unusual (5% territory)",
                 font_size=20, color=GOLD),
            Text("|z| > 3     → result is very rare (< 0.3%)",
                 font_size=20, color=CRIMSON),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        interpretation.next_to(legend, DOWN, buff=0.5)

        for line in interpretation:
            self.play(FadeIn(line, shift=RIGHT * 0.2), run_time=0.5)

        self.wait(2)
        self.clear_all(header, formula, legend, interpretation)

    # ── 7. Die game D2 ──

    def play_die_game_example(self):
        header = self.section_header("Applied Example: Die Game D2")

        # Game description
        desc = Text(
            "Win $6 on a 6, lose $1 on 1-5.",
            font_size=22, color=SOFTWHITE,
        )
        desc.shift(UP * 2.0)
        self.play(FadeIn(desc), run_time=0.6)

        # EV calculation
        ev_calc = MathTex(
            r"\langle P \rangle = \tfrac{1}{6}(+6) + \tfrac{5}{6}(-1)"
            r"= 1 - \tfrac{5}{6} = \tfrac{1}{6}",
            font_size=26, color=SOFTWHITE,
        )
        ev_calc.next_to(desc, DOWN, buff=0.4)
        self.play(Write(ev_calc), run_time=1)

        # Variance calculation
        var_calc = MathTex(
            r"V = \tfrac{1}{6}\!\left(6 - \tfrac{1}{6}\right)^2"
            r"+ \tfrac{5}{6}\!\left(-1 - \tfrac{1}{6}\right)^2"
            r"\approx 6.806",
            font_size=24, color=SOFTWHITE,
        )
        var_calc.next_to(ev_calc, DOWN, buff=0.3)
        self.play(Write(var_calc), run_time=1.2)

        sd_val = MathTex(
            r"\sigma = \sqrt{6.806} \approx 2.609",
            font_size=24, color=TEAL,
        )
        sd_val.next_to(var_calc, DOWN, buff=0.3)
        self.play(Write(sd_val), run_time=0.8)

        # After 200 trials
        trials_box = RoundedRectangle(
            width=10, height=2.2, corner_radius=0.15,
            fill_color=NAVY, fill_opacity=0.9,
            stroke_color=TEAL, stroke_width=2,
        ).to_edge(DOWN, buff=0.3)

        trials_text = VGroup(
            Text("After 200 trials:", font_size=22, color=GOLD, weight=BOLD),
            MathTex(r"\mu_{200} = 200 \times \tfrac{1}{6} \approx 33.3",
                    font_size=22, color=SOFTWHITE),
            MathTex(r"\sigma_{200} = 2.609 \times \sqrt{200} \approx 36.9",
                    font_size=22, color=SOFTWHITE),
            MathTex(r"z(0) = \tfrac{0 - 33.3}{36.9} \approx -0.90"
                    r"\;\Rightarrow\; 81.7\%\text{ chance of being ahead}",
                    font_size=22, color=TEAL),
        ).arrange(DOWN, buff=0.15)
        trials_text.move_to(trials_box)

        self.play(FadeIn(trials_box), run_time=0.5)
        for line in trials_text:
            self.play(FadeIn(line), run_time=0.6)

        self.wait(2.5)
        self.clear_all(header, desc, ev_calc, var_calc, sd_val,
                        trials_box, trials_text)

    # ── 8. Poker session ──

    def play_poker_session(self):
        header = self.section_header("Poker Reality Check")

        # Player stats
        stats = VGroup(
            Text("A solid winning player:", font_size=24,
                 color=GOLD, weight=BOLD),
            MathTex(r"\text{Win rate} = 0.015 \text{ BB/hand}",
                    font_size=24, color=SOFTWHITE),
            MathTex(r"\sigma = 2 \text{ BB/hand}",
                    font_size=24, color=SOFTWHITE),
            MathTex(r"\text{Session} = 300 \text{ hands}",
                    font_size=24, color=SOFTWHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        stats.shift(UP * 1.5 + LEFT * 2)

        for line in stats:
            self.play(FadeIn(line, shift=RIGHT * 0.2), run_time=0.5)

        # Calculation
        calc_group = VGroup(
            MathTex(r"\mu_{300} = 300 \times 0.015 = 4.5 \text{ BB}",
                    font_size=24, color=TEAL),
            MathTex(r"\sigma_{300} = 2 \times \sqrt{300} \approx 34.64 \text{ BB}",
                    font_size=24, color=TEAL),
            MathTex(r"z(0) = \frac{0 - 4.5}{34.64} \approx -0.13",
                    font_size=24, color=SOFTWHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        calc_group.next_to(stats, DOWN, buff=0.5)

        self.play(Write(calc_group[0]), run_time=0.8)
        self.play(Write(calc_group[1]), run_time=0.8)
        self.play(Write(calc_group[2]), run_time=0.8)

        # Result box
        result_box = RoundedRectangle(
            width=10, height=1.2, corner_radius=0.15,
            fill_color=NAVY, fill_opacity=0.9,
            stroke_color=CRIMSON, stroke_width=2,
        ).to_edge(DOWN, buff=0.4)

        result = Text(
            "This player wins only 55.17% of 300-hand sessions!",
            font_size=22, color=CRIMSON, weight=BOLD,
        )
        result.move_to(result_box)

        self.play(FadeIn(result_box), FadeIn(result), run_time=0.8)
        self.wait(2.5)
        self.clear_all(header, stats, calc_group, result_box, result)

    # ── 9. Sample size table ──

    def play_sample_size_table(self):
        header = self.section_header("The Long Run: Sample Size Matters")

        # Table header
        col_headers = VGroup(
            Text("Hands", font_size=20, color=GOLD, weight=BOLD),
            Text("EV (BB)", font_size=20, color=GOLD, weight=BOLD),
            Text("95% Range (BB)", font_size=20, color=GOLD, weight=BOLD),
            Text("Range / EV", font_size=20, color=GOLD, weight=BOLD),
        ).arrange(RIGHT, buff=0.8)
        col_headers.shift(UP * 2.0)

        # Data rows — win rate 0.015 BB/hand, σ = 2 BB/hand
        # 95% range = ±1.96σ√N
        data = [
            ("300",    "4.5",    "±67.9",   "15.1x"),
            ("1,000",  "15",     "±124.0",  "8.3x"),
            ("10,000", "150",    "±392.0",  "2.6x"),
            ("100,000", "1,500", "±1,240",  "0.8x"),
            ("1,000,000", "15,000", "±3,920", "0.3x"),
        ]

        rows = VGroup()
        for i, (hands, ev, rng, ratio) in enumerate(data):
            color = SOFTWHITE if i < 3 else TEAL
            row = VGroup(
                Text(hands, font_size=18, color=color),
                Text(ev, font_size=18, color=color),
                Text(rng, font_size=18, color=color),
                Text(ratio, font_size=18, color=color),
            ).arrange(RIGHT, buff=0.8)
            rows.add(row)

        # Align columns with headers
        rows.arrange(DOWN, buff=0.25)
        rows.next_to(col_headers, DOWN, buff=0.35)

        # Align each column
        for row in rows:
            for j, item in enumerate(row):
                item.set_x(col_headers[j].get_x())

        self.play(FadeIn(col_headers), run_time=0.6)
        for row in rows:
            self.play(FadeIn(row, shift=RIGHT * 0.2), run_time=0.5)

        arrow_note = Text(
            "The noise shrinks relative to the signal as sample grows.",
            font_size=18, color=SLATE,
        )
        arrow_note.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(arrow_note), run_time=0.6)
        self.wait(2.5)
        self.clear_all(header, col_headers, rows, arrow_note)

    # ── 10. AK vs AQ ──

    def play_ak_vs_aq(self):
        header = self.section_header("The AK vs AQ Story")

        # Setup
        cards_ak = VGroup(
            self.make_card("A", "♠", WHITE),
            self.make_card("K", "♠", WHITE),
        ).arrange(RIGHT, buff=0.15)

        vs_text = Text("vs", font_size=28, color=SOFTWHITE, weight=BOLD)

        cards_aq = VGroup(
            self.make_card("A", "♥", CRIMSON),
            self.make_card("Q", "♥", CRIMSON),
        ).arrange(RIGHT, buff=0.15)

        matchup = VGroup(cards_ak, vs_text, cards_aq).arrange(RIGHT, buff=0.4)
        matchup.shift(UP * 2.0)

        self.play(FadeIn(matchup), run_time=0.8)

        # Claim
        claim = Text(
            'Player claims: "AK vs AQ is basically 50-50\n'
            'over my last 2,000 hands."',
            font_size=20, color=SOFTWHITE, line_spacing=1.3,
        )
        claim.next_to(matchup, DOWN, buff=0.5)
        self.play(FadeIn(claim), run_time=0.8)

        # Truth: AK wins ~70%
        truth = VGroup(
            Text("Reality: AK wins ~70% vs AQ", font_size=22,
                 color=GOLD, weight=BOLD),
            MathTex(r"\text{Over 2000 hands: } \mu = 1400, \;"
                    r"\sigma \approx 25.8",
                    font_size=22, color=SOFTWHITE),
        ).arrange(DOWN, buff=0.2)
        truth.next_to(claim, DOWN, buff=0.4)
        self.play(FadeIn(truth), run_time=0.8)

        # Z-score
        z_calc_box = RoundedRectangle(
            width=10, height=1.6, corner_radius=0.15,
            fill_color=NAVY, fill_opacity=0.9,
            stroke_color=CRIMSON, stroke_width=2,
        ).to_edge(DOWN, buff=0.35)

        z_calc = VGroup(
            MathTex(
                r"z = \frac{1000 - 1400}{25.8}"
                r"\ \approx\ {-15.5}",
                font_size=26, color=SOFTWHITE,
            ),
            Text("This is essentially impossible. The claim is false.",
                 font_size=20, color=CRIMSON, weight=BOLD),
        ).arrange(DOWN, buff=0.15)
        z_calc.move_to(z_calc_box)

        self.play(FadeIn(z_calc_box), Write(z_calc[0]), run_time=1)
        self.play(FadeIn(z_calc[1]), run_time=0.6)
        self.wait(2.5)
        self.clear_all(header, matchup, claim, truth, z_calc_box, z_calc)

    # ── 11. Key takeaways ──

    def play_key_takeaways(self):
        lines = VGroup(
            Text("Key Concepts — Chapter 2", font_size=36,
                 color=GOLD, weight=BOLD),
            Text("", font_size=10),
            Text("1.  Variance measures how spread out results are around EV",
                 font_size=22, color=SOFTWHITE),
            Text("2.  Standard deviation = square root of variance (same units as EV)",
                 font_size=22, color=SOFTWHITE),
            Text("3.  Over N trials: EV scales with N, but SD only scales with sqrt(N)",
                 font_size=22, color=SOFTWHITE),
            Text("4.  A winning player can easily lose in the short run",
                 font_size=22, color=SOFTWHITE),
            Text("5.  Z-scores let us test whether observed results are plausible",
                 font_size=22, color=SOFTWHITE),
            Text("", font_size=14),
            Text("Variance is the enemy of the short run,",
                 font_size=26, color=CRIMSON, weight=BOLD),
            Text("but the friend of the skilled long-run player.",
                 font_size=26, color=TEAL, weight=BOLD),
        )
        lines.arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        lines[0].set_x(0)
        lines[-1].set_x(0)
        lines[-2].set_x(0)
        lines.move_to(ORIGIN)

        for line in lines:
            self.play(FadeIn(line, shift=UP * 0.15), run_time=0.5)

        self.wait(3)
        self.play(FadeOut(lines), run_time=1)
