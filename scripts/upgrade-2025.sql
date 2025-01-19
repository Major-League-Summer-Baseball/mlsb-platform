ALTER TABLE player
	ALTER COLUMN password TYPE varchar(240);

CREATE SEQUENCE image_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

CREATE TABLE IF NOT EXISTS image
(
    id integer NOT NULL DEFAULT nextval('image_id_seq'::regclass),
    url text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT image_pkey PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS sponsor
    ADD COLUMN logo_id integer;

ALTER TABLE sponsor
    ADD CONSTRAINT sponsor_logo_id_fkey FOREIGN KEY (logo_id)
    REFERENCES image (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;

ALTER TABLE IF EXISTS league_event
    ADD COLUMN image_id integer;

ALTER TABLE IF EXISTS league_event
    ADD CONSTRAINT league_event_image_id_fkey FOREIGN KEY (image_id)
    REFERENCES image (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;

ALTER TABLE IF EXISTS league_event_date
    ADD COLUMN image_id integer;

ALTER TABLE IF EXISTS league_event_date
    ADD CONSTRAINT league_event_date_image_id_fkey FOREIGN KEY (image_id)
    REFERENCES image (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;

ALTER TABLE IF EXISTS team
    ADD COLUMN image_id integer;

ALTER TABLE IF EXISTS team
    ADD CONSTRAINT team_image_id_fkey FOREIGN KEY (image_id)
    REFERENCES image (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;

-- map all existing sponsors to its logos uploaded to tigris
INSERT INTO image (url)
SELECT 
	CONCAT(
		'https://fly.storage.tigris.dev/image-store/sponsors/',
		REPLACE(LOWER(TRIM(name)), ' ', '_'),
		'.png'
	)
FROM sponsor
WHERE name is not null and name <> ' '
ORDER BY name;

UPDATE sponsor
SET logo_id = (
	SELECT id FROM image
	WHERE url = CONCAT(
		'https://fly.storage.tigris.dev/image-store/sponsors/',
		REPLACE(LOWER(TRIM(sponsor.name)), ' ', '_'),
		'.png'
	)
);


-- map all existing league event to their images uploaded to tigris
INSERT INTO image (url)
SELECT 
	CONCAT(
		'https://fly.storage.tigris.dev/image-store/events/',
		REPLACE(LOWER(TRIM(name)), ' ', '_'),
		'.png'
	)
FROM league_event
WHERE name is not null and name <> ' '
ORDER BY name;

UPDATE league_event
SET image_id = (
	SELECT id FROM image
	WHERE url = CONCAT(
		'https://fly.storage.tigris.dev/image-store/events/',
		REPLACE(LOWER(TRIM(league_event.name)), ' ', '_'),
		'.png'
	)
);
