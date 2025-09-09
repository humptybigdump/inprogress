import plotly.express as px
import pandas as pd

# Create DataFrame with city coordinates and some extra details
df_geo = pd.DataFrame({
    'City': ['Berlin', 'Rome', 'Paris', 'Tokyo', 'New York', 'Sydney'],
    'lat': [52.5200, 41.9028, 48.8566, 35.6762, 40.7128, -33.8688],
    'lon': [13.4050, 12.4964, 2.3522, 139.6503, -74.0060, 151.2093],
    'Population': [3.6, 2.8, 2.1, 14.0, 8.4, 5.3],
    'Country': ['Germany', 'Italy', 'France', 'Japan', 'USA', 'Australia'],
    'Continent': ['Europe', 'Europe', 'Europe', 'Asia', 'North America', 'Australia']
})

# Generate an interactive scatter map with enhanced visuals
fig = px.scatter_geo(
    df_geo,
    lat='lat', lon='lon',
    hover_name='City',
    hover_data={'lat': False, 'lon': False, 'Population': True, 'Country': True},
    size='Population',
    projection='orthographic',
    color='City',
    title='Globe Visualization of Cities',
)

# Update layout for a cleaner and fancier appearance
fig.update_layout(
    geo=dict(
        showland=True,
        landcolor='lightgrey',
        showocean=True,
        oceancolor='lightblue',
        showcountries=True,
        countrycolor='white',
        showlakes=True,
        lakecolor='skyblue',
    ),
    margin=dict(l=0, r=0, t=80, b=0),
    title_font=dict(size=22),

)

# Add dropdown menu for rotating the globe to different continents
fig.update_layout(
    updatemenus=[
        {
            'buttons': [
                {
                    'label': 'Global',
                    'method': 'relayout',
                    'args': ['geo.projection.rotation', dict(lon=0, lat=0)]
                },
                {
                    'label': 'Europe',
                    'method': 'relayout',
                    'args': ['geo.projection.rotation', dict(lon=10, lat=50)]
                },
                {
                    'label': 'Asia',
                    'method': 'relayout',
                    'args': ['geo.projection.rotation', dict(lon=100, lat=35)]
                },
                {
                    'label': 'North America',
                    'method': 'relayout',
                    'args': ['geo.projection.rotation', dict(lon=-100, lat=40)]
                },
                {
                    'label': 'Australia',
                    'method': 'relayout',
                    'args': ['geo.projection.rotation', dict(lon=135, lat=-25)]
                }
            ],
            'direction': 'down',
            'showactive': True,
            'x': 0.1,
            'xanchor': 'left',
            'y': 1.05,
            'yanchor': 'top',
            'bgcolor': 'lightgrey',
            'bordercolor': 'black',
        }
    ]
)

# Display the map
fig.show()
