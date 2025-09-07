
## Tools
# julia, via juliaup 
# Visual Sudio Code & Julia Language Support Extension
# - Useful Shortcuts:
#   - Alt-D : "Julia: Send current line or selection to REPL"
#   - Alt-E : "Julia: Execute Code Cell in REPL"
#   - Alt-S : "Julia: Execute File in REPL"

## Julia Dependencies
# ] activate .  # use local environment to install packages
# ] add TypedPolynomials, JuMP, Clarabel   # install packages

using Printf: @printf
using LinearAlgebra: rank, eigvals
using TypedPolynomials: Polynomial, Monomial, Term, Variable, monomials, coefficients, degree, @polyvar
using JuMP
import Clarabel


"substitute individual monomials in polynomial
    - p  : polynomial
    - m  : vector of monomials, corresponding to s
    - s  : vector of substitutes"
function polysub(p::Polynomial, m::Array{<:Monomial}, s::Array)
    T = indexin(monomials(p), m)
    coefficients(p)' * s[T]
end
function polysub(p::Union{<:Monomial,<:Variable,<:Term}, m::Array{<:Monomial}, s::Array)
    T = indexin([p], m)
    s[first(T)]
end
function polysub(p::Number, m::Array{<:Monomial}, s::Array)
    T = indexin(1, m)
    p * s[first(T)]
end
function polysub(p::Union{<:Tuple,<:Array}, m::Array{<:Monomial}, s::Array)
    map(p -> polysub(p,m,s), p)
end
"polynomial to symmetric coefficient matrix
    - p : polynomial
    - m : array of monomials"
function poly2coeff(p::Polynomial, m::Array{<:Monomial})
    C = zeros(size(m))
    for pt in terms(p)
        ind = monomial(pt) .== m
        C[ind] .+= coefficients(pt) / count(ind)
    end
    return C
end
function poly2coeff(p::Union{Variable,Monomial,Term}, m::Array{<:Monomial})
    poly2coeff(polynomial(p), m)
end
function poly2coeff(p::Number, m::Array{<:Monomial})
    poly2coeff(p*constant_monomial(m[1]), m)
end


## Rosenbrock 
vars = @polyvar x y                          # quasi-symbolic variables (only for polynomial computations)
a, b = 2, 100                                # Rosenbrock Parameters
p = (a-x)^2 + b*(y-x^2)^2                    # Rosenbrock function
N = 2                                        # 2N ≥ degree(p)
y1N = monomials(vars, 0:1*N)                 # vector of monomials
y2N = monomials(vars, 0:2*N)
yw1 = monomials(vars, 0:N-1)
model = Model(Clarabel.Optimizer)            # SDP solver, using JuMP interface. Alternative: CSDP, Mosek, ...
@variable(model, yo[eachindex(y2N)])         # define quasi-symbolic optimization variables as vector yo[i]
# display(hcat(y2N, yo))                     # view correspondences between poly and optim variables
@objective(model, Min, polysub(p, y2N, yo))  # define objective function; replace polyvars with optimization vars
Xo = polysub(y1N*y1N', y2N, yo)              # X matrix, replace polynomial variables with optimization variables
@constraint(model, Xo in PSDCone())          # constraint: X positive definite
@constraint(model, yo[1]==1)                 # constraint: X[1,1] = 1
ga = 100^2 - sum(monomials(vars, 1).^2)      # constraint: x²+y² ≤ 100²: since feasible domain is non-compact ... 
@constraint(model, polysub(ga*yw1*yw1', y2N, yo) in PSDCone()) # ... as PSD constraint
@constraint(model, polysub(ga, y2N, yo) ≥ 0) # ... as "normal" constraint (alone not rank-tight)
optimize!(model)                             # solve semidefinite programming problem
# display(value.(Xo))                        # display X*
# display(eigvals(value.(Xo)))               # inspect eigenvalues for rank of X
xOpt = polysub(vars, y2N, value.(yo))        # extract solution
@printf("status = %s,   rank = %u \n", termination_status(model), rank(value.(Xo), rtol=1e-4))
@printf("p* = %f,    p(xOpt) = %f  \n", objective_value(model), p(vars => xOpt)) # true: 0
@printf("x* = (%f, %f) \n", xOpt...)         # true: (a, a^2)


