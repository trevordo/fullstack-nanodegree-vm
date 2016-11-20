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
    conn = connect()
    c = conn.cursor()
    # Clear Matches
    matches = "DELETE FROM Matches"
    c.execute(matches)
    # Update Standings without clearing standings
    standing = "UPDATE Standings SET score = 0, matches = 0"

    c.execute(standing)
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    # Clear Standings First
    standings = "DELETE FROM Standings"
    c.execute(standings)
    # Clear Players 
    players = "DELETE FROM Players"
    c.execute(players)
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    # SQL statement to count the number of players
    count = "SELECT count(*) FROM Players"
    c.execute(count)
    result = c.fetchone()
    total = result [0]
    conn.close()
    return total


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    # SQL statement for adding player to table Players
    player = "INSERT INTO Players (name) VALUES(%s) RETURNING id"
    # SQL statement for adding player to table Standings
    standing = "INSERT INTO Standings (player_id,name) VALUES (%s,%s)"
    c.execute(player, (name,))
    player_id = c.fetchone()[0]
    c.execute(standing, (player_id,name,))
    conn.commit()
    conn.close()


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
    conn = connect()
    c = conn.cursor()
    # SQL statement to resturn standing
    standings = "SELECT * FROM Standings ORDER BY score DESC"
    c.execute(standings)
    result = c.fetchall()
    conn.close()
    return result


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    win_point = 1
    lose_point = 0
    # SQL statement to insert match results into Matches and add to table
    sql = "INSERT into Matches (winner_id, loser_id) VALUES (%s,%s)"

    conn = connect()
    c = conn.cursor()
    c.execute(sql, (winner, loser,))

    # SQL statements to update table Standings
    win = """UPDATE Standings 
             SET score = score+%s, matches = matches+1 
             WHERE player_id = %s"""
    loss = """UPDATE Standings 
             SET score = score+%s, matches = matches+1 
             WHERE player_id = %s"""

    c.execute(win, (win_point, winner,))
    c.execute(loss, (lose_point, loser,))
    conn.commit()
    conn.close()
 
 
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
    # SQL statement to rank players according to score(ie wins)
    sql = """SELECT player_id, name FROM Standings
             ORDER BY score DESC"""

    conn = connect()
    c = conn.cursor()
    c.execute(sql)
    top = c.fetchall()

    # Extract all the fields into a list
    p = []
    [p.extend(item) for item in top]

    # Group list items into tuples so pairs are group by rank
    pairs = [tuple(p[i:i+4]) for i in range(0, len(p), 4)]

    conn.close()
    return pairs
