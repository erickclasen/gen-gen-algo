import random

def test(t):
	return abs(0.5-t)

# MAIN
pop = [0,0,0]

for x in range(len(pop)):
  pop[x] = random.random()
  print("population",x,pop[x])

#for x in range(len(pop)):
sample_pop = random.randint(0,len(pop)-1)
fitness_ref = test(pop[sample_pop])
print("Test Fitness, pop# and fitness: ",sample_pop,fitness_ref) 

# Breed at random
A = random.randint(0,len(pop)-1)
B = random.randint(0,len(pop)-1)

# Rechoose if they are equal to the same index
while B == A:
	B = random.randint(0,len(pop)-1)


print("A,B:",A,B)
C_value = (pop[A]+pop[B])*0.5
print("Breed:",A,B,C_value)

# Test Fitness
fitness_offspring = test(C_value)
print("fitness of offspring",fitness_offspring)

if fitness_offspring < fitness_ref: # Minimize the error in this case.
	pop[sample_pop] = C_value # Replace a element of pop with offspring.
	print("Replace")
else:
	print("Leave")
