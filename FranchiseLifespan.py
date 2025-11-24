import duckdb
import pandas as pd

con = duckdb.connect("games.duckdb")

franchises = con.execute("SELECT * FROM franchises").df()
games = con.execute('SELECT * FROM games').df()

exploded = franchises.explode('games')
merged = exploded.merge(games[['id', 'releaseDate']], left_on='games', right_on='id', how='left')
result = merged.groupby('id_x').agg(franchise_name=('name', 'first'), earliest_release=('releaseDate', 'min'), latest_release=('releaseDate', 'max')).reset_index()

result['earliest_release'] = pd.to_datetime(result['earliest_release'])
result['latest_release'] = pd.to_datetime(result['latest_release'])

result['lifespan_days'] = (result['latest_release'] - result['earliest_release']).dt.days
result['franchise_lifespan'] = result['lifespan_days'] / 365.25
result['franchise_lifespan'] = result['franchise_lifespan'].round(2)

try:
    con.execute("ALTER TABLE franchises ADD COLUMN franchise_duration DOUBLE")
except duckdb.CatalogException:
    print("Column 'franchise_lifespan' likely already exists.")

con.register('df', result[['id_x', 'franchise_lifespan']])

con.execute("""
    UPDATE franchises
    SET franchise_duration = df.franchise_lifespan
    FROM df
    WHERE franchises.id = df.id_x
""")