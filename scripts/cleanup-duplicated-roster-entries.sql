CREATE TEMP TABLE cleanedRoster AS 
SELECT player_id, team_id FROM roster GROUP BY player_id, team_id;

DELETE FROM roster;

INSERT INTO roster SELECT * FROM cleanedRoster;

ALTER TABLE roster
ADD CONSTRAINT roster_pkey PRIMARY KEY (player_id, team_id),

