import duckdb

def main():
    db = duckdb.connect("games.duckdb")
    con = db.cursor()

    CreateDatabase(con)
    populate_database(con)

def CreateDatabase(con):
    con.execute("CREATE TABLE genres (id INTEGER PRIMARY KEY, name VARCHAR)")
    con.execute("CREATE TABLE franchises (id INTEGER PRIMARY KEY, name VARCHAR, games INTEGER[])")
    con.execute("CREATE TABLE games (id INTEGER PRIMARY KEY, name VARCHAR, genres INTEGER[], franchise INTEGER, releaseDate DATE, FOREIGN KEY (franchise) REFERENCES franchises(id))")

def populate_database(con):
    con.execute("INSERT INTO genres SELECT id, name FROM read_json_auto('genres.json')")
    con.execute("INSERT INTO franchises SELECT id, name, games FROM read_json_auto('cleaned_franchises.json')")
    con.execute("INSERT INTO games SELECT id, name, genres, franchises[1], first_release_date FROM read_json_auto('cleaned_games.json')")

if __name__ == "__main__":
    main()