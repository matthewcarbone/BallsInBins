# Balls in Bins

A simple balls-in-bins simulator. The problem considers throwing $N$ balls into $M$ bins, and the various statistical puzzles that embody the problem. Here are a few problems we'll consider here.

## Number of collisions

[The number of collisions](https://www.cs.purdue.edu/homes/hmaji/teaching/Spring%202017/lectures/03.pdf) (aka the birthday paradox) is a common problem in probability theory.

Let $X_{ij}$ be an indicator variable which is equal to 1 if $i$th and $j$th balls fall into the same bin. Given every throw is independent, we throw ball $i$ and allow it to land somewhere. The probability then that ball $j$ lands in the same bin as $i$ is simply $1/N.$ This can also be framed as the expectation of this random variable:

$$ E[X_{ij}] = 1/n.$$

Next, we define a new random variable $X$ which counts the total number of collisions in a specific way,

$$ X = \sum_{1 \leq i < j \leq M} X_{ij}.$

We want the expected number of collisions on average,

$$ E[X] = E[\sum_{1 \leq i < j \leq M} X_{ij}] = \sum_{1 \leq i < j \leq M} E[X_{ij}]$$

with the second equality from linearity of expectation. This sum can be solved analytically,

$$ E[X] = 