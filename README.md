# gen-gen-algo
A generic genetic algorithm. Functions can be passed to it for optimization.
genalgo.py README.md
## Overview

This repository contains a Python module called genalgo.py, which includes Genetic Algorithm Code that can be used for optimization or in a machine learning application. Additionally, it includes a basic stochastic optimization algorithm as a warm-up.
Requirements

    Python 2.6.6 or higher

## Usage

To use this module, run the following command:
```
python genalgo.py
```
or 
```
import genalgo
```

## Contents

**example_called_fxn**: A function that returns the error value, how far it is away from 0.5, which is to be minimized.

**test**: A generic function that can contain anything to test and optimize. It uses a function passed in as an argument. This function just is a wrapper and returns the so-called output of the function called to be optimized.

**calculate_best_parameter**: A function that averages all of the populations and then uses a smoothing function to create a best parameter. Smoothing function works like an EMA or IIR filter. In this case, a = a*(1-c) + b*c, where c is an exponential weighting constant that takes most of the old value and recurses it with a new b added in small doses.

**generate_random_trial**: A function that generates a uniform random trial value whose value is constrained by the bounds.

**sa**: A function for Stochastic Optimization. It just creates a random number and is just like taking a guess, if the guess is better than the last one, then discard the last guess. It will work with just a population of one. It is basically stripped-down GA code.

**mutate**: A function that allows an element of the population picked at random to be mutated by replacement via a random value.

**random_pop_select**: A function that randomly selects two indexes to grab from the population. The while makes sure that they are unique.

**generate_offspring**: A function that uses a regular average formula to generate the offspring.

## How to contribute

Contributions to the code are welcome! Just open a pull request and we'll take a look at it.
License

This project is licensed under the MIT License - see the LICENSE file for details.
