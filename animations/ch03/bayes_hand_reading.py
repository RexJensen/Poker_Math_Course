"""
Bayes' Theorem for Poker Hand Reading — Manim Animation
========================================================

Concept: Chapter 3 of "The Mathematics of Poker" (Chen & Ankenman)

This animation shows how a poker player uses Bayesian updating to narrow
down an opponent's likely holdings as new information (actions) arrive.

NARRATION SCRIPT
================

[0:00 - Title]
"One of the most powerful ideas in The Mathematics of Poker is that
hand reading isn't guesswork — it's Bayesian inference."

[0:08 - Prior Distribution]
"Before any action, your opponent could hold any hand. But hands aren't
equally likely to be played the same way. Let's group holdings into
five categories and assign prior probabilities based on how often
each type appears in a typical opening range."

[0:22 - Bayes' Formula]
"Bayes' theorem tells us how to update these probabilities when
new evidence arrives. The posterior probability of each hand category
equals its prior probability times the likelihood of the observed
action given that category, divided by the total probability of
seeing that action."

[0:38 - Preflop Raise]
"Our opponent raises from under-the-gun — the earliest and tightest
position. Premium hands raise almost always. Strong hands raise
most of the time. But speculative and weak hands rarely raise
from this position. Watch how the distribution shifts."

[0:55 - Post-Update 1]
"The distribution has changed dramatically. Premium and strong hands
now dominate. Weak hands have nearly vanished. This is the
mathematical foundation of hand reading — each action is evidence
that reshapes the probability landscape."

[1:08 - Flop Continuation Bet]
"The flop comes King-Seven-Two rainbow — a dry, uncoordinated board.
Our opponent bets two-thirds of the pot. Premium hands with a king
or an overpair almost always bet here. But hands that missed this
flop are much less likely to continue."

[1:22 - Post-Update 2]
"After two rounds of Bayesian updating, the picture is clear.
Our opponent almost certainly has a premium hand — a big pair
or ace-king. The math has done the hand reading for us."

[1:35 - Conclusion]
"This is the core message of Chapter 3: every action your opponent
takes is data. Bayes' theorem is the machine that converts that data
into knowledge. The players who learn to think this way have a
profound edge over those who rely on gut feeling alone."

RENDER INSTRUCTIONS
===================
    pip install manim
    # Low quality preview:
    manim -pql animations/bayes_hand_reading.py BayesHandReading
    # High quality render:
    manim -qh animations/bayes_hand_reading.py BayesHandReading
"""

from manim import *
import numpy as np

# ── Color palette (poker-themed) ──
CRIMSON   = "#c9362c"
GOLD      = "#d4a017"
TEAL      = "#2eaf7d"
SLATE     = "#5a7d9a"
CHARCOAL  = "#3a3a3a"
DARKBG    = "#1a1a2e"
SOFTWHITE = "#e0e0e0"


class BayesHandReading(Scene):
    """Bayesian hand reading in poker — animated with Manim."""

    def construct(self):
        self.camera.background_color = DARKBG

        self.play_title()
        self.play_prior()
        self.play_bayes_formula()
        self.play_update_preflop()
        self.play_flop()
        self.play_update_flop()
        self.play_conclusion()

    # ─────────────────── helpers ───────────────────

    def make_bars(self, values, title_text, highlight_idx=None):
        """Build a bar chart with category labels and percentage labels."""
        categories = ["Premium", "Strong", "Medium", "Speculative", "Weak"]
        colors = [CRIMSON, GOLD, TEAL, SLATE, CHARCOAL]

        bars = VGroup()
        labels = VGroup()
        pct_labels = VGroup()

        bar_width = 0.9
        max_height = 4.0
        spacing = 1.4

        for i, (val, cat, col) in enumerate(zip(values, categories, colors)):
            h = max(val / 100 * max_height, 0.04)
            rect = Rectangle(
                width=bar_width, height=h,
                fill_color=col, fill_opacity=0.85,
                stroke_color=WHITE, stroke_width=1,
            )
            x_pos = (i - 2) * spacing
            rect.move_to(np.array([x_pos, -2.0 + h / 2, 0]))

            label = Text(cat, font_size=18, color=SOFTWHITE)
            label.next_to(rect, DOWN, buff=0.15)

            pct = Text(f"{val:.0f}%", font_size=20, color=WHITE, weight=BOLD)
            pct.next_to(rect, UP, buff=0.1)

            if highlight_idx is not None and i == highlight_idx:
                rect.set_stroke(GOLD, width=3)
                pct.set_color(GOLD)

            bars.add(rect)
            labels.add(label)
            pct_labels.add(pct)

        title = Text(title_text, font_size=28, color=SOFTWHITE, weight=BOLD)
        title.to_edge(UP, buff=0.5)

        group = VGroup(title, bars, labels, pct_labels)
        return group, bars, labels, pct_labels, title

    def animate_bar_transition(self, old_bars, old_pcts, new_values, new_title_text,
                                old_title, old_labels):
        """Morph existing bars to new heights and update percentages."""
        categories = ["Premium", "Strong", "Medium", "Speculative", "Weak"]
        colors = [CRIMSON, GOLD, TEAL, SLATE, CHARCOAL]

        bar_width = 0.9
        max_height = 4.0
        spacing = 1.4

        new_bars = VGroup()
        new_pcts = VGroup()

        for i, (val, col) in enumerate(zip(new_values, colors)):
            h = max(val / 100 * max_height, 0.04)
            rect = Rectangle(
                width=bar_width, height=h,
                fill_color=col, fill_opacity=0.85,
                stroke_color=WHITE, stroke_width=1,
            )
            x_pos = (i - 2) * spacing
            rect.move_to(np.array([x_pos, -2.0 + h / 2, 0]))

            pct = Text(f"{val:.1f}%", font_size=20, color=WHITE, weight=BOLD)
            pct.next_to(rect, UP, buff=0.1)

            new_bars.add(rect)
            new_pcts.add(pct)

        new_title = Text(new_title_text, font_size=28, color=SOFTWHITE, weight=BOLD)
        new_title.to_edge(UP, buff=0.5)

        self.play(
            *[Transform(old_bars[i], new_bars[i]) for i in range(5)],
            *[Transform(old_pcts[i], new_pcts[i]) for i in range(5)],
            Transform(old_title, new_title),
            run_time=2.0,
        )

        return old_bars, old_pcts, old_title

    # ─────────────────── scenes ───────────────────

    def play_title(self):
        title = Text("Bayesian Hand Reading", font_size=48, color=WHITE, weight=BOLD)
        subtitle = Text("The Mathematics of Poker — Chapter 3",
                        font_size=24, color=SOFTWHITE)
        subtitle.next_to(title, DOWN, buff=0.4)

        suits = Text("♠ ♥ ♦ ♣", font_size=36, color=CRIMSON)
        suits.next_to(subtitle, DOWN, buff=0.6)

        quote = Text(
            '"Every action is data.\nBayes\' theorem converts it into knowledge."',
            font_size=20, color=SLATE, slant=ITALIC,
        )
        quote.next_to(suits, DOWN, buff=0.6)

        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle, shift=UP * 0.3), run_time=0.8)
        self.play(FadeIn(suits), run_time=0.5)
        self.play(FadeIn(quote, shift=UP * 0.2), run_time=0.8)
        self.wait(2)
        self.play(FadeOut(VGroup(title, subtitle, suits, quote)), run_time=0.8)

    def play_prior(self):
        """Show the prior distribution of opponent hand categories."""
        # Prior probabilities (rough % of all starting hands)
        # Premium: AA, KK, QQ, AKs ≈ 2.6%
        # Strong: JJ, TT, AQs, AKo, AQo ≈ 4.8%
        # Medium: 99-77, KQs, suited connectors ≈ 10.5%
        # Speculative: small pairs, suited aces, suited connectors ≈ 18%
        # Weak: everything else ≈ 64%
        prior = [2.6, 4.8, 10.5, 18.0, 64.1]

        header = Text("Step 1: The Prior Distribution", font_size=32,
                       color=GOLD, weight=BOLD)
        header.to_edge(UP, buff=0.3)
        self.play(Write(header), run_time=0.8)

        desc = Text(
            "Before any action, how often does each hand category appear?",
            font_size=20, color=SOFTWHITE,
        )
        desc.next_to(header, DOWN, buff=0.25)
        self.play(FadeIn(desc), run_time=0.5)

        group, bars, labels, pcts, title = self.make_bars(prior, "Prior: All Starting Hands")
        title.next_to(desc, DOWN, buff=0.4)

        self.play(
            *[GrowFromEdge(b, DOWN) for b in bars],
            *[FadeIn(l) for l in labels],
            FadeIn(title),
            run_time=1.5,
        )
        self.play(*[FadeIn(p) for p in pcts], run_time=0.5)
        self.wait(2)

        # Store for later transition
        self.prior_bars = bars
        self.prior_pcts = pcts
        self.prior_title = title
        self.prior_labels = labels
        self.prior_header = header
        self.prior_desc = desc

    def play_bayes_formula(self):
        """Show Bayes' theorem formula."""
        formula_box = RoundedRectangle(
            width=11, height=2.5, corner_radius=0.2,
            fill_color="#0d1b2a", fill_opacity=0.9,
            stroke_color=GOLD, stroke_width=2,
        )
        formula_box.to_edge(DOWN, buff=0.3)

        formula = MathTex(
            r"P(\text{Hand} \mid \text{Action})",
            r"=",
            r"\frac{P(\text{Action} \mid \text{Hand}) \cdot P(\text{Hand})}{P(\text{Action})}",
            font_size=36,
        )
        formula[0].set_color(TEAL)
        formula[2][0:19].set_color(GOLD)   # likelihood
        formula[2][20:30].set_color(CRIMSON)  # prior
        formula.move_to(formula_box.get_center() + UP * 0.3)

        legend = VGroup(
            Text("Posterior", font_size=16, color=TEAL),
            Text("  =  Likelihood", font_size=16, color=GOLD),
            Text(" × Prior", font_size=16, color=CRIMSON),
            Text(" / Evidence", font_size=16, color=SOFTWHITE),
        ).arrange(RIGHT, buff=0.1)
        legend.next_to(formula, DOWN, buff=0.3)

        self.play(FadeIn(formula_box), run_time=0.5)
        self.play(Write(formula), run_time=2)
        self.play(FadeIn(legend), run_time=0.5)
        self.wait(2.5)

        self.play(FadeOut(VGroup(formula_box, formula, legend)), run_time=0.8)

    def play_update_preflop(self):
        """Villain raises UTG — update the distribution."""
        # Action announcement
        action = Text("ACTION: Villain raises from Under-the-Gun",
                       font_size=26, color=CRIMSON, weight=BOLD)
        action_box = SurroundingRectangle(action, color=CRIMSON, buff=0.2,
                                          corner_radius=0.1)
        action_group = VGroup(action_box, action)
        action_group.to_edge(DOWN, buff=0.5)

        self.play(FadeIn(action_group, shift=UP * 0.3), run_time=0.8)
        self.wait(1.5)

        # Likelihood of raising UTG for each category
        # Premium: ~95%, Strong: ~70%, Medium: ~25%, Speculative: ~8%, Weak: ~2%
        likelihood = [0.95, 0.70, 0.25, 0.08, 0.02]
        prior = [2.6, 4.8, 10.5, 18.0, 64.1]

        # Show likelihood values
        like_text = VGroup()
        cats = ["Premium", "Strong", "Medium", "Speculative", "Weak"]
        like_vals = ["95%", "70%", "25%", "8%", "2%"]
        for cat, lv in zip(cats, like_vals):
            t = Text(f"{cat}: {lv}", font_size=16, color=GOLD)
            like_text.add(t)
        like_text.arrange(RIGHT, buff=0.5)
        like_header = Text("P(Raise UTG | Hand):", font_size=18, color=GOLD,
                           weight=BOLD)
        like_group = VGroup(like_header, like_text).arrange(DOWN, buff=0.15)
        like_group.next_to(action_group, UP, buff=0.3)

        self.play(FadeIn(like_group), run_time=0.8)
        self.wait(1.5)

        # Compute posterior via Bayes
        unnormalized = [p * l for p, l in zip(prior, likelihood)]
        total = sum(unnormalized)
        posterior = [u / total * 100 for u in unnormalized]

        # Animate the transition
        self.animate_bar_transition(
            self.prior_bars, self.prior_pcts, posterior,
            "Posterior: After UTG Raise",
            self.prior_title, self.prior_labels,
        )
        self.wait(2)

        # Clean up overlays
        self.play(FadeOut(action_group), FadeOut(like_group), run_time=0.6)

        # Store for next update
        self.post1_values = posterior

    def play_flop(self):
        """Show the flop: K♠ 7♥ 2♦"""
        flop_label = Text("THE FLOP", font_size=24, color=SOFTWHITE, weight=BOLD)
        flop_label.to_edge(DOWN, buff=1.8)

        cards_data = [("K", "♠", WHITE), ("7", "♥", CRIMSON), ("2", "♦", CRIMSON)]
        card_mobjects = VGroup()

        for rank, suit, suit_color in cards_data:
            card_bg = RoundedRectangle(
                width=1.0, height=1.45, corner_radius=0.08,
                fill_color="#f5f5f0", fill_opacity=1.0,
                stroke_color="#333", stroke_width=2,
            )
            rank_text = Text(rank, font_size=32, color="#111", weight=BOLD)
            suit_text = Text(suit, font_size=28, color=suit_color)
            rank_text.move_to(card_bg.get_center() + UP * 0.2)
            suit_text.move_to(card_bg.get_center() + DOWN * 0.25)
            card = VGroup(card_bg, rank_text, suit_text)
            card_mobjects.add(card)

        card_mobjects.arrange(RIGHT, buff=0.25)
        card_mobjects.next_to(flop_label, DOWN, buff=0.3)

        board_text = Text("K♠ 7♥ 2♦ rainbow — dry board", font_size=18,
                          color=SLATE)
        board_text.next_to(card_mobjects, DOWN, buff=0.2)

        self.play(
            Write(flop_label),
            *[FadeIn(c, shift=DOWN * 0.5) for c in card_mobjects],
            run_time=1.2,
        )
        self.play(FadeIn(board_text), run_time=0.5)
        self.wait(1.5)

        self.flop_group = VGroup(flop_label, card_mobjects, board_text)

    def play_update_flop(self):
        """Villain c-bets 2/3 pot on K-7-2 rainbow."""
        action = Text("ACTION: Villain bets 2/3 pot",
                       font_size=24, color=CRIMSON, weight=BOLD)
        action_box = SurroundingRectangle(action, color=CRIMSON, buff=0.2,
                                          corner_radius=0.1)
        action_group = VGroup(action_box, action)
        action_group.next_to(self.flop_group, UP, buff=0.2)

        self.play(FadeIn(action_group, shift=UP * 0.2), run_time=0.6)
        self.wait(1)

        # Likelihood of c-betting 2/3 pot on K-7-2r
        # Premium (KK, AA, AK hit): ~90%
        # Strong (QQ, JJ — overpairs): ~75%
        # Medium (missed draws, 99-77): ~30%
        # Speculative (total air): ~15%
        # Weak (missed): ~5%
        likelihood2 = [0.90, 0.75, 0.30, 0.15, 0.05]

        unnormalized = [p * l for p, l in zip(self.post1_values, likelihood2)]
        total = sum(unnormalized)
        posterior2 = [u / total * 100 for u in unnormalized]

        self.animate_bar_transition(
            self.prior_bars, self.prior_pcts, posterior2,
            "Posterior: After UTG Raise + Flop C-bet",
            self.prior_title, self.prior_labels,
        )
        self.wait(2)

        # Show the final read
        read_box = RoundedRectangle(
            width=9, height=1.2, corner_radius=0.15,
            fill_color="#0d1b2a", fill_opacity=0.9,
            stroke_color=TEAL, stroke_width=2,
        )
        read_box.to_edge(DOWN, buff=0.3)

        read_text = Text(
            f"Villain likely holds: Premium ({posterior2[0]:.0f}%) "
            f"or Strong ({posterior2[1]:.0f}%) — total {posterior2[0]+posterior2[1]:.0f}%",
            font_size=22, color=TEAL, weight=BOLD,
        )
        read_text.move_to(read_box.get_center())

        self.play(FadeOut(action_group), FadeOut(self.flop_group), run_time=0.5)
        self.play(FadeIn(read_box), Write(read_text), run_time=1)
        self.wait(2)

        self.final_read = VGroup(read_box, read_text)

    def play_conclusion(self):
        """Final takeaway."""
        self.play(
            FadeOut(self.prior_bars),
            FadeOut(self.prior_pcts),
            FadeOut(self.prior_labels),
            FadeOut(self.prior_title),
            FadeOut(self.prior_header),
            FadeOut(self.prior_desc),
            FadeOut(self.final_read),
            run_time=1,
        )

        lines = VGroup(
            Text("Key Insight from Chapter 3", font_size=36,
                 color=GOLD, weight=BOLD),
            Text("", font_size=10),
            Text("Every opponent action is evidence.", font_size=26,
                 color=SOFTWHITE),
            Text("Bayes' theorem is the engine that converts", font_size=22,
                 color=SOFTWHITE),
            Text("actions into a probability distribution over hands.",
                 font_size=22, color=SOFTWHITE),
            Text("", font_size=10),
            Text("Two updates turned 170 possible hands", font_size=22,
                 color=SLATE),
            Text("into a clear read: big pair or AK.", font_size=22,
                 color=SLATE),
            Text("", font_size=14),
            Text("This is the math behind hand reading.",
                 font_size=28, color=CRIMSON, weight=BOLD),
        )
        lines.arrange(DOWN, buff=0.2)
        lines.move_to(ORIGIN)

        for line in lines:
            self.play(FadeIn(line, shift=UP * 0.2), run_time=0.6)

        self.wait(3)
        self.play(FadeOut(lines), run_time=1)
