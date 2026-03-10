# Chapter 2: Predicting the Future — Variance and Sample Outcomes

## Narration Script

### [0:00 – Title]
"Chapter 2 introduces a concept just as important as expected value: variance. Knowing your expected profit means nothing if you don't understand how wildly your actual results can swing around that number. Variance quantifies that swing."

### [0:12 – Variance Definition]
"Variance measures how spread out the possible outcomes are from the mean. The formula sums each outcome's squared distance from the expected value, weighted by its probability. We square the distances so that outcomes above and below the mean don't cancel each other out. A high variance means the results are all over the place; a low variance means they cluster tightly around the EV."

### [0:30 – Variance Examples: Coin vs Die]
"Let's build intuition with two simple examples. A fair coin flip — plus one or minus one — has an EV of zero. Each outcome is exactly one unit from the mean, so the variance is one. Now consider a standard die roll. The outcomes range from one to six with a mean of three-point-five. The squared distances are larger and more spread out, giving a variance of about two-point-nine-two. More possible outcomes and a wider range mean more variance."

### [0:52 – Standard Deviation]
"Variance is measured in squared units — dollars squared, for instance. That's hard to interpret. So we take the square root to get the standard deviation, sigma. Standard deviation is in the same units as our expected value, which makes comparison natural. For the coin flip, sigma equals one. For the die, sigma is about one-point-seven-one."

### [1:06 – Variance Additivity]
"Here's a critical property: variance is additive across independent trials. If you play N rounds, the total variance is N times the single-round variance. But standard deviation grows with the square root of N, not N itself. This is the key — your expected profit grows linearly, but the noise around it grows much more slowly. The signal eventually overwhelms the noise."

### [1:22 – The Normal Distribution]
"When you add up many independent random variables, the Central Limit Theorem tells us the total approaches a normal distribution — the famous bell curve. About 68 percent of outcomes fall within one standard deviation of the mean. About 95.5 percent within two. And 99.7 percent within three. This gives us a powerful framework for predicting where our results are likely to land."

### [1:40 – Z-Scores]
"A z-score converts any result into a standardized scale. Take your observed result, subtract the mean, and divide by the standard deviation. A z-score near zero means the result is typical. A z-score of two means you're out in the 5 percent tail — unusual but not impossible. Beyond three, and the result is extremely rare, less than three-tenths of a percent."

### [1:56 – Die Game D2]
"The book introduces a die game called D2: you win six dollars on a six and lose one dollar on anything else. The EV is one-sixth of a dollar per roll — a positive expectation game. But the variance is about 6.8, giving a standard deviation of 2.6 per roll. After 200 rolls, your expected profit is 33 dollars, but the standard deviation is nearly 37 dollars. Despite positive EV, there's roughly an 18 percent chance you're still behind after 200 trials. Variance is real."

### [2:16 – Poker Session Reality]
"Now apply this to poker. A solid winning player earns 0.015 big blinds per hand with a standard deviation of 2 big blinds per hand. In a 300-hand session, the expected win is just 4.5 big blinds — but the standard deviation is almost 35 big blinds. That's nearly eight times the expected win. Run the z-score calculation and this player only wins 55 percent of their sessions. Nearly half the time, a genuine winner walks away a loser. This is why session results mean so little."

### [2:38 – Sample Size Table]
"As the sample grows, the picture changes dramatically. At 300 hands, the 95 percent confidence interval is about 15 times the expected value. At 10,000 hands, it shrinks to about 2.6 times. At a million hands, it's just 0.3 times. The noise doesn't disappear, but it becomes tiny compared to the signal. This is the law of large numbers in action — and it's why tracking thousands, not hundreds, of hands matters for evaluating your poker ability."

### [2:56 – AK vs AQ Story]
"The chapter closes with a memorable example. A player claims that AK versus AQ is basically fifty-fifty based on his experience over 2,000 hands. But AK actually wins about 70 percent of the time. Over 2,000 hands, the expected wins would be 1,400 with a standard deviation of roughly 26. To be at 50 percent, the z-score would be around negative 15 — an event so improbable it would never happen in the lifetime of the universe. The player's claim isn't just unlikely, it's impossible. Variance is real, but it has limits — and z-scores let us identify when someone's story doesn't add up."

### [3:16 – Key Takeaways]
"Chapter 2's message is both humbling and empowering. Variance means you will lose sessions, sometimes many in a row, even when you're playing well. But the math is on your side in the long run. EV grows with N while standard deviation grows with only the square root of N. Play enough hands, and your true edge will emerge from the noise. The tools of variance, standard deviation, and z-scores are your defense against both false confidence and unnecessary despair."
