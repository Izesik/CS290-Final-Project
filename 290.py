import duckdb
import pandas as pd

isCleaned = False

def main():
    db = duckdb.connect("test3.duckdb")
    c = db.cursor()

    cleanJSON('franchises.json', 'games')
    cleanJSON('games.json', 'genres')

    CreateDatabase(c)
    populate_database(c)

    c.close()

def cleanJSON(fileName, column):
    df = pd.read_json(fileName)
    df[column] = df[column].str.replace("{", "").str.replace("}", "").str.split(",")
    df[column] = df[column].apply(lambda x: [int(i) for i in x] if x is not None else None)

    df.to_json(f'cleaned_{fileName}', orient='records', indent=2)

def CreateDatabase(con):
    con.execute("CREATE TABLE genres (id INTEGER PRIMARY KEY, name VARCHAR)")
    con.execute("CREATE TABLE franchises (id INTEGER PRIMARY KEY, name VARCHAR, games INTEGER[])")
    con.execute("CREATE TABLE games (id INTEGER PRIMARY KEY, name VARCHAR, genres INTEGER[])")

def populate_database(con):
    con.execute("INSERT INTO genres SELECT id, name FROM read_json_auto('genres.json')")
    con.execute("INSERT INTO franchises SELECT id, name, games FROM read_json_auto('cleaned_franchises.json')")
    con.execute("INSERT INTO games SELECT id, name, genres FROM read_json_auto('cleaned_games.json')")

if __name__ == "__main__":
    main()






