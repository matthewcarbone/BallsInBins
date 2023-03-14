# Balls in Bins

A simple balls-in-bins simulator. The problem considers throwing $N$ balls into $M$ bins, and the various statistical puzzles that embody the problem. Here are a few problems we'll consider here.

**Resources**
- [Purdue lecture notes on the balls in bins problem](https://www.cs.purdue.edu/homes/hmaji/teaching/Spring%202017/lectures/03.pdf)

## Tutorial on the GitHub Actions Yaml file

GitHub Actions triggers whenever there is some change to a repository (or the user triggers an Action manually). When this happens, GitHub looks for files with the `.yml` extension in a hidden directory (one with a `.` prefix) called `.github/workflows`. Every `.yml` file in that directory is executed.

Today, we'll look at one such directory, which I've called `ci.yml` (though you can call it whatever you want). We'll look through it one step at a time.

### Naming your workflow

The first line simply names the Action:

```yaml
name: my_CI_workflow
```

Nothing more, nothing less. It will show up with the same name under the Actions tab on a GitHub repository.

### Specifying when the workflow should trigger

The next piece is important. GitHub will not just run any workflow, it only will run the workflows it is allowed to. When the workflow is triggered is determined by the `on` key. In this case, we have the following,

```yaml
on:
  pull_request:
    branches:
      - master
  push:
    branches:
      - master
```

In the simplest terms, this workflow file will run on
- pull requests in which the target branch is `master`
- pushes directly to the `master` branch

You can find more details on the specific options [here](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#on).

### Building and testing your code

TK


## Overview of some balls-in-bins theory

### Number of empty bins

After throwing $N$ balls into $M$ bins, one interesting question we can ask is how many bins are empty?

First consider the probability that any single bin is empty after $N$ throws. Given that the probability of any ball landing in any single bin is $1/M,$ the probability of a ball _not_ landing in any single bin is its complement: $1-1/M.$ For a bin to be empty after $N$ throws, this would have to happen $N$ times: $(1-1/M)^N.$ Put more precisely, the indicator variable for whether or not bin $i$ is empty is given by 

$$ E[X_i] = (1-1/M)^N. $$

Let $X$ be the random variable representing the total number of empty bins after $N$ throws. The total expected number of empty bins is just this value, multiplied by the total number of bins:

$$ \mathbb{E}[X] = \sum_{i=1}^M E[X_i] = M (1 - 1/M)^N.$$

### Number of collisions

The number of collisions (aka the birthday paradox) is a common problem in probability theory.

Let $X_{ij}$ be an indicator variable which is equal to 1 if $i$th and $j$th balls fall into the same bin. Given every throw is independent, we throw ball $i$ and allow it to land somewhere. The probability then that ball $j$ lands in the same bin as $i$ is simply $1/M.$ This can also be framed as the expectation of this random variable:

$$ \mathbb{E}[X_{ij}] = 1/M.$$

Next, we define a new random variable $X$ which counts the total number of collisions in a specific way,

$$ X = \sum_{1 \leq i < j \leq N} X_{ij}.$$

We want the expected number of collisions on average,

$$ \mathbb{E}[X] = \mathbb{E}\left[\sum_{1 \leq i < j \leq N} X_{ij}\right] = \sum_{1 \leq i < j \leq N} \mathbb{E}[X_{ij}]$$

with the second equality from linearity of expectation. This sum can be solved analytically,

$$ \mathbb{E}[X] = {N \choose 2} \frac{1}{M}. $$

