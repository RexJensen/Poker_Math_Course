# Chapter 3: Using All the Information — Estimating Parameters and Bayes' Theorem

## Narration Script

### [0:00 – Title]
"One of the most powerful ideas in The Mathematics of Poker is that hand reading isn't guesswork — it's Bayesian inference. Every time your opponent acts, they reveal information. Bayes' theorem is how we turn that information into a probability distribution over their possible holdings."

### [0:08 – Prior Distribution]
"Before any action, your opponent could hold any of the 169 distinct starting hands. But not all hands are created equal. We group holdings into five categories — Premium, Strong, Medium, Speculative, and Weak — and assign prior probabilities based on how frequently each type appears. Notice that weak hands dominate: nearly two-thirds of all starting hands fall into that bucket. Premium hands like aces, kings, and ace-king suited make up just two and a half percent. This is our starting point — the prior distribution."

### [0:22 – Bayes' Formula]
"Here is the updating engine: Bayes' theorem. The posterior probability of a hand category given an observed action equals the likelihood of that action given the hand, times the prior probability of the hand, divided by the total probability of the action across all categories. In plain language: posterior equals likelihood times prior, divided by evidence. The likelihood captures how often a player with that specific hand type would take the action we just observed."

### [0:36 – Preflop: Villain Raises UTG]
"Now the action begins. Our opponent raises from under the gun — the earliest position at the table, where only the tightest ranges are profitable. How likely is each hand category to raise from here? Premium hands raise almost always — ninety-five percent of the time. Strong hands raise seventy percent. But medium hands only twenty-five percent, speculative hands just eight percent, and weak hands a mere two percent. Watch the bar chart as we apply Bayes' theorem. The distribution shifts dramatically. Premium and strong hands now tower over the rest. Weak hands, which started as the overwhelming majority, have nearly disappeared. A single action has completely reshaped the probability landscape."

### [0:53 – Flop: K-spade 7-heart 2-diamond]
"The flop comes down: king of spades, seven of hearts, two of diamonds. A dry, rainbow board with no flush draws and no connected cards. This is a board that strongly favors hands that already have a made pair — especially big pairs and ace-king."

### [1:01 – Flop: Villain C-bets 2/3 Pot]
"Our opponent fires a continuation bet of two-thirds pot. Time for a second Bayesian update. Premium hands — sets, overpairs, top pair top kicker — bet this board roughly ninety percent of the time. Strong overpairs like queens and jacks bet seventy-five percent. But medium hands that missed bet only thirty percent, speculative hands fifteen percent, and weak hands just five percent. After this second update, the picture is unmistakable. Premium hands now account for the clear majority of our opponent's range, and premium plus strong together make up the vast bulk of the distribution. Two rounds of Bayesian updating have turned a vague universe of possible hands into a sharp, actionable read: this opponent almost certainly holds a big pair or ace-king."

### [1:15 – Conclusion]
"This is the core lesson of Chapter 3. Every action your opponent takes — a raise, a call, a bet, a check — is a data point. Bayes' theorem is the machine that processes that data and converts it into knowledge. Two simple updates turned a hundred and seventy possible starting hands into a clear read. The players who learn to think this way, updating probabilities with each new piece of evidence, have a profound mathematical edge over those who rely on gut feeling alone. This is the math behind hand reading."
