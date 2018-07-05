#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import random

#These are our probability constants, defined by the spec
#Probability R_0 is true
rZeroTrue = 0.2
#Probability R_0 is false
rZeroFalse = 0.8
#Probability R_t is true, given R_t-1 is true
rtTrueRtMinOneTrue = 0.7
#Probability R_t is false, given R_t-1 is true
rtFalseRtMinOneTrue = 0.3
#Probability R_t is true, given R_t-1 is false
rtTrueRtMinOneFalse = 0.3
#Probability R_t is false, given R_t-1 is false
rtFalseRtMinOneFalse = 0.7
#Probability U_t is true, given R_t is true
utTrueRtTrue = 0.9
#Probability U_t is false, given R_t is true
utFalseRtTrue = 0.1
#Probability U_t is true, given R_t is false
utTrueRtFalse = 0.2
#Probability U_t is false, given R_t is false
utFalseRtFalse = 0.8

#State variable is used to create the states for the Hidden Markov Model
#Each raining variable is a state
#i.e. each R_t for 0 <= t <= T
class StateVariable:
	def __init__(self, evidenceVariable, step):
		#Evidence variable is the observed umbrella variable per R
		#i.e. each U_t for 0 <= t <= T
		#This is a boolean value to indicate observed or unobserved
		#This is defined by the input text file
		self.evidenceVariable = evidenceVariable
		#Step represents the number of the state variable in the Hidden Markov Model
		self.step = step
		#Next state points to the next state variable in the Hidden Markov Model
		self.nextState = None

#Builds a Hidden Markov Model data structure, given a set of observations
#Observations is a string of observed evidence variables
#It is the input text file, with the whitespace removed
#The head of the string is removed after each recursion, indicating that the related state variable has been created
#Constructs the Hidden Markov Model recursively, one state variable at a time
#Takes in the step of the current state variable
#Returns the head of the Hidden Markov Model
def buildHiddenMarkovModel(observations, step):
	#If there are no observations left, all of the state variables have been constructed
	if len(observations) == 0:
		#We're done
		return None

	else:
		evidenceVariable = None
		if observations[0] == "0":
			#There was no umbrella observed
			evidenceVariable = False

		elif observations[0] == "1":
			#There was an umbrella observed
			evidenceVariable = True

		#Build the current state variable
		currentState = StateVariable(evidenceVariable, step)
		#Build the next state variable
		currentState.nextState = buildHiddenMarkovModel(observations[1:], step + 1)
		#Return the current state
		return currentState

#Generates a sample using likelihood weighting
#Weight is the current weight of the sample
#Current state is the current state variable being sampled
#Sample is a string indicating the boolean values of each state variable sampled so far
#Takes the sample recursively, one state variable at a time
#Returns the string of sample values and the weight value
def generateLikelihoodSample(weight, currentState, sample):
	#If the current state does not exist
	#We have reached the end of the Hidden Markov Model
	if not currentState:
		#We're done
		return sample, weight

	else:
		#Get a random sample number
		sampleNumber = random.random()
		#If the sample number is less than the probability distribution that the current state variable is true
		#We note the current state variable as being sampled true
		#We consider the region after this probability to represent the probability distribution that the current state is false

		#If the current state is the head of the Hidden Markov Model
		#We cannot account for P(R_i | R_(i - 1))
		if currentState.step == 0:
			#We use the P(R_0) distribution
			#If the sample number is less than the probability distribution that the current state variable is true
			#We note the current state variable as being sampled true
			#We consider the region after this probability to represent the probability distribution that the current state is false
			if sampleNumber < rZeroTrue:
				#Note the sample as true
				sample += "t"
				#If the umbrella was observed
				if currentState.evidenceVariable == True:
					#w <- w * P(U_t = True | R_t = True)
					weight *= utTrueRtTrue

				#If the umbrella was not observed
				elif currentState.evidenceVariable == False:
					#w <- w * P(U_t = False | R_t = True)
					weight *= utFalseRtTrue

			#If the sample number is within the probability distribution for false
			elif sampleNumber >= rZeroTrue:
				#Note the sample as false
				sample += "f"
				#If the umbrella was observed
				if currentState.evidenceVariable == True:
					#w <- w * P(U_t = True | R_t = False)
					weight *= utTrueRtFalse

				#If the umbrella was not observed
				elif currentState.evidenceVariable == False:
					#w <- w * P(U_t = False | R_t = False)
					weight *= utFalseRtFalse

		#If the current state is not the head
		elif currentState.step > 0:
			#If the previous state variable was noted as true
			if sample[currentState.step - 1] == "t":
				#If the sample number is within the probability distribution for true
				if sampleNumber < rtTrueRtMinOneTrue:
					#Note the sample as true
					sample += "t"
					#If the umbrella was observed
					if currentState.evidenceVariable == True:
						#w <- w * P(U_t = True | R_t = True)
						weight *= utTrueRtTrue

					#If the umbrella was not observed
					elif currentState.evidenceVariable == False:
						#w <- w * P(U_t = False | R_t = True)
						weight *= utFalseRtTrue

				#If the sample number is within the probability distribution for false
				elif sampleNumber >= rtTrueRtMinOneTrue:
					#Note the sample as false
					sample += "f"
					#If the umbrella was observed
					if currentState.evidenceVariable == True:
						#w <- w * P(U_t = True | R_t = False)
						weight *= utTrueRtFalse

					#If the umbrella was not observed
					elif currentState.evidenceVariable == False:
						#w <- w * P(U_t = False | R_t = False)
						weight *= utFalseRtFalse

			#If the previous state variable was noted as false
			elif sample[currentState.step - 1] == "f":
				#If the sample number is within the probability distribution for true
				if sampleNumber < rtTrueRtMinOneFalse:
					#Note the sample as true
					sample += "t"
					#If the umbrella was observed
					if currentState.evidenceVariable == True:
						#w <- w * P(U_t = True | R_t = True)
						weight *= utTrueRtTrue

					#If the umbrella was not observed
					elif currentState.evidenceVariable == False:
						#w <- w * P(U_t = False | R_t = True)
						weight *= utFalseRtTrue

				#If the sample number is within the probability distribution for false
				elif sampleNumber >= rtTrueRtMinOneFalse:
					#Note the sample as false
					sample += "f"
					#If the umbrella was observed
					if currentState.evidenceVariable == True:
						#w <- w * P(U_t = True | R_t = False)
						weight *= utTrueRtFalse

					#If the umbrella was not observed
					elif currentState.evidenceVariable == False:
						#w <- w * P(U_t = False | R_t = False)
						weight *= utFalseRtFalse

	#Return the next likelihood sample
	return generateLikelihoodSample(weight, currentState.nextState, sample)

#Performs likelihood weighted sampling on a given Hidden Markov Model for a given number of samples
#Returns the probability distribution for R_t
def likelihoodWeightedSampling(hiddenMarkovModel, numberSamples):
	#Samples will contain all of the strings of samples returned
	#i.e. ["tttf", "ttft", etc.]
	samples = []
	#Tallies contains the counts for how many times each sample was returned
	#The index of a tally corresponds to the sample of the same index
	tallies = []
	#Weights contains the weights associated to each sample
	weights = []
	#Perform N samples
	for n in range(numberSamples):
		#Get the samples and the weight
		#Initialise the weight as 1
		sample, weight = generateLikelihoodSample(1, hiddenMarkovModel, "")
		#Check to see if this sample has been returned before
		if sample in samples:
			#If it has, increase its tally by one
			tallies[samples.index(sample)] += 1

		#If this sample has not been returned before
		elif sample not in samples:
			#Add the sample and weight to their lists, and create a new tally
			samples.append(sample)
			tallies.append(1)
			weights.append(weight)

	t = len(samples[0]) - 1
	likelihoodRtTrue = 0
	likelihoodRtFalse = 0
	sampleIndex = 0

	#Compute the likelihood weighted estimates
	#For each sample
	for sample in samples:
		#If R_t was predicted to be true
		if sample[t] == "t":
			#Add the tally count for this sample multiplied by its weighting to the probability distribution for true
			likelihoodRtTrue += tallies[sampleIndex] * weights[sampleIndex]

		#If R_t was predicted to be false
		elif sample[t] == "f":
			#Add the tally count for this sample multiplied by its weighting to the probability distribution for false
			likelihoodRtFalse += tallies[sampleIndex] * weights[sampleIndex]

		sampleIndex += 1

	#Apply the alpha value
	alpha = 1 / (likelihoodRtTrue + likelihoodRtFalse)
	likelihoodRtTrue *= alpha
	likelihoodRtFalse *= alpha

	#Return the probability distribution
	return likelihoodRtTrue, likelihoodRtFalse

#Performs Gibbs sampling on a given Hidden Markov Model for a given number of samples
#Returns the probability distribution for R_t
def gibbsSampling(hiddenMarkovModel, numberSamples):
	#Samples will contain all of the strings of samples returned
	#i.e. ["tttf", "ttft", etc.]
	samples = []
	currentState = hiddenMarkovModel
	#Sample list is a list of the values in the current sample
	#It is combined later to form the sample string
	#i.e. ["t", "t", "f", "t"]
	sampleList = []

	#Initialise the non-evidence variables randomly
	#For all of the state variables in the Hidden Markov Model
	while currentState != None:
		sampleNumber = random.random()
		#Decide whether they're true or false randomly, so give them a 50/50 chance of either
		if sampleNumber < 0.5:
			#State variable is true
			sampleList.append("t")

		elif sampleNumber >= 0.5:
			#State variable is false
			sampleList.append("f")

		#Move on to the next state
		currentState = currentState.nextState

	#This will be out initial sample
	#Join it as a string, and add it to the list of samples
	sample = "".join(sampleList)
	samples.append(sample)

	currentState = hiddenMarkovModel

	#Perform N - 1 samples
	#N - 1 because we already have our initial sample
	for n in range(numberSamples - 1):
		#Get the probability distribution for the current state variable, given its Markov Blanket
		#P(R_i | R_(i - 1), U_i, R_(i + 1))
		#We can rewrite this as
		#P(R_i | R_(i - 1)) * P(R_i | U_i) * P(R_(i + 1) | R_i)
		riTrueMarkovBlanket = 0
		riFalseMarkovBlanket = 0
		#If the umbrella was observed
		if currentState.evidenceVariable == True:
			#P(R_i | U_i = True)
			riTrueMarkovBlanket = utTrueRtTrue
			riFalseMarkovBlanket = utTrueRtFalse

		elif currentState.evidenceVariable == False:
			#P(R_i | U_i = False)
			riTrueMarkovBlanket = utFalseRtTrue
			riFalseMarkovBlanket = utFalseRtFalse

		#If this is not the head of the Hidden Markov Model
		#We can account for P(R_i | R_(i - 1))
		if currentState.step > 0:
			#If the previous state variable was noted as true
			if sampleList[currentState.step - 1] == "t":
				#P(R_i | R_(i - 1) = True)
				riTrueMarkovBlanket *= rtTrueRtMinOneTrue
				riFalseMarkovBlanket *= rtFalseRtMinOneTrue

			#If the previous state variable was noted as false
			elif sampleList[currentState.step - 1] == "f":
				#P(R_i | R_(i - 1) = False)
				riTrueMarkovBlanket *= rtTrueRtMinOneFalse
				riFalseMarkovBlanket *= rtFalseRtMinOneFalse

		#If this is not the end of the Hidden Markov Model
		#We can account for P(R_(i + 1) | R_i)
		if currentState.step < len(sampleList) - 1:
			#If the next state variable was noted as true
			if sampleList[currentState.step + 1] == "t":
				#P(R_(i + 1) = True | R_i)
				riTrueMarkovBlanket *= rtTrueRtMinOneTrue
				riFalseMarkovBlanket *= rtTrueRtMinOneFalse

			#If the next state variable was noted as false
			elif sampleList[currentState.step + 1] == "f":
				#P(R_(i + 1) = False | R_i)
				riTrueMarkovBlanket *= rtFalseRtMinOneTrue
				riFalseMarkovBlanket *= rtFalseRtMinOneFalse

		#Apply the alpha value
		alpha = 1 / (riTrueMarkovBlanket + riFalseMarkovBlanket)
		riTrueMarkovBlanket *= alpha
		riFalseMarkovBlanket *= alpha

		#Get a random sample number
		sampleNumber = random.random()
		#If the sample number is within the probability distribution for true
		if sampleNumber < riTrueMarkovBlanket:
			#Note the sample as true
			sampleList[currentState.step] = "t"

		#If the sample number is within the probability distribution for false
		elif sampleNumber >= riTrueMarkovBlanket:
			#Note the sample as false
			sampleList[currentState.step] = "f"

		#Join it as a string, and add it to the list of samples
		sample = "".join(sampleList)
		samples.append(sample)

		#Move on to the next state variable
		#If there is no next state variable, we restart from the head
		if not currentState.nextState:
			currentState = hiddenMarkovModel

		#Otherwise we just move down one
		elif currentState.nextState != None:
			currentState = currentState.nextState

	#Now that we have our samples, we can determine the probability distribution
	#We want to count how many times R_t is predicted to be true/false
	trueCount = 0
	falseCount = 0
	t = len(samples[0]) - 1
	#For each sample
	for sample in samples:
		if sample[t] == "t":
			#R_t was predicted to be true
			trueCount += 1

		elif sample[t] == "f":
			#R_t was predicted to be false
			falseCount += 1

	#Apply the alpha value
	alpha = 1 / (trueCount + falseCount)
	gibbsRtTrue = trueCount * alpha
	gibbsRtFalse = falseCount * alpha

	#Return the probability distribution
	return gibbsRtTrue, gibbsRtFalse

def main(argv):
	#Open and read the observation text file
	observationFile = open(argv[0], "r")
	observations = observationFile.read()

	#Clear the whitespace from the input
	observations = observations.replace(" ", "")
	observations = observations.strip()

	#Build the Hidden Markov Model
	hiddenMarkovModel = buildHiddenMarkovModel(observations, 0)

	#Get the probability distribution of R_t as given by Likelihood Weighted Sampling
	likelihoodTrue, likelihoodFalse = likelihoodWeightedSampling(hiddenMarkovModel, 20000)
	print(likelihoodTrue, likelihoodFalse, "Likelihood")

	#Get the probability distribution of R_t as given by Gibbs Sampling
	gibbsTrue, gibbsFalse = gibbsSampling(hiddenMarkovModel, 20000)
	print(gibbsTrue, gibbsFalse, "Gibbs")

main(sys.argv[1:])