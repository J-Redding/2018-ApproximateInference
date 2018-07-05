Performs approximate inference methods on a Hidden Markov Model to produce a probability distribution for an unobserved variable in a series of unobserved variables.

The HMM represents a series of days. 
There are two variables. 
The unobserved variables {R_0, R_1,..., R_T} represent if it is raining. 
The observed variables {U_0, U_1,..., U_T} represent if somebody was observed with an umbrella on that day.

Returns the probability distribution for P(R_T| U_0, U_1,...,U_T).

The following probabilities are already known:
P(R_0 = True) = 0.2
P(R_t = True | R_(t - 1) = True) = 0.7
P(R_t = True | R_(t - 1) = False) = 0.3
P(U_t = True | R_t = True) = 0.9
P(U_t = True | R_t = False) = 0.2

Uses and returns both the likelihood weighted sampling and Gibbs sampling probability distributions.

Input is a text file containing a sequence of white space seperated binary numbers.
e.g. 0 1 1 0
This sequence represents the observed variable sequence, with 0 indicating False and 1 indicating True.
