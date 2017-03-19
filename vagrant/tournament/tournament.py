#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
	"""Connect to the PostgreSQL database.  Returns a database connection."""
	return psycopg2.connect("dbname=tournament")


def deleteMatches():
	"""Remove all the match records from the database."""
	con = connect()
	cur = con.cursor()
	cur.execute("DELETE FROM Matches;")
	con.commit()
	con.close()


def deletePlayers():
	"""Remove all the player records from the database."""
	con = connect()
	cur = con.cursor()
	cur.execute("DELETE FROM Players;")
	con.commit()
	con.close()


def countPlayers():
	"""Returns the number of players currently registered."""
	con = connect()
	cur = con.cursor()
	cur.execute("SELECT COUNT(*) FROM Players;")
	res = cur.fetchone()
	con.commit()
	con.close()
	return res[0]


def registerPlayer(name):
	"""Adds a player to the tournament database.

	The database assigns a unique serial id number for the player.  (This
	should be handled by your SQL database schema, not in your Python code.)

	Args:
	  name: the player's full name (need not be unique).
	"""
	con = connect()
	cur = con.cursor()
	cmd = "INSERT INTO Players (name) VALUES (%s);"
	values = [name]
	cur.execute(cmd, values)  # prevent SQL injection
	con.commit()
	con.close()


def playerStandings():
	"""Returns a list of the players and their win records, sorted by wins.

	The first entry in the list should be the player in first place, or a player
	tied for first place if there is currently a tie.

	Returns:
	  A list of tuples, each of which contains (id, name, wins, matches):
		id: the player's unique id (assigned by the database)
		name: the player's full name (as registered)
		wins: the number of matches the player has won
		matches: the number of matches the player has played
	"""
	con = connect()
	cur = con.cursor()
	cmd = \
		"SELECT p.id, p.name, p.wins, " + \
		"(SELECT COUNT(*) FROM Matches m2 " + \
			"WHERE m2.winner = p.id OR m2.loser = p.id) as matches " + \
		"FROM PlayerWins p " + \
		"ORDER BY wins DESC;"
	cur.execute(cmd)
	res = cur.fetchall()
	con.commit()
	con.close()
	return res


def reportMatch(winner, loser):
	"""Records the outcome of a single match between two players.

	Args:
	  winner:  the id number of the player who won
	  loser:  the id number of the player who lost
	"""
	con = connect()
	cur = con.cursor()
	cmd = "INSERT INTO Matches (winner, loser) VALUES (%s, %s);"
	values = (winner, loser)
	cur.execute(cmd, values)
	con.commit()
	con.close()


def swissPairings():
	"""Returns a list of pairs of players for the next round of a match.

	Assuming that there are an even number of players registered, each player
	appears exactly once in the pairings.  Each player is paired with another
	player with an equal or nearly-equal win record, that is, a player adjacent
	to him or her in the standings.

	Returns:
	  A list of tuples, each of which contains (id1, name1, id2, name2)
		id1: the first player's unique id
		name1: the first player's name
		id2: the second player's unique id
		name2: the second player's name
	"""
	con = connect()
	cur = con.cursor()
	cmd = \
		"SELECT " + \
			"p1.id as id1, p1.name as name1, " + \
			"p2.id as id2, p2.name as name2 " + \
		"FROM PlayerWins p1, PlayerWins p2 " +\
		"WHERE p1.id != p2.id AND p1.row % 2 = 1 AND p2.row = p1.row + 1;"
	cur.execute(cmd)
	res = cur.fetchall()
	con.commit()
	con.close()
	return res
