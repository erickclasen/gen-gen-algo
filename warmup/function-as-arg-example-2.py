#!/usr/bin/python
#title			:function-as-arg-example.py.py
#description	:From MIT Open Course Ware Fall 2016 6.0001 Ana Bell. Functions as Arguments. This takes a function as an arg and computes the square as an example. Used it as a warmup as I was familiar with fxn pointers in C from using them but, wanted to use in Python for Genetic Algo code to pass a function through to the core GA code.
#author			:Ana Bell orig., mods Erick Clasen
#date			:20200622
#version		:0.2
#usage			:python function-as-arg-example.py.py
#notes			:
#python_version	:2.6.6
#==============================================================================

def sq(func,x):
	y = x
	return func(y)

def f(x):
	return x**2

calc = sq(f,2)
print(calc)
