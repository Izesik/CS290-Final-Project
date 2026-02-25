<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
 
</head>
<body>

<h1>Video Game Franchise Data Wrangling Project</h1>
<p><strong>Course:</strong> Data Wrangling<br>
<strong>Students:</strong> Ryan Demarest & Isaac Nunez <br>
<strong>Final Project</strong></p>

<div class="section">
<h2>Project Overview</h2>
<p>
This project performs an end-to-end data wrangling and database construction workflow using large-scale video game data sourced from IGDB and augmented with Steam identifiers from an external dataset. The objective of the project is to transform raw, semi-structured JSON data into a fully structured relational database using Python, Pandas, and DuckDB, and to engineer new analytical variables such as:
</p>
<ul>
    <li>Franchise lifespan (in years)</li>
    <li>Dominant genre of each franchise</li>
    <li>Steam application IDs for games</li>
</ul>
<p>
The final DuckDB database supports analytical queries on franchise longevity, genre trends, and external platform integration.
</p>
</div>

<div class="section">
<h2>Technologies Used</h2>
<ul>
    <li>Python 3</li>
    <li>Pandas</li>
    <li>DuckDB</li>
    <li>Requests</li>
    <li>JSON & CSV data formats</li>
</ul>
</div>

<div class="section">
<h2>Data Sources</h2>

<h3>Primary Data (IGDB Exports)</h3>
<ul>
    <li>games.json</li>
    <li>franchises.json</li>
    <li>genres.json</li>
</ul>

<h3>External Data</h3>
<ul>
    <li>external_games.csv (used to map IGDB game IDs to Steam application IDs)</li>
</ul>
</div>

<div class="section">
<h2>Data Cleaning Process</h2>

<h3>Franchise Cleaning</h3>
<p>
The games field in franchises.json was originally stored as a string-based list:
</p>
<pre>"{12345, 67890}"</pre>

<p>This column was cleaned by:</p>
<ul>
    <li>Removing curly braces</li>
    <li>Splitting values into lists</li>
    <li>Converting all values to integers</li>
    <li>Exporting to cleaned_franchises.json</li>
</ul>

<h3>Game Cleaning</h3>
<p>Two columns in games.json were cleaned:</p>
<ul>
    <li>genres</li>
    <li>franchises</li>
</ul>

<p>Both were:</p>
<ul>
    <li>Stripped of braces</li>
    <li>Split into arrays</li>
    <li>Converted to integer lists</li>
    <li>Exported to cleaned_games.json</li>
</ul>
</div>

<div class="section">
<h2>Database Schema</h2>

<h3>Genres</h3>
<pre>
CREATE TABLE genres (
    id INTEGER PRIMARY KEY,
    name VARCHAR
);
</pre>

<h3>Franchises</h3>
<pre>
CREATE TABLE franchises (
    id INTEGER PRIMARY KEY,
    name VARCHAR,
    games INTEGER[],
    franchise_duration DOUBLE,
    franchise_genre VARCHAR
);
</pre>

<h3>Games</h3>
<pre>
CREATE TABLE games (
    id INTEGER PRIMARY KEY,
    name VARCHAR,
    genres INTEGER[],
    franchise INTEGER,
    releaseDate DATE,
    steamId INTEGER,
    FOREIGN KEY (franchise) REFERENCES franchises(id)
);
</pre>
</div>

<div class="section">
<h2>Database Population</h2>
<p>Data was inserted using DuckDB’s read_json_auto() function:</p>
<ul>
    <li>genres.json → genres</li>
    <li>cleaned_franchises.json → franchises</li>
    <li>cleaned_games.json → games</li>
</ul>
<p>Franchise IDs for games were normalized using:</p>
<pre>franchises[1]</pre>
</div>

<div class="section">
<h2>Franchise Lifespan Calculation</h2>
<ul>
    <li>franchises.games was exploded into individual rows</li>
    <li>Joined with games.releaseDate</li>
    <li>Grouped by franchise</li>
    <li>Lifespan calculated in days and converted to years</li>
</ul>
<pre>(latest_release - earliest_release).days / 365.25</pre>
<p>The finalized value was stored in the column <strong>franchises.franchise_duration</strong>.</p>
</div>

<div class="section">
<h2>Franchise Dominant Genre Assignment</h2>
<p>
Each game’s primary genre was extracted using the first genre ID in the genres array.
</p>
<ul>
    <li>Exploded franchise-game relationships</li>
    <li>Joined with games and genres</li>
    <li>Counted genre frequency per franchise</li>
    <li>Selected the most common genre</li>
    <li>Updated the franchises table</li>
</ul>
</div>

<div class="section">
<h2>Steam ID Integration</h2>
<ul>
    <li>Filtered external_games.csv for Steam entries</li>
    <li>Joined with the games table on IGDB ID</li>
    <li>Extracted numerical Steam IDs</li>
    <li>Added steamId column to games table</li>
    <li>Updated the database using SQL merge logic</li>
</ul>
</div>

<div class="section">
<h2>Steam API Verification</h2>
<p>
https://store.steampowered.com/api/appdetails?appids=730
</p>
<ul>
    <li>Verified game name</li>
    <li>Verified Steam App ID</li>
    <li>Confirmed successful external mapping</li>
</ul>
</div>

<div class="section">
<h2>Project Structure</h2>
<pre>
project_root/
games.json
franchises.json
genres.json
cleaned_games.json
cleaned_franchises.json
external_games.csv
games.duckdb

clean_data.py
create_database.py
calculate_lifespan.py
assign_franchise_genre.py
steam_id_merge.py
README.md
</pre>
</div>

<div class="section">
<h2>Execution Instructions</h2>
<pre>
pip install pandas duckdb requests
python clean_data.py
python create_database.py
python calculate_lifespan.py
python assign_franchise_genre.py
python steam_id_merge.py
</pre>
</div>

</body>

<div class="section">
<h2>How To Replicate This Project</h2>

<h3>1. Install Required Software</h3>
<ul>
    <li>Install Python 3.10 or newer</li>
    <li>Install DuckDB</li>
    <li>Ensure pip is available</li>
</ul>

<h3>2. Install Required Python Libraries</h3>
<pre>
pip install pandas duckdb requests
</pre>

<h3>3. Obtain the Raw Data Files</h3>
<p>
Place the following files in the project root directory:
</p>
<ul>
    <li>games.json</li>
    <li>franchises.json</li>
    <li>genres.json</li>
    <li>external_games.csv</li>
</ul>

<h3>4. Clean the JSON Data</h3>
<p>Run the cleaning script to convert string-based lists into integer arrays:</p>
<pre>
python clean_data.py
</pre>
<p>This will generate:</p>
<ul>
    <li>cleaned_games.json</li>
    <li>cleaned_franchises.json</li>
</ul>

<h3>5. Create and Populate the Database</h3>
<pre>
python create_database.py
</pre>
<p>This creates the DuckDB database file:</p>
<ul>
    <li>games.duckdb</li>
</ul>

<h3>6. Calculate Franchise Lifespans</h3>
<pre>
python calculate_lifespan.py
</pre>
<p>This computes and stores franchise durations in years.</p>

<h3>7. Assign Franchise Dominant Genres</h3>
<pre>
python assign_franchise_genre.py
</pre>
<p>This computes the majority genre for each franchise.</p>

<h3>8. Merge Steam IDs</h3>
<pre>
python steam_id_merge.py
</pre>
<p>This adds Steam application IDs to the games table.</p>

<h3>9. Verify Using the Steam API (Optional)</h3>
<pre>
https://store.steampowered.com/api/appdetails?appids=730
</pre>

<h3>10. Query the Final Database</h3>
<pre>
import duckdb
con = duckdb.connect("games.duckdb")
</pre>

<p>
At this point, the project is fully reproduced and ready for analysis.
</p>
</div>

</html>
