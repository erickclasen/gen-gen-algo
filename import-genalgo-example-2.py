#!/usr/bin/python
#title                  :import-genalgo-example.py
#description    :This code shows how to import the test fxn from genalgo and call a local funtion to optimize.
#author                 :Erick Clasen
#date                   :20200622
#version                :0.1
#usage                  :python import-genalgo-example.py
#notes                  :
#python_version :2.6.6
#==============================================================================

import genalgo as ga


def hello_optimize_me(t):
        ''' Example of a function to optimize. In this case solve for sqaure root of two. 
            The format must be in a 0 = t*t -2 form to solve. Taking the abs value allows
            the GA code to minimize the error (cost) to zero.
            The function to optimize has to appear ABOVE the calling function.          '''

        return(abs(t*t - 2))

        #return(abs(t*t - 2*t))
        #return pow(pow(0.5-t,2),0.5) # RMS Error



#pop = ga.read_pop_from_file()
ga.run_algo(hello_optimize_me,loops=1000,bounds=[0,2],optimization_threshold = 0.000001)
#ga.write_pop_to_file(pop)
