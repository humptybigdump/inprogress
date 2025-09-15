#
# (c) 2017 Andreas Geyer-Schulz
#          Simple Genetic Algorithm in R. 
#
      
#
# Interface Problem Environment with Simple Genetic Algorithm
#
# The Problem Environment is a list of functions defined in 
#     ProblemEnvironment.R:
#
# We need the following functions:
#  ProblemEnv$bitlength()  returns vector with bits used in coding parms
#  ProblemEnv$genelength   total number of bits (sum of bitlength)    
#  ProblemEnv$lb()         lower bounds of parameter box
#  ProblemEnv$ub()         upper bounds of parameter box
#  ProblemEnv$f()          function to be optimized.
#

#' Map the bit strings of a binary gene to parameters in an interval
#'
#' @description \code{GeneMap} maps the bit strings of a binary string
#'              to parameters in an interval.
#'
#' @param \code{gene} a binary gene
#' @param \code{penv} a problem environment
#'
#' @return the decoded gene.
#'
#' @family {gene layer}
#' @seealso EvalGene() uses GeneMap()
#'
#' @examples
#' gene<-InitGene(Parabola2D$genelength())
#' GeneMap(gene, Parabola2D)
#'
#' @export
GeneMap<-function(gene, penv)
{ nparm<-length(penv$bitlength())
  parm<-rep(0, nparm)
  s<-1
  for (i in 1:nparm)
  { bv<-gene[s:(s-1+penv$bitlength()[i])]
	s<-s+penv$bitlength()[i]
	parm[i]<-penv$lb()[i]+(penv$ub()[i]-penv$lb()[i])*
		(sum(bv*2^((length(bv)-1):0))/(2^length(bv)-1)) }
return(parm)
}

#' Evaluates a binary gene in a problem environment
#'
#' @description \code{EvalGene} evaluates a binary gene in
#'              a problem environment. Fitness is maximized. 
#'
#' @details The problem environment \code{penv} must 
#'          contain the following functions:
#'          \itemize{
#'         \item \code{penv$name()} returns the name of the problem
#'               environment.
#'         \item \code{penv$bitlength()} returns a vector whose
#'               elements specify the bit length of each parameter.
#'         \item \code{penv$genelength()} returns the
#'               length of the gene.
#'         \item \code{penv$lb()}
#'               the vector of lower bounds of parameters.
#'         \item \code{penv$ub()}
#'               the vector of upper bounds of parameters.
#'         \item \code{penv$f(parm)}
#'               returns the function value f at point parm.
#'         }
#'
#' @param \code{gene} a binary gene
#' @param \code{penv} a problem environment
#'
#' @return The fitness value of the gene.
#'
#' @family {gene layer}
#' @seealso GeneMap() is used by EvalGene().
#'          Evalpopulation() uses EvalGene().
#' @examples
#' gene<-InitGene(Parabola2D$genelength())
#' EvalGene(gene, Parabola2D)
#' EvalGene(gene, Parabola2D)
#' @export
EvalGene<-function(gene, penv)
{
penv$f(GeneMap(gene, penv))
}


#
# gene level operations
#

#' Initialize a binary gene
#'
#' @description \code{InitGene} generates a random binary gene
#'              with a given length.
#'
#' @param genelength       the length of a gene
#'
#' @return the decoded gene.
#'
#' @family {gene layer}
#' @seealso InitPopulation() uses InitGene()
#'
#' @examples
#' InitGene(20)
#' InitGene(10)
#' InitGene(Parabola2D$genelength())
#'
#' @export
InitGene<-function(genelength)
{
sample(0:1, genelength, replace=T)
}

#' Initializes a population of genes.
#'
#' @description \code{InitPopulation} initializes a population
#                  of genes.
#'
#' @param \code{genelength} the length of a gene. 
#' @param \code{popsize} the population size
#'
#' @return list of genes.
#'
#' @family {population layer}
#' @seealso InitGene() is used by InitPopulation()
#'
#' @examples
#' pop10<-InitPopulation(5, 10)
#' pop10
#'
#' @export
InitPopulation<-function(genelength, popsize)
{
lapply(rep(genelength, popsize), InitGene)
}

#' Evaluates a population of genes in a a problem environment
#'
#' @description \code{EvalPopulation} evaluates a population
#'                  of genes in a problem environment.
#'
#' @param \code{pop} a population of genes.
#' @param \code{penv} a problem environment.
#'
#' @return a list of fitness values.
#'
#' @family {population layer}
#' @seealso EvalGene() is used by Evalpopulation()
#'
#' @examples
#' pop10<-InitPopulation(Parabola2D$genelength(), 10)
#' fit<-EvalPopulation(pop10, Parabola2D)
#' @export
EvalPopulation<-function(pop, penv)
{
	unlist(lapply(pop, EvalGene, penv=penv))
}

#' Selection proportional to fitness differences
#'
#' @description \code{SelectGene} implements selection
#'              proportional to fitness differences.
#'              It selects a gene out of the population.
#'              with a probability proportional to the fitness
#'              difference to the gene with minimal fitness.
#'
#' @details     The fitness of survival of the gene with
#'              minimal fitness is set to \code{0.01}.
#'              See equation (7.45) Andreas Geyer-Schulz (1997), p. 205.
#'
#' @references   Andreas Geyer-Schulz (1997):
#'               \emph{Fuzzy Rule-Based Expert Systems and Genetic Machine Learning},
#'               Physica, Heidelberg.
#'
#'              Note: This contains a dynamic scaling function.
#'
#' @param \code{fit} the vector of fitness values of the population.
#'
#' @return the index of the selected gene.
#'
#' @family {gene layer}
#' @seealso ReplicateGene() uses SelectGene().
#'
#' @examples
#' fit<-sample(10, 15, replace=TRUE)
#' SelectGene(fit) 
#' SelectGene(fit) 
#' @export
SelectGene<-function(fit)
{
eps<-0.01
1+sum(1*((cumsum(eps+(fit-min(fit)))/((length(fit)*eps)+sum(fit-min(fit))))<runif(1)))
}

# 
# Nice functional code, but slow!
# 
# flip<-function(x,r)
# {       if(runif(1)<r) {1*!(x==1)} else x }
# 
# MutateGene<-function(gene, r)
# { 	unlist(lapply(gene, flip,r=r)) }

#' Mutate a gene.
#'
#' @description \code{MutateGene} mutates a binary gene.
#'               The per bit mutation rate is given by MutationRate().
#'
#' @param \code{gene} a binary gene.
#' @param \code{r}    the mutation rate. 
#'
#' @return a binary gene
#'
#' @family {gene layer}
#' @seealso ReplicateGene() uses MutateGene().
#'
#' @examples
#' gene1<-InitGene(Parabola2D$genelength())
#' GeneMap(gene1, Parabola2D)
#' gene<-MutateGene(gene1, 0.01)
#' gene
#' gene1
#' GeneMap(gene, Parabola2D)
#' gene<-MutateGene(gene1, 0.5)
#' GeneMap(gene, Parabola2D)
#' @export
MutateGene<-function(gene, r)
{
	1*xor(gene,runif(length(gene), 0, 1)<r)
}

#' Crossover of 2 genes.
#'
#' @description \code{CrossGene} randomly determines a cut point.
#'
#' @details     It combines the bits before the cut point of first gene
#'              with the bits after the cut point from the second gene (kid 1).
#'              It combines the bits before the cut point of second gene
#'              with the bits after the cut point from the first gene (kid 2).
#'
#' @param \code{g1} a binary gene.
#' @param \code{g2} a binary gene.
#'
#' @return a list of 2 binary genes.
#'
#' @family {gene layer}
#' @seealso ReplicateGene() uses CrossGene().
#'
#' @examples
#' gene1<-InitGene(Parabola2D$genelength())
#' gene2<-InitGene(Parabola2D$genelength())
#' GeneMap(gene1, Parabola2D)
#' GeneMap(gene2, Parabola2D)
#' newgenes<-CrossGene(gene1, gene2)
#' GeneMap(newgenes[[1]], Parabola2D)
#' GeneMap(newgenes[[2]], Parabola2D)
#' as.data.frame(do.call(rbind, c(list(gene1, gene2), newgenes)))
#' @export
CrossGene<-function(g1, g2)
{
    cut<-sample(1:length(g1), 1)
    return(list( c(head(g1,cut), tail(g2, length(g2)-cut)),
    c(head(g2,cut), tail(g1, length(g2)-cut))))
}

#' Replicates a gene.
#'
#' @description \code{ReplicateGene} replicates a gene. Replication
#'              is the reproduction function which uses crossover and
#'              mutation.
#'
#' @details    The control flow is as follows:
#'              \itemize{
#'              \item A gene is selected from the population.
#'              If the crossover operation should be applied
#'              with a probability of \code{crossrate} then
#'              \itemize{
#'                \item A mating gene is selected from the population.
#'                \item Perform the crossover operation.
#'                \item Apply mutation with a probability of \code{mutrate}.
#'                \item Return a list with both genes.
#'                            }
#'                \item Apply mutation with a probability of \code{mutrate}.
#'                \item Return a list with a single gene.
#'              }
#'
#' @param \code{pop} a population of binary genes.
#' @param \code{fit} its fitness vector.
#' @param \code{crossrate} probability of crossover.
#' @param \code{mutrate} probability of mutation of a bit of a gene.
#'
#' @return A list of either 1 or 2 binary genes.
#'
#' @family {gene layer}
#' @seealso Uses SelectGene(), MutateGene(), and CrossGene().
#'
#' @examples
#' pop10<-lapply(rep(0,10), function(x) InitGene(Parabola2D$genelength()))
#' fit10<-unlist(lapply(pop10, EvalGene, penv=Parabola2D))
#' newgenes<-ReplicateGene(pop10, fit10, 0.5, 0.1)
#' GeneMap(newgenes[[1]], Parabola2D)
#' newgenes<-ReplicateGene(pop10, fit10, 0.5, 0.1)
#' GeneMap(newgenes[[1]], Parabola2D)
#' newgenes<-ReplicateGene(pop10, fit10, 0.5, 0.1)
#' GeneMap(newgenes[[1]], Parabola2D)
#' @export
ReplicateGene<- function(pop, fit, crossrate, mutrate)
{
    g<-pop[[SelectGene(fit)]]
    if (runif(1)<crossrate) 
    {
     return(lapply(CrossGene(g, pop[[SelectGene(fit)]]),MutateGene, r=mutrate)) 
    } else
    {
       return(list(MutateGene(g, mutrate)))
    }
}

#' Computes the next population of genes.
#'
#' @description \code{NextPopulation} builds the next population by repeatedly
#'                calling \code{ReplicateGene}.
#'
#' @param \code{pop} a population of genes.
#' @param \code{fit} its fitness vector.
#' @param \code{crossrate} probability of crossover.
#' @param \code{mutrate} probability of mutation of a bit of a gene.
#'
#' @return A list of genes.
#'
#' @family {population layer}
#' @seealso ReplicateGene() is used by NextPopulation().
#'
#' @examples
#' pop10<-InitPopulation(Parabola2D$genelength(), 10)
#' fit<-EvalPopulation(pop10, Parabola2D)
#' newpop<-NextPopulation(pop10, fit, 0.4, 0.1)
#' pop10
#' fit
#' newpop
#' @export
NextPopulation<-function(pop, fit, crossrate, mutrate)
{
	newpop<-list()
        while(length(newpop)<length(pop))
	{
	newpop<-append(newpop, ReplicateGene(pop, fit, crossrate, mutrate))
	}
	return(head(newpop,length(pop)))
}

#' Provide elementary summary statistics of the fitness of the population.
#'
#' @description \code{SummaryPopulation} reports
#'              on the fitness and the value of the best solution
#'              in the population.
#'
#' @param \code{pop} a population of derivation trees.
#' @param \code{fit} the vector of fitness values of \code{pop}.
#' @param \code{iter} the generation. Default: 0.
#'
#' @return the number 0.
#'
#' @family {population layer}
#' @seealso RunSGA() uses SummaryPopulation().
#'
#' @examples
#' pop10<-InitPopulation(Parabola2D$genelength(), 10)
#' fit<-EvalPopulation(pop10, Parabola2D)
#' rc<-SummaryPopulation(Parabola2D, pop10, fit, iter=12)
#'
#' @export
SummaryPopulation<-function(penv, pop, fit, iter=0)
{
	best<-(1:length(fit))[max(fit)==fit]
	cat("Best: ", best, 
	    " Typeof: ", typeof(best), 
	    "Length: ", length(best), "\n")
	parms<- GeneMap(pop[[head(best,1)]],penv)
        if (iter==0) 
	{
	cat("Best solution:\n")
	} else
	{
	cat("Best Solution in Iteration:", iter, "\n")
	}
        cat("Fitness: Max: ", max(fit), " Mean: ", mean(fit), "\n")
	cat("Parameters: ", parms, "\n") 
	cat("Function Value: ", penv$f(parms), "\n") 
	return(0)
}

#' Run a simple genetic algorithm with binary genes for a problem environment
#' which contains a function to optimize.
#'
#' @description \code{RunSGA} runs a simple genetic algorithm.
#'
#' Layers (in top-down direction)
#'
#' \enumerate{
#'   \item Top-level main programs
#'         RunSGA
#'   \item Population level operations - independent of representation
#'         InitPopulation, EvalPopulation,
#'         BestGeneInPopulation,
#'         NextPopulation, SummaryPopulation
#'   \item Gene level operations - gene representation dependent.
#'         Binary representation 
#'         InitGene, MapGene, EvalGene,
#'         MutateGene, CrossGene, SelectGene, ReplicateGene.
#'         }
#'
#' @param \code{penv} Problem environment.
#' @param \code{generations} Number of generations. Default: 20.
#' @param \code{popsize} Population size. Default: 100.
#' @param \code{crossrate} the crossover rate. Default: 0.20.
#' @param \code{mutrate} the mutation rate. Default: 0.005.
#'
#' @return a list of of fitness vectors.
#'
#' @family {top-level main program layer}
#' @seealso RunSGA() uses InitPopulation(), EvalPopulation(), 
#'          NextPopulation(), and SummaryPopulation(). 
#'
#' @examples
#' a<-RunSGA(Parabola2D)
#' b<-RunSGA(Parabola2D, generations=100)
#' e<-RunSGA(Parabola2D, 100, 50, 0.15, 0.05)
#'
#' @export
RunSGA<-function(penv, generations=20, popsize=100, 
		 crossrate=0.2, mutrate=0.005)
{ maxfit<-vector()	
pop<-InitPopulation(penv$genelength(), popsize)
fit<-EvalPopulation(pop, penv)
maxfit<-append(maxfit,max(fit))
for(i in 1:generations)
{ rc<-SummaryPopulation(penv, pop, fit, i)
	pop<-NextPopulation(pop, fit, crossrate, mutrate)
	fit<-EvalPopulation(pop, penv)
        maxfit<-append(maxfit,max(fit))
}
	rc<-SummaryPopulation(penv, pop, fit)
#        print(maxfit)
	return(maxfit)
}

# Examples of calling the simple GA:
# a<-RunSGA(P4dParabola, 100, 10, 0.2, 0.01)
# a<-RunSGA(ProblemEnv)
# system.time(a<-RunSGA(ProblemEnv))
# plot(a)


#
# The code for multicore execution is not exported.
#

library(parallel)

mcEvalPopulation<-function(pop, penv)
{
	unlist(mclapply(pop, EvalGene, penv=penv, mc.cores=detectCores()))
}


mcRunSGA<-function(penv, generations=20, popsize=100,
                 crossrate=0.2, mutrate=0.005)
{ maxfit<-vector("integer")
pop<-InitPopulation(penv$genelength(), popsize)
fit<-mcEvalPopulation(pop, penv)
maxfit<-append(maxfit,max(fit))
for(i in 1:generations)
{ rc<-SummaryPopulation(penv, pop, fit, i)
        pop<-NextPopulation(pop, fit, crossrate, mutrate)
        fit<-mcEvalPopulation(pop, penv)
        maxfit<-append(maxfit,max(fit))
}
        rc<-SummaryPopulation(penv, pop, fit)
#        print(maxfit)
        return(maxfit)
}




#
# (c) 2021 Andreas Geyer-Schulz
#          Simple Genetic Algorithm in R. V 0.1
#          Problem environments for simple binary or real coded GAs 
#          Package: envDeJongFunctions 
#

#' List of functions for problem environment DeJongF1b
#'
#' @description This list of functions sets up the problem environment 
#'              for De Jong's function F1 which is a 3-dimensional
#'              quadratic parabola. 
#'
#' @details The list of functions contains all functions needed for 
#'          the simple genetic algorithm with binary coded genes 
#'          of package \code{sga}.
#'
#' @return A list of functions named \code{DeJongF1b}
#'         from which we can dispatch the following functions:
#'         \itemize{
#'         \item \code{DeJongF1b$name()} returns the name of the problem 
#'               environment.
#'         \item \code{DeJongF1b$bitlength()} returns a vector whose 
#'               elements specify the bit length of each parameter.
#'         \item \code{DeJongF1b$genelength()} returns the 
#'               length of the gene.
#'         \item \code{DeJongF1b$lb()}
#'               the vector of lower bounds of parameters. 
#'         \item \code{DeJongF1b$ub()}
#'               the vector of upper bounds of parameters. 
#'         \item \code{DeJongF1b$f(parm)}
#'               returns the function value f at point parm.
#'         }
#' 
#' @family {problem environments}
#' @seealso [DeJongF1], [DeJongF1a1]
#'
#' @examples
#' DeJongF1b$name() 
#' DeJongF1b$bitlength()
#' DeJongF1b$genelength()
#' DeJongF1b$lb()
#' DeJongF1b$ub()
#' DeJongF1b$f(c(2.2, 1.0, -3.5))
#' @export
DeJongF1b<-list()
DeJongF1b<-c(DeJongF1b, name=function() {"DeJongF1b"})
DeJongF1b<-c(DeJongF1b, bitlength=function() {c(64, 64, 64)})
DeJongF1b<-c(DeJongF1b, genelength=function() {sum(DeJongF1b$bitlength())})
DeJongF1b<-c(DeJongF1b, lb=function() {c(-5.12, -5.12, -5.12)})
DeJongF1b<-c(DeJongF1b, ub=function() {c(5.12, 5.12, 5.12)})
DeJongF1b<-c(DeJongF1b, f=function(parm) {sum(parm^{2})})

#
# DeJongF1 = DJongF1b + describe + solution
#

#' List of functions for problem environment DeJongF1
#'
#' @description This list of functions sets up the problem environment 
#'              for De Jong's function F1 which is a 3-dimensional
#'              quadratic parabola.
#'      F1 is a 3-dimensional parabola with spherical constant-cost contours. 
#' It is a continuous, convex, unimodal, low-dimensional quadratic function. 
#'
#'
#' @details It extends the minimal interface of 
#'          \code{DeJongF1b} with a description
#'          and with known solutions (for validation).
#'
#' @return A list of functions named \code{DeJongF1}
#'         from which we can dispatch the following functions:
#'         \itemize{
#'         \item \code{DeJongF1$name()} returns the name of the problem 
#'               environment.
#'         \item \code{DeJongF1$bitlength()} returns a vector whose 
#'               elements specify the bit length of each parameter.
#'         \item \code{DeJongF1$genelength()} returns the 
#'               length of the gene.
#'         \item \code{DeJongF1$lb()}
#'               the vector of lower bounds of parameters. 
#'         \item \code{DeJongF1$ub()}
#'               the vector of upper bounds of parameters. 
#'         \item \code{DeJongF1$f(parm)}
#'               returns the function value f at point parm.
#'         \item \code{DeJongF1$describe()}
#'               outputs a short description of the mathematical 
#'               properties of the function and of a reference 
#'               to the origin of the function.
#'         \item \code{DeJongF1$solution()}
#'               returns a named list with 
#'               the values and parameters of known minima and 
#'               and maxima of the (boxed) function.
#'         }
#'
#' @family {problem environments}
#' @seealso [DeJongF1b], [DeJongF1a1]
#'
#' @examples
#' DeJongF1$name() 
#' DeJongF1$bitlength()
#' DeJongF1$genelength()
#' DeJongF1$lb()
#' DeJongF1$ub()
#' DeJongF1$f(c(2.2, 1.0, -3.5))
#' DeJongF1$describe()
#' DeJongF1$solution()
#' @export
DeJongF1<-DeJongF1b
DeJongF1$name<-function() {"DeJongF1"}
DeJongF1$genelength<-function() {sum(DeJongF1$bitlength())}
DeJongF1<-c(DeJongF1, describe=function() {
cat("See", "\n")
cat("De Jong (1975) ")
cat("An Analysis of the Behavior of a Class of Genetic Adaptive Systems.", "\n")
cat("PhD thesis, Michigan, Ann Arbor, pp. 196-199", "\n\n")
cat("F1 is a 3-dimensional parabola with spherical constant-cost contours.", "\n")
cat("It is a continuous, convex, unimodal, low-dimensional quadratic function.", "\n")
})
DeJongF1<-c(DeJongF1, solution=function() {
                 s<-list()
                 s[["minimum"]]<-0
                 s[["minpoints"]]<-list(list(c(0, 0, 0)))
                 s[["maximum"]]<-78.6432
                 s[["maxpoints"]]<-list( c(5.12, 5.12, 5.12),
                                      c(5.12, 5.12, -5.12),
                                      c(5.12, -5.12, 5.12),
                                      c(5.12, -5.12, -5.12),
                                      c(-5.12, 5.12, 5.12),
                                      c(-5.12, 5.12, -5.12),
                                      c(-5.12, -5.12, -5.12),
                                      c(-5.12, -5.12, -5.12))
                 return(s)
                   })




#
# A 5-D parabola. Local functions.
#

#' Function factory for the list of functions for problem environment DeJongF1a1
#'
#' @description A function factory for the list of functions 
#'              of the problem environment of a 5-dimensional quadratic parabola.
#'              The list of functions is specified in a closure in three steps:
#'              \enumerate{
#'              \item We specify the local functions 
#'                    name(), bitlength(), genelength(), lb(), ub(), f(parm) 
#'              \item and the function list \code{DeJongF1a1}
#'                    is created as a named list
#'                    with the local functions as elements.
#'                    Please read the source file \code{DeJongF1.R}.
#'              \item We return the function list.
#'              }
#'
#' @return A list of functions with the functions
#'         \code{name()}, \code{bitlength()}, 
#'         \code{genelength()}, \code{lb()}, \code{ub()}, \code{f(parm)}
#'
#' @family {problem environments}
#' @seealso [DeJongF1], [DeJongF1b]
#'
#' @examples
#' DeJongF1a1<-DeJongF1a1Factory()
#' DeJongF1a1$name() 
#' DeJongF1a1$bitlength()
#' DeJongF1a1$genelength()
#' DeJongF1a1$lb()
#' DeJongF1a1$ub()
#' DeJongF1a1$f(c(2.2, 1.0, -3.5, -4.2, -2.9))
#' @export
DeJongF1a1Factory<-function() {
name<-function() {"DeJongF1a1"}
bitlength<-function() {rep(64, 5)}
genelength<-function() {sum(bitlength())}
lb<-function() {rep(-5.12, 5)}
ub<-function() {rep(5.12, 5)}
f<-function(parm) {sum(parm^{2})}
DeJongF1a1<-list(
name=name,
bitlength=bitlength,
genelength=function() {sum(bitlength())},
lb=lb,
ub=ub,
f=f)
return(DeJongF1a1)
}

#
# End of DeJongF1
#



#  Problem Environment: Delayed Parabola.
# (c) 2017 Andreas Geyer-Schulz

#' Function list for a 2-dimensional quadratic parabola with delayed execution.
#'
#' @description This list of functions sets up the problem environment
#'              for a 2-dimensional
#'              quadratic parabola with a delayed execution of 0.1s.
#'
#' @details The list of functions contains examples of all functions 
#'          which form the interface of a problem environment to
#'          the simple genetic algorithm with binary coded genes
#'          of package \code{sga}.
#'
#' @return A function list named \code{DelayedP}
#'         from which we can dispatch the following functions:
#'         \itemize{
#'         \item \code{DelayedP$name()} returns the name of the problem
#'               environment.
#'         \item \code{DelayedP$bitlength()} returns a vector whose
#'               elements specify the bit length of each parameter.
#'         \item \code{DelayedP$genelength()} returns the
#'               length of the gene.
#'         \item \code{DelayedP$lb()}
#'               the vector of lower bounds of parameters.
#'         \item \code{DelayedP$ub()}
#'               the vector of upper bounds of parameters.
#'         \item \code{DelayedP$f(parm)}
#'               returns the function value f at point parm.
#'         }
#' @family {problem environments}
#' @seealso [Parabola2D], [Parabola32D]
#'
#' @examples
#' DelayedP$f(c(2.2, 1.0))
#' @export
DelayedP<-list()
DelayedP<-c(DelayedP, bitlength=function() {c(20, 20)})
DelayedP<-c(DelayedP, genelength=function() {sum(DelayedP$bitlength())})
DelayedP<-c(DelayedP, lb=function() {c(-4.5, -4.5)})
DelayedP<-c(DelayedP, ub=function() {c(4.5, 4.5)})
DelayedP<-c(DelayedP, f=function(parm) {
               Sys.sleep(0.1)
               sum(parm^{2}) })

#
# End of DelayedP
#



# Problem Environment PMADGlobalXY
# (c) 2023 A. Geyer-Schulz

#' List of functions for problem environment PMADGlobalXY
#'
#' @description A list of functions for setting up a 
#'              problem environment for solving 
#'              a L1-regression problem  by a simple genetic algorithm.
#'
#' @details The solver assumes that the 
#'          global variable \code{Y} contains values 
#'          of the dependent variable and
#'          the global variable \code{X} the design matrix 
#'          of the regression problem. The global variables 
#'          must exist before calling the genetic algorithm.
#'
#' @return The list of functions \code{PMADGlobalXY} with the functions
#'         \code{name()}, \code{bitlength()},
#'         \code{genelength()}, \code{lb()}, \code{ub()}, \code{f(parm)}
#'
#' @family {problem environments}
#' @seealso [POLSGlobalXY]
#'
#' @examples
#' lm(rating~ ., data=attitude)
#' Y<-attitude[,1]
#' X<-cbind(1, as.matrix(attitude[,seq(2,(ncol(attitude)-1))]))
#' b<-c((5.0+sample(10, 1)), rnorm(5))
#' PMADGlobalXY$f(b)
#' PMADGlobalXY$f(b)
#' RunSGA(PMADGlobalXY)
#'@export
PMADGlobalXY<-list()
PMADGlobalXY<-c(PMADGlobalXY, bitlength=function() {rep(32,ncol(X))})
PMADGlobalXY<-c(PMADGlobalXY, genelength=function() {sum(PMADGlobalXY$bitlength())})
PMADGlobalXY<-c(PMADGlobalXY, lb=function() {c(5, rep(-1, (ncol(X)-1)))})
PMADGlobalXY<-c(PMADGlobalXY, ub=function() {c(15,rep(1, (ncol(X)-1)))})
PMADGlobalXY<-c(PMADGlobalXY, f=function(b) {return(-sum(abs(Y-X%*%b)))})

cat("Loaded Problem Environment PMADGlobalXY\n")
cat("Usage: PMADGlobalXY$f(parametervector) \n")

#
# End of PMADGlobalXY
#



# Problem Environment POLSGlobalXY
# (c) 2023 A. Geyer-Schulz

#' List of functions for problem environment POLSGlobalXY
#'
#' @description A list of functions for setting 
#'              up a problem environment for solving 
#'              an ordinary least squares regression problem 
#'              by a simple genetic algorithm.
#'
#' @details The solver assumes that the global variable \code{Y} 
#'          contains values of the dependent variable and
#'          the global variable \code{X} the design matrix 
#'          of a regression problem. 
#'
#' @return The list of functions \code{POLSGlobalXY} with the functions
#'         \code{name()}, \code{bitlength()},
#'         \code{genelength()}, \code{lb()}, \code{ub()}, \code{f(parm)}
#'
#' @family {problem environments}
#' @seealso [PMADGlobalXY]
#'
#' @examples
#' lm(rating~ ., data=attitude)
#' Y<-attitude[,1]
#' X<-cbind(1, as.matrix(attitude[,seq(2,(ncol(attitude)-1))]))
#' b<-c((5.0+sample(10, 1)), rnorm(5))
#' POLSGlobalXY$f(b)
#' POLSGlobalXY$f(b)
#' RunSGA(POLSGlobal)
#'@export
POLSGlobalXY<-list()
POLSGlobalXY<-c(POLSGlobalXY, bitlength=function() {rep(32,ncol(X))})
POLSGlobalXY<-c(POLSGlobalXY, genelength=function() {sum(POLSGlobalXY$bitlength())})
POLSGlobalXY<-c(POLSGlobalXY, lb=function() {c(5, rep(-1, (ncol(X)-1)))})
POLSGlobalXY<-c(POLSGlobalXY, ub=function() {c(15,rep(1, (ncol(X)-1)))})
POLSGlobalXY<-c(POLSGlobalXY, f=function(b) {return(-sum((Y-X%*%b)^2))})

cat("Loaded Problem Environment POLSGlobalXY\n")
cat("Usage: POLSGlobalXY$f(parametervector) \n")

#
# End of POLSGlobalXY.R
#



# Problem Environment Parabola2D
# (c) 2021 A. Geyer-Schulz

#' List of functions for a 2-dimensional quadratic parabola.
#'
#' @description This list of functions sets up the problem environment
#'              for a 2-dimensional
#'              quadratic parabola.
#'
#' @details The list of functions contains all functions needed for
#'          the simple genetic algorithm with binary coded genes
#'          of package \code{sga}.
#'
#' @return A list of functions named \code{Parabola2D}
#'         from which we can dispatch the following functions:
#'         \itemize{
#'         \item \code{DeJongF1b$name()} returns the name of the problem
#'               environment.
#'         \item \code{DeJongF1b$bitlength()} returns a vector whose
#'               elements specify the bit length of each parameter.
#'         \item \code{DeJongF1b$genelength()} returns the
#'               length of the gene.
#'         \item \code{DeJongF1b$lb()}
#'               the vector of lower bounds of parameters.
#'         \item \code{DeJongF1b$ub()}
#'               the vector of upper bounds of parameters.
#'         \item \code{DeJongF1b$f(parm)}
#'               returns the function value f at point parm.
#'         }
#'
#' @family {problem environments}
#' @seealso [DelayedP], [Parabola32D], [DeJongF1]
#'
#' @examples
#' Parabola2D$name()
#' Parabola2D$bitlength()
#' Parabola2D$genelength()
#' Parabola2D$lb()
#' Parabola2D$ub()
#' Parabola2D$f(c(2.2, 1.0, -3.5))
#' @export
Parabola2D<-list()
Parabola2D<-c(Parabola2D, name=function() {"Parabola2D"})
Parabola2D<-c(Parabola2D, bitlength=function() {c(20, 20)})
Parabola2D<-c(Parabola2D, genelength=function() {sum(Parabola2D$bitlength())})
Parabola2D<-c(Parabola2D, lb=function() {c(-4.5, -4.5)})
Parabola2D<-c(Parabola2D, ub=function() {c(4.5, 4.5)})
Parabola2D<-c(Parabola2D, f=function(parm) {parm[1]^{2}+parm[2]^{2}})

cat("Loaded Problem Environment Parabola2D\n")
cat("Usage: Parabola2D$f(parametervector) \n")
cat("Parabola2D$f(c(3.5, 3.0))\n")

#
# End of Parabola2D
#



# Problem Environment Parabola32D
# (c) 2023 A. Geyer-Schulz


#' List of functions of the problem environment of a 32-dimensional quadratic parabola.
#'
#' @description This list of functions sets up the problem environment
#'              for a 32-dimensional
#'              quadratic parabola.
#'
#' @details The list of functions contains all functions needed for
#'          the simple genetic algorithm with binary coded genes
#'          of package \code{sga}.
#'
#' @return A list of functions named \code{Parabola32D}
#'         from which we can dispatch the following functions:
#'         \itemize{
#'         \item \code{Parabola32D$name()} returns the name of the problem
#'               environment.
#'         \item \code{Parabola32D$bitlength()} returns a vector whose
#'               elements specify the bit length of each parameter.
#'         \item \code{Parabola32D$genelength()} returns the
#'               length of the gene.
#'         \item \code{Parabola32D$lb()}
#'               the vector of lower bounds of parameters.
#'         \item \code{Parabola32D$ub()}
#'               the vector of upper bounds of parameters.
#'         \item \code{Parabola32D$f(parm)}
#'               returns the function value f at point parm.
#'         }
#'
#' @family {problem environments}
#' @seealso
#'
#' @examples
#' Parabola32D$name()
#' Parabola32D$bitlength()
#' Parabola32D$genelength()
#' Parabola32D$lb()
#' Parabola32D$ub()
#' Parabola32D$f(c(2.2, 1.0, -3.5))
#' @export
Parabola32D<-list()
Parabola32D<-c(Parabola32D, name=function() {"Parabola32D"})
Parabola32D<-c(Parabola32D, bitlength=function() {rep(50,32)})
Parabola32D<-c(Parabola32D, genelength=function() {sum(Parabola32D$bitlength())})
Parabola32D<-c(Parabola32D, lb=function() {rep(-4.5, 32)})
Parabola32D<-c(Parabola32D, ub=function() {rep(4.5, 32)})
Parabola32D<-c(Parabola32D, f=function(parm) {sum(parm^{2})})

cat("Loaded Problem Environment Parabola32D\n")
cat("Usage: Parabola32D$f(parametervector) \n")
cat("Parabola32D$f(c(3.5, 3.0))\n")

#
# End of Parabola2D
#

# plot a 2D-parabola on a pdf-file
# (c) 2023 A. Geyer-Schulz

#' plot a 2D-parabola on a pdf-file
#' 
#' @examples
#' plotParabola2D()
#' # View the pdf-file Parabola.pdf 
#' # E.g.
#' # system("evince Parabola.pdf")
#' @export
plotParabola2D<-function()
{
parabola<-function(x, y) {x^{2}+y^{2}}

y<-x<-seq(-4.5, 4.5, 0.1)

z<-outer(x, y, parabola)

persp(x, y, z)

pdf("Parabola.pdf")
persp(x, y, z)
dev.off()
}

#
# End of ParabolaPlot.R
#

