# Chapter 1: Decisions Under Risk — Probability and Expectation

## Narration Script

### [0:00 – Title]
"Chapter 1 of The Mathematics of Poker lays the foundation for everything
that follows: probability and expected value. These two ideas are the
engine behind every correct poker decision."

### [0:10 – Why Money, Not Utility]
"The book begins with an important simplification. In reality, people
value money non-linearly — winning five million dollars is worth far more
than half of winning ten million. This is called utility. But to keep the
math tractable, the authors assume players are well-bankrolled and simply
want to maximize the money they win."

### [0:24 – Probability Definition]
"So what is probability? If we dealt a million holdem hands, the fraction
that contain pocket aces would converge on a specific number. That number
is the probability. Formally: the limit of occurrences over trials as
trials approach infinity."

### [0:38 – Counting: Pocket Aces]
"Let's compute it. The chance the first card is an ace is 4 out of 52, or
1 in 13. Given the first card IS an ace, only 3 aces remain among 51
cards. These events are dependent — the first card changes what's left
in the deck. Multiplying: 1/13 times 1/17 gives us 1/221. You'll be
dealt pocket aces roughly once every 221 hands."

### [0:58 – Mutually Exclusive Events]
"Some events can't happen at the same time. A card can't be both the
ace of spades AND the ace of hearts. These are mutually exclusive. For
mutually exclusive events, the probability of A or B is simply the sum
of their individual probabilities. So the chance of being dealt aces,
kings, or queens is 3/221."

### [1:10 – Independent vs Dependent Events]
"Events are independent when one doesn't affect the other — like two
separate dice rolls. For independent events, the joint probability is the
product. But drawing cards without replacement creates dependent events,
where we need conditional probability: P(A and B) = P(A) times P(B given A)."

### [1:26 – The Inclusion-Exclusion Principle]
"When events are NOT mutually exclusive, we can't just add. A card being
a heart and a card being an ace can both be true — the ace of hearts. The
general rule: P(A or B) = P(A) + P(B) minus P(A and B). This avoids
double-counting the overlap."

### [1:40 – Flopping a Flush]
"Here's a beautiful application: what's the chance of flopping a flush
with a suited hand? We hold two suited cards, leaving 11 of our suit in
50 remaining cards. Each successive card is dependent on the last. The
chain of conditional probabilities multiplies out to 33/3920 — just
under 1 percent."

### [1:58 – Probability Distributions]
"A single probability isn't always enough. A probability distribution
pairs every possible outcome with its probability. A coin flip: heads
1/2, tails 1/2. A die roll: each face 1/6. In poker, we use distributions
to represent the range of hands an opponent might hold."

### [2:14 – Expected Value: The Core Concept]
"Now the most important idea in the chapter: expected value. When each
outcome has a dollar value, EV is the sum of each value times its
probability. A fair $10 coin flip has EV of zero — you break even on
average."

### [2:30 – EV of a Favorable Bet]
"But what if your friend pays you $11 when you win and you pay $10 when
you lose? Now EV = (1/2)(+11) + (1/2)(−10) = +$0.50 per flip. You
should always take this bet. This is the essence of poker: find spots
where you have positive expected value."

### [2:46 – EV of a Bad Bet]
"The reverse: your friend pays $30 if you roll double sixes, but you pay
$1 otherwise. EV = (1/36)(+30) + (35/36)(−1) = −$0.14. Negative EV.
Don't take this bet. This exact wager exists on every craps table in
Las Vegas."

### [3:00 – EV is Additive]
"A crucial property: expected value is additive. The EV of six bets in
a row is the sum of each individual EV. This is how casinos profit —
millions of tiny negative-EV bets add up. And it's how winning poker
players profit — by consistently choosing positive-EV actions."

### [3:16 – Key Takeaways]
"Chapter 1's message is clear: poker decisions are evaluated by their
expected value. Probability gives us the framework. EV gives us the
criterion. A mathematical player's entire goal is to maximize the sum
of expected values across every decision they make."
