import statsmodels.api as sm
# ...
# setup model with given formula and data
model = sm.OLS.from_formula(formula, data=data)
# fit the model
results = model.fit()
# print summary table as LaTeX code
print(results.summary().as_latex())
# another option that allows you to combine multiple specifications
# by adding more fitted models to the list of results
print(summary_col([results],stars=True,float_format='%0.2f').as_latex())

