-- psql script to prepare a new database for the tournament project.


DROP DATABASE IF EXISTS tournament;
-- DROP VIEW IF EXISTS PlayerWins;
-- DROP TABLE IF EXISTS Matches;
-- DROP TABLE IF EXISTS Players;

CREATE DATABASE tournament;

\c tournament;

CREATE TABLE Players (
    id serial PRIMARY KEY,
    name varchar(64) NOT NULL
);

CREATE TABLE Matches (
    id serial PRIMARY KEY,
    winner integer REFERENCES Players (id),
    loser integer REFERENCES Players (id)
);

CREATE VIEW PlayerWins AS
    SELECT
        row_number() OVER
            (ORDER BY (SELECT COUNT(*) FROM Matches m1 WHERE m1.winner = p.id) DESC)
            as row,
        id,
        name,
        (SELECT COUNT(*) FROM Matches m1 WHERE m1.winner = p.id) as wins
    FROM Players p;
