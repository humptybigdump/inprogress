import plotly.graph_objects as go
# --- 1. Generate Synthetic Data ---
np.random.seed(42)
# Create daily data
dates_daily = pd.date_range("2021-01-01", "2025-12-31", freq="D")
values_daily = np.random.randint(5, 15, size=len(dates_daily))  # random daily values
df_daily = pd.DataFrame({"Date": dates_daily, "Value": values_daily})
df_daily.set_index("Date", inplace=True)
# Resample data to get monthly and yearly data
df_monthly = df_daily.resample("M").sum().reset_index()
df_yearly = df_daily.resample("Y").sum().reset_index()
# --- 2. Create Traces for Different Timeframes ---
trace_daily = go.Scatter(
    x=df_daily.index, 
    y=df_daily["Value"], 
    mode="lines+markers",
    name="Daily",
    visible=True
)
trace_monthly = go.Scatter(
    x=df_monthly["Date"], 
    y=df_monthly["Value"], 
    mode="lines+markers",
    name="Monthly",
    visible=False
)
trace_yearly = go.Scatter(
    x=df_yearly["Date"], 
    y=df_yearly["Value"], 
    mode="lines+markers",
    name="Yearly",
    visible=False
)
# --- 3. Build Figure with Dropdown ---
fig = go.Figure(data=[trace_daily, trace_monthly, trace_yearly])
fig.update_layout(
    title="Interactive Time Series with Dropdown",
    xaxis_title="Date",
    yaxis_title="Value",
    updatemenus=[
        dict(
            buttons=[
                dict(label="Daily",
                     method="update",
                     args=[{"visible": [True, False, False]},
                           {"title": "Daily Time Series"}]),
                dict(label="Monthly",
                     method="update",
                     args=[{"visible": [False, True, False]},
                           {"title": "Monthly Time Series"}]),
                dict(label="Yearly",
                     method="update",
                     args=[{"visible": [False, False, True]},
                           {"title": "Yearly Time Series"}])
            ],
            direction="down",
            showactive=True,
            x=0.5,
            xanchor="center",
            y=1.2,
            yanchor="top"
        )
    ]
)
fig.show()
