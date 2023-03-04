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
* See the example code **import-genalgo-example.py** and **import-genalgo-example-2.py** to see "hello world" importing examples.

## Features

   - Passed Function: The genetic algorithm can be passed a function to optimize.
   - Stochastic algorithm as a sanity check: The stochastic algorithm can be used as a quick check to ensure that the code is functioning properly before running the more computationally expensive genetic algorithm.
   - Flexible input parameters: The genetic algorithm's input parameters can be adjusted to optimize performance for the specific problem being solved.
   - Bounds: Bounds can be set on the search range.
   - Rates - Mutation rates can be asjusted along with a type of annealling that looks for when the population has become too stagnant and requires a slight shakeup by dithering the values around. The idea that inspired this is simulated annealing and also a cat breeding example... I happened to remember a story about farmers having barn cats and once and a long while they have to do a cat exchange with another farmer to shake up the genetics a bit or else the offspring settles down to an unfit level.
   - Min or Max Optimization - Can optimize for a maximum value or minimum value.
   - Best Parameter in [0] - The best performing parameter is always bubbled into the [0] position for ease of use and visual confirmation when looking at the array.
   - Uniform or Gaussian random mutations.

## Contents
* **genalgo.py** - is the code that can be imported as a module to perform optimization using a genetic algorithm.
* **import-genalgo-example.py** and **import-genalgo-example-2.py**  Two "hello world" types of examples of importing and running the GA code.
* **genalgo-unit-test.py** - Runs the algorithm code 100 times of 100 epochs, adjustable. Then it prints statistics of how it behaved. Useful as a sanity check and when optimizing parameters and looking for problems due to edge cases.
* **genalgo-production.py** - Used in a production code setting, this version is slightly different, it has a few different functions from the regular genalgo.py. The main difference between the two sets of Python defs is in the default values of the "bounds" parameter in some of the functions.In the first code (genalgo.py), the "bounds" parameter default value is set to a list [0,1], while in the other code (genalgo-production.py), the "bounds" parameter default value is set to a tuple (0,1). There are also some additional functions in the second set (genalgo-production.py) that are not present in the first code (genalgo.py), such as "deadwood_generate_random_trial", "gaussian_mutate", and "orig_fitness_evaluation".
### Warmup Directory
The files in this directory were the backsotry on this codes development. Basically as I was putting this code together I was working up to the final version by making some smaller steps. I have included these here mostly for educational purposes.

function-as-arg-example-2.py  simple-ga-normalized.py  simple-ga-warmup.py
function-as-arg-example.py    simple-ga.py



## Genalgo.py Functions

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

## Acknowledgements

This code was developed by [insert your name here] and is based on the genetic algorithm implementation by [insert any relevant sources or references here].

## License


This project is licensed under the GNU GPL License - see the LICENSE file for details.
