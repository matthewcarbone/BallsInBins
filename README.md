# Balls in Bins

A simple balls-in-bins simulator. The problem considers throwing $N$ balls into $M$ bins, and the various statistical puzzles that embody the problem. However, the real point of this tutorial is to get you familiar with [GitHub Actions](https://docs.github.com/en/actions/learn-github-actions). See below!


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

The `jobs` key specifies what the parameter file should do. In this case, we have three differet jobs (`build_and_test`, `black`, and `flake8_py3`):

```yaml
jobs:
  build_and_test:
    ...
  black:
    ...
  flake8_py3:
    ...
```

We'll go over each of these in detail, but briefly, `build_and_test` does exactly what you'd expect it to do. It builds and tests your code. `black` and `flake8_py3` are programs you may not be familiar with. `black` checks that your code "style" is "good" (more on what good means at Black's docs page), and `flake8_py3` runs the `flake8` linter on your code, ensuring no syntax or formatting errors.

#### Build and test

So how do we build and test the code? Here are the steps in the `build_and_test` dictionary:

```yaml
  build_and_test:

    strategy:
      matrix:
        platform: [ubuntu-latest]
        python-version: ["3.9", "3.11"]
      fail-fast: false
    runs-on: ${{ matrix.platform }}

    steps:
    - uses: actions/checkout@v3

    - uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Build and install
      run: pip install --verbose ".[test]"

    - name: Run tests
      run: |
        pytest -v --cov --cov-report xml balls_in_bins/_tests
```

Let's go over each of these one-by-one. First of all, there are three keys in the `build_and_test` "header": `strategy`, `runs-on` and `steps`. The `strategy` tells Actions how to run the job.

- The `matrix` keyword specifies all combinations of the values of whatever lists come after it. In this case, all possible combinations of different listed `platform`s (operating systems) and `python-version`s. In this case, this means the matrix will run Python 3.9 on the latest version of Ubuntu, and Python 3.11 on the latest version of Ubuntu. You can specify other operating systems here too, like `macos-latest` to run on the most recent Mac operating system. More details [here](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#jobsjob_idstrategymatrix).
- The `fail-fast` set to False keyword simply says that if any job in the matrix fails, to cancel any other jobs currently running in the matrix. This allows for quicker debugging. More details [here](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#jobsjob_idstrategyfail-fast).

While it is not listed under `strategy`, `runs-on` simply tells Actions what to run `build_and_test` on. In this case, we actually want it to run on the operating system specified in the matrix. This can be accessed via environment variable `${{ matrix.platform }}`, which Actions knows how to parse when the job is run.

Finally, `steps` then defines sequential steps taken by the rest of the action. Each step can "use" a different action, which can be accessed via e.g. `actions/checkout@v3`, which conveniently tells the workflow to checkout to your current repository's commit. Our steps are:

```yaml
steps:
- uses: actions/checkout@v3

- uses: actions/setup-python@v4
  with:
    python-version: ${{ matrix.python-version }}

- name: Build and install
  run: pip install --verbose ".[test]"

- name: Run tests
  run: |
    pytest -v --cov --cov-report xml balls_in_bins/_tests
```

Note that when running `uses` with an Action, that these Actions are actually just more code on GitHub. For example, `actions/setup-python` can be accessed [here](https://github.com/actions/setup-python)! In addition, while the `actions` organization is run by GitHub, anyone can create and deploy an action, such `rickstaa/action-black@v1` later on in the workflow.

The last two steps are given custom names and do two things. First, we install our package using the optional testing requirements. Second, we run the tests using `pytest`. If all of the tests pass, we pass the Action. If any test fails, we fail the action.


#### Code quality checks

While not critical to ensure that a code runs correctly, it is very important for development to follow a certain standard of quality. [Black](https://black.readthedocs.io/en/stable/) and [Flake8](https://flake8.pycqa.org/en/latest/) are two such tools that enforce certain style requirements. Note that syntax errors will show up on the tests, but code style errors will not. Try and figure out what each of these Actions does on your own.



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

