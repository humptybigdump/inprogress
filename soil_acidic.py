# soil_acidic.py
def filter_acidic_soils(df):
    """Filter the soil data to pick out acidic soils (pH < 7)."""
    acidic_soils = df[df['pH'] < 7]
    return acidic_soils

