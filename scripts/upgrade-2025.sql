ALTER TABLE [player]
ALTER COLUMN [password] varchar(240);

CREATE TABLE IF NOT EXISTS [image]
(
    id integer NOT NULL DEFAULT nextval('image_id_seq'::regclass),
    url text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT image_pkey PRIMARY KEY (id)
)

ALTER TABLE [sponsor]
    ADD CONSTRAINT sponsor_logo_id_fkey FOREIGN KEY (logo_id)
    REFERENCES [image] (id) MATCH SIMPLE
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