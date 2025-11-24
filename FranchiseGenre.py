import pandas as pd
import duckdb

con = duckdb.connect('games.duckdb')

genres = con.execute("SELECT * FROM genres").df()
franchises = con.execute("SELECT * FROM franchises").df()
games = con.execute("SELECT * FROM games").df()

games_processed = games.copy()
games_processed['main_genre_id'] = games_processed['genres'].str[0]

exploded = franchises.explode('games')

merged_games = exploded.merge(
    games_processed,
    left_on='games',
    right_on='id',
    suffixes=('_franchise', '_game')
)

full_data = merged_games.merge(
    genres,
    left_on='main_genre_id',
    right_on='id'
)

genre_counts = full_data.groupby(['id_franchise', 'name']).size().reset_index(name='count')
top_genres = genre_counts.sort_values('count', ascending=False) \
                         .groupby('id_franchise') \
                         .head(1) \
                         .rename(columns={'name': 'franchise_genre'})

franchises = franchises.merge(
    top_genres[['id_franchise', 'franchise_genre']],
    left_on='id',
    right_on='id_franchise',
    how='left'
)

if 'id_franchise' in franchises.columns:
    franchises = franchises.drop(columns=['id_franchise'])

try:
    con.execute("ALTER TABLE franchises ADD COLUMN franchise_genre VARCHAR")
except duckdb.CatalogException:
    print("Column 'franchise_genre' likely already exists.")

con.register('df', franchises[['id', 'franchise_genre']])

con.execute("""
    UPDATE franchises
    SET franchise_genre = df.franchise_genre
    FROM df
    WHERE franchises.id = df.id
""")