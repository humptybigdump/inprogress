import plotly.express as px

# Data
data = {'Category': ['A', 'B', 'C', 'D'], 'Values': [40, 30, 20, 10]}

# Create Pie Chart with Enhanced Styling
fig = px.pie(
    data, values='Values', names='Category', 
    title='Category Distribution',
    color_discrete_sequence=px.colors.sequential.Viridis,  # Nice modern color palette
    hole=0.4  # Turns it into a donut chart for a cleaner look
)

# Update layout for better appearance
fig.update_layout(
    title_font_size=18, 
    title_font_family="Arial",
    showlegend=True
)

# Show the Chart
fig.show()
