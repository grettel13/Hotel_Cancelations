# Part 4: Tennis Data

*Intermediate - Advanced level SQL*

---

## Setup

We'll be using tennis data from [here](https://archive.ics.uci.edu/ml/datasets/Tennis+Major+Tournament+Match+Statistics).

Navigate to your preferred working directory, and download the data.

```bash
curl -L -o tennis.zip http://archive.ics.uci.edu/ml/machine-learning-databases/00300/Tennis-Major-Tournaments-Match-Statistics.zip
unzip tennis.zip -d tennis
```

Make sure you have Postgres installed and initialized

```bash
brew install postgresql
brew services start postgres
```

Install SQLAlchemy if you haven't already

```
conda install -c anaconda sqlalchemy
```

Start Postgres in your terminal with the command `psql`. Then, create a `tennis` database using the `CREATE DATABASE` command.

```
psql

<you_user_name>=# CREATE DATABASE TENNIS;
CREATE DATABASE
<you_user_name>=# \q
```

Pick a table from the *tennis* folder, and upload it to the database using SQLAlchemy and Pandas.

```python
from sqlalchemy import create_engine
import pandas as pd


engine = create_engine('postgresql://<your_user_name>:localhost@localhost:5432/tennis')

aus_men = pd.read_csv('./tennis/AusOpen-men-2013.csv')

# I'm choosing to name this table "aus_men"
aus_men.to_sql('aus_men', engine, index=False)
```

*Note: In the place of `<your_user_name>` you should have your computer user name ...*

Check that you can access the table

```python
query = 'SELECT * FROM aus_men;'
df = pd.read_sql(query, engine)

df.head()
```

Do the same for the other CSV files in the *tennis* directory.

---

## The challenges!

This challenge uses only SQL queries. Please submit answers in a markdown file.

1. Using the same tennis data, find the number of matches played by
   each player in each tournament. (Remember that a player can be
   present as both player1 or player2).

Create view for all matches:
```sql
CREATE VIEW allMatches AS
SELECT *, 'US Open' AS tournament, 'women' as gender FROM us_women
UNION ALL
SELECT *, 'AUST Open' AS tournament, 'women' as gender FROM aus_women
UNION ALL
SELECT *, 'French Open' AS tournament, 'women' as gender FROM french_women
UNION ALL
SELECT *, 'Wimbledon' AS tournament, 'women' as gender FROM wimbledon_women
UNION ALL
SELECT *, 'US Open' AS tournament, 'men' as gender FROM us_men
UNION ALL
SELECT *, 'AUST Open' AS tournament, 'men' as gender FROM aus_men
UNION ALL
SELECT *, 'French Open' AS tournament, 'men' as gender FROM french_men
UNION ALL
SELECT *, 'Wimbledon' AS tournament, 'men' as gender FROM wimbledon_men
```
List players and match counts:
```sql
SELECT player, tournament, SUM(count)
FROM
    (SELECT "Player 2" as player, tournament, COUNT(*) AS count
        FROM allMatches
        GROUP BY "Player 2", tournament
    UNION
    SELECT "Player 1" as player, tournament, COUNT(*) AS count
        FROM allMatches
        GROUP BY "Player 1", tournament) temp
GROUP BY player, tournament
ORDER BY sum DESC
```
Answer:
```{python}
	player	tournament	sum
0	N.Djokovic	Wimbledon	7.0
1	Rafael Nadal	US Open	7.0
2	Dominika Cibulkova	AUST Open	7.0
3	V Azarenka	US Open	7.0
4	Rafael Nadal	French Open	7.0
...	...	...	...
970	Pauline Parmentier	AUST Open	1.0
971	Daniel Munoz-De La Nava	French Open	1.0
972	Mallory Burdette	French Open	1.0
973	L.Dominguez Lino	Wimbledon	1.0
974	M.Rybarikova	Wimbledon	1.0
```

2. Who has played the most matches total in all of US Open, AUST Open,
   French Open? Answer this both for men and women.

Create View of all players:
```sql
CREATE VIEW allPlayers AS
    SELECT "Player 2" as player, tournament, COUNT(*) AS count
        FROM allMatches
        GROUP BY "Player 2", tournament
UNION
    SELECT "Player 1" as player, tournament, COUNT(*) AS count
        FROM allMatches
        GROUP BY "Player 1", tournament
```
List players with most matches across both men and women:
```sql
SELECT * FROM
    (SELECT tournament, player, sum, RANK() OVER my_window
    FROM
        (SELECT tournament, player, SUM(count)
        FROM allPlayers
        GROUP BY tournament, player
        ORDER BY sum DESC) temp
    WINDOW my_window AS
        (PARTITION BY tournament ORDER BY sum DESC)) temp2
WHERE temp2.rank = 1
```
Answer:
```sql
tournament	player
0	AUST Open	Dominika Cibulkova
1	AUST Open	Rafael Nadal
2	AUST Open	Na Li
3	French Open	Maria Sharapova
4	French Open	Serena Williams
5	French Open	David Ferrer
6	French Open	Rafael Nadal
7	US Open	Rafael Nadal
8	US Open	V Azarenka
9	Wimbledon	N.Djokovic
10	Wimbledon	M.Bartoli
11	Wimbledon	S.Lisicki
12	Wimbledon	A.Murray
```
3. Who has the highest first serve percentage? (Just the maximum value
   in a single match.)
```sql
SELECT player, MAX(fsp)
FROM
    (SELECT "Player 2" as player, "FSP.2" as fsp
        FROM allMatches
    UNION
    SELECT "Player 1" as player, "FSP.1" as fsp
        FROM allMatches) temp
GROUP BY player
ORDER BY max DESC
LIMIT 1
```
Answer:
```
	player	max
0	S Errani	93
```

4. What are the unforced error percentages of the top three players
   with the most wins? (Unforced error percentage is % of points lost
   due to unforced errors. In a match, you have fields for number of
   points won by each player, and number of unforced errors for each
   field.)

*Hint:* `SUM(double_faults)` sums the contents of an entire column. For each row, to add the field values from two columns, the syntax `SELECT name, double_faults + unforced_errors` can be used.


*Special bonus hint:* To be careful about handling possible ties, consider using [rank functions](http://www.sql-tutorial.ru/en/book_rank_dense_rank_functions.html).

Create view of winners:
```sql
CREATE VIEW winners AS
SELECT "Player 2" as winner, "UFE.2" as ufe, "DBF.2" as dbf
            FROM allMatches
            WHERE "Result" = 0
    UNION
    SELECT "Player 1" as winner, "UFE.1" as ufe, "DBF.1" as dbf
            FROM allMatches
            WHERE "Result" = 1
```
Calculate unforced error percentage on top 3 players with most wins:
```sql
SELECT temp2.winner as player, (SUM(ufe) * 100 / SUM(dbf + ufe)) as UFE_percentage
FROM
    (SELECT winner, count(*)
    FROM winners
    GROUP BY winner
    ORDER BY count DESC
    LIMIT 3) as temp1
LEFT JOIN
    (SELECT winner, ufe, dbf
    FROM winners
    WHERE (dbf + ufe) != 0) as temp2
ON temp1.winner = temp2.winner
GROUP BY temp2.winner
```
Answer:
```{python}
player	ufe_percentage
0	David Ferrer	90.235690
1	Rafael Nadal	93.800539
2	Stanislas Wawrinka	92.087912
```
