import plotly.express as px
# Sample data for 2D scatter
df_2d = pd.DataFrame({
    'x': [1, 2, 3, 4, 5],
    'y': [10, 12, 9, 14, 11],
    'category': ['A', 'A', 'B', 'B', 'A']
})
# Create a minimalistic 2D scatter plot
fig = px.scatter(
    df_2d,
    x='x', y='y',
    color='category',
    color_discrete_sequence=px.colors.qualitative.Set2,
    title='2D Scatter Plot',
    template='simple_white'
)
# Update layout for a cleaner look
fig.update_layout(
    xaxis_title='X-Axis',
    yaxis_title='Y-Axis',
    margin=dict(l=60, r=40, t=60, b=40),
    font=dict(family='Helvetica', size=14, color='black'),
    legend_title_text='Category',
    legend=dict(yanchor="top", y=1, xanchor="left", x=0.01),
)
# Adjust marker settings for clarity
fig.update_traces(marker=dict(size=10, line=dict(width=2, color='black')), 
                  selector=dict(mode='markers'))
fig.show()
