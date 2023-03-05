#!/usr/bin/python
#title			:import-genalgo-example.py
#description	:This code shows how to import the test fxn from genalgo and call a local funtion to optimize.
#author			:Erick Clasen
#date			:20200622
#version		:0.1
#usage			:python import-genalgo-example.py
#notes			:
#python_version	:2.6.6
#==============================================================================

import genalgo as ga


def hello_optimize_me(t):
        return pow(pow(0.5-t,2),0.5) # RMS Error
	#return abs(0.5-t)

pop = ga.read_pop_from_file()
ga.run_algo(hello_optimize_me,pop,loops=1000,optimization_threshold = 0.000001)
ga.write_pop_to_file(pop)
