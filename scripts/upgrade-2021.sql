CREATE SEQUENCE public.flask_dance_oauth_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

CREATE SEQUENCE public.join_league_request_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

CREATE TABLE flask_dance_oauth
(
    id integer NOT NULL DEFAULT nextval('flask_dance_oauth_id_seq'::regclass),
    provider character varying(50) COLLATE pg_catalog."default" NOT NULL,
    created_at timestamp without time zone NOT NULL,
    token json NOT NULL,
    provider_user_id character varying(256) COLLATE pg_catalog."default" NOT NULL,
    player_id integer NOT NULL,
    CONSTRAINT flask_dance_oauth_pkey PRIMARY KEY (id),
    CONSTRAINT flask_dance_oauth_provider_user_id_key UNIQUE (provider_user_id),
    CONSTRAINT flask_dance_oauth_player_id_fkey FOREIGN KEY (player_id)
        REFERENCES public.player (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);

CREATE TABLE join_league_request
(
    id integer NOT NULL DEFAULT nextval('join_league_request_id_seq'::regclass),
    team_id integer NOT NULL,
    email character varying(120) COLLATE pg_catalog."default" NOT NULL,
    name character varying(120) COLLATE pg_catalog."default" NOT NULL,
    pending boolean,
    gender character varying(1) COLLATE pg_catalog."default",
    CONSTRAINT join_league_request_pkey PRIMARY KEY (id),
    CONSTRAINT join_league_request_email_key UNIQUE (email),
    CONSTRAINT join_league_request_team_id_fkey FOREIGN KEY (team_id)
        REFERENCES public.team (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);


