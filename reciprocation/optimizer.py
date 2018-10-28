

# DEPRECATED

from genetic_alg import evaluate

class optimizer:
    def __init__(self,learner,iterations,discountfactor,repetitions):
        self.population=[]
        self.weights=[]

    def anneal(self,initstep,stepsize,minstep):
        step=initstep
        while step>minstep:
            #Generate successor state
            successors=self.generateSuccessors(stepsize)
            #Evaluate successor states
            evaluations=[evaluate(s,self.learner,self.iterations,self.discountfactor,self.repetitions) for s in successors]
            # Thin succession states
            self.population=self.chooseSuccessors(successors,evaluations)
            step=step*stepsize
        # return aggregate result

class hillclimb(optimizer):
    def __init__(self):
        self.steps=[(1,0,0),(0,1,0),(0,0,1),(-1,0,0),(0,-1,0),(0,0,-1)]
        self.allsteps=[(-1,-1,-1),(-1,-1,0),(-1,-1,1),(-1,0,-1),(-1,0,0),(-1,0,1),(-1,1,-1),(-1,1,0),(-1,1,1),
          (0,-1,-1),(0,-1,0),(0,-1,1),(0,0,-1),(0,0,0),(0,0,1),(0,1,-1),(0,1,0),(0,1,1),
          (1,-1,-1),(1,-1,0),(1,-1,1),(1,0,-1),(1,0,0),(1,0,1),(1,1,-1),(1,1,0),(1,1,1)]