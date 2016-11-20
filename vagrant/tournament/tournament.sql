-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


/* 
First drop database to clear then
Create the database and establish schema
Tables - capital and plural
fields - lowercase

Tables (Players, Matches, Scores, )

 */

DROP DATABASE tournament;


CREATE DATABASE tournament;

-- connect to database
\c tournament 

-- create Players Table
CREATE TABLE Players (
        name text,
        id serial PRIMARY KEY
);

-- create Matches Table
CREATE TABLE Matches ( 
        winner_id INTEGER REFERENCES Players(id),
        loser_id INTEGER REFERENCES Players(id),
        matchid SERIAL PRIMARY KEY
);

-- create Standings Table

CREATE TABLE Standings ( 
        player_id INTEGER REFERENCES Players(id),
        name TEXT,
        score INTEGER  DEFAULT 0,
        matches INTEGER DEFAULT 0
);
