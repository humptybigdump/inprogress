import plotly.graph_objects as go
# Generate sample data
np.random.seed(42)
x = np.linspace(0, 10, 100)
y = 2 * x**3 * x**2 + 4 * x + 7 + np.random.normal(0, 5, size=100)
# Generate polynomial fits for degrees 1 to 4 manually
polynomial_lines = {}
for degree in range(1, 5):
    coeffs = np.polyfit(x, y, degree)  # Fit polynomial of given degree
    y_pred = np.polyval(coeffs, x)     # Evaluate polynomial
    polynomial_lines[degree] = y_pred
# Create base scatter plot
fig = go.Figure()
# Add the original data points
fig.add_trace(go.Scatter(x=x, y=y, mode='markers', name='Data', marker=dict(size=6, color='darkblue')))
# Add polynomial fits as traces
for degree, y_pred in polynomial_lines.items():
    fig.add_trace(go.Scatter(x=x, y=y_pred, mode='lines', name=f'Degree {degree}', visible=(degree == 1)))
# Create slider steps
steps = []
for i, degree in enumerate(range(1, 5)):
    step = dict(
        method="restyle",
        args=[{"visible": [True if j == i+1 or j == 0 else False for j in range(len(fig.data))]}],
        label=f"Degree {degree}"
    )
    steps.append(step)
# Add the slider
fig.update_layout(
    title="Polynomial Regression with Slider",
    sliders=[{
        "active": 0,"steps": steps,
        "currentvalue": {"prefix": "Polynomial Degree: ", "font": {"size": 16}}
    }],
)
fig.show()
