# the Best Theoretical Distribution

Knowing the underlying (probability) distribution of your data has many modeling
advantages. The easiest manner to determine the underlying distribution is by
visually inspecting the random variable(s) using a histogram. With the candidate
distribution, various plots can be created such as the Probability Distribution
Function plot (PDF/CDF), and the QQ plot.

However, to determine the exact distribution parameters (e.g., loc, scale), it is
essential to use quantitative methods. In this blog, I will describe
_why it is important to determine the underlying probability distribution for your
data set. What the differences are between parametric and non-parametric distributions.
How to determine the best fit using a quantitative approach and how to confirm it
using visual inspections_.
Analyses are performed using the `distfit` library, and a notebook is accompanied
for easy access and experimenting.

## References

- https://towardsdatascience.com/how-to-find-the-best-theoretical-distribution-for-your-data-a26e5673b4bd
