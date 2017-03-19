# Tournament Results Project Submission

## Review

Modified code is in the [`tournament`](vagrant\tournament) directory.

### [`tournament.sql`](vagrant\tournament\tournament.sql)

SQL script to prepare a new tournament database.

#### `Players` table
Table recording a unique ID and required full player name.

#### `Matches` table
Table recording a winner and loser for a match, using foreign keys on `Player.id`.

#### `PlayerWins` view
View presenting an ordered list of players and their number of wins.
This is used in the implementation of both `playerStandings()` and `swissPairings()`.

### [`tournament.py`](vagrant\tournament\tournament.py)

Data access layer containing loose utility functions for manipulating player and match data, 
and running a Swiss Tournament round. 

Backed by a PostgreSQL database using the [`psycopg2`](http://initd.org/psycopg/) Python API.

#### `playerStandings()`
This function leverages the `PlayerWins` view to fetch the pre-calculated number of player wins, 
and also does its own count of matches in which the player has been named a winner or loser.
It also sorts the results by wins descending.

#### `swissPairings()`
This function performs a self-join on the `PlayerWins` view, 
merging pairs of rows into the output tuple of player pairs (opponents).
Note that the view is already sorted by wins descending, so adjacent rows 
have players with a comparable number of wins.

### [`tournament_test.py`](vagrant\tournament\tournament_test.py)

Unit tests for [`tournament.py`](tournament.py).

An additional test `testPlayerStandingsSortedByWins()` was added to meet the requirement 
given in the docstring for `playerStandings()`. 

## Build

1. Clone the repo and follow the Udacity setup instructions for Vagrant and VirtualBox.
2. Open a command prompt in the repo and change to the vagrant directory `cd vagrant`.
3. Launch the VM `vagrant up`.
4. SSH into the VM `vagrant ssh`.
5. Change to the tournament directory `cd /vagrant/tournament`.
6. Launch psql `psql`.
7. Prepare a new tournament database `\i tournament.sql`.
8. Quit psql `\q`.

## Run

Open `tournament_test.py` in a Python interpreter 
to execute the unit test suite `python tournament_test.py`.
