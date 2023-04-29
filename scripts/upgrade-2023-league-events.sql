CREATE SEQUENCE public.league_event_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

CREATE SEQUENCE public.league_event_date_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

CREATE TABLE IF NOT EXISTS public.league_event
(
    id integer NOT NULL DEFAULT nextval('league_event_id_seq'::regclass),
    name character varying(80) COLLATE pg_catalog."default",
    description text COLLATE pg_catalog."default",
    active boolean,
    CONSTRAINT league_event_pkey PRIMARY KEY (id)
)


CREATE TABLE IF NOT EXISTS public.league_event_date
(
    id integer NOT NULL DEFAULT nextval('league_event_date_id_seq'::regclass),
    league_event_id integer,
    date timestamp without time zone,
    CONSTRAINT league_event_date_pkey PRIMARY KEY (id),
    CONSTRAINT league_event_date_league_event_id_fkey FOREIGN KEY (league_event_id)
        REFERENCES public.league_event (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

CREATE TABLE IF NOT EXISTS public.attendance
(
    player_id integer,
    league_event_date_id integer,
    CONSTRAINT attendance_league_event_date_id_fkey FOREIGN KEY (league_event_date_id)
        REFERENCES public.league_event_date (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT attendance_player_id_fkey FOREIGN KEY (player_id)
        REFERENCES public.player (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

/* Insert all the existing data from previous years. */
INSERT INTO league_event (name, active, description) VALUES
('Beerlympics', true, '<p>
            Beerlympics (formerly called Beerfest). Ever seen the movie? Well this is even better. Teams dressed up as various countries competing under the hot sun coupled with several awesome drinking games makes for a day that you will never forget.
            </p>
            <p>Actually, you probably won’t be able to remember much at all. Teams that do well will bring home points for the year end ESPYs.</p>'),
('Jays Game', true, '<p>What better way to get ready for the MLSB season than to drive down buses full of party animals like yourselves to T.O. to watch the boys of summer?</p>'),
('Summerween', true, '<p>
                We all know Halloween during university is the best holiday for several obvious reasons. At MLSB, you get to partake in celebrating this joyous day twice a year.
            </p>
            <p>
                Best costumes take home points for the ESPYs.
            </p>'),
('Mystery Bus', true, '<p>What do you get when you cram over a hundred students on to school buses and send them to a bar in the middle of nowhere? A hell of a good time! This event marks the start of MLSB every year and takes place in the winter.</p>'),
('Rafting', true, '<p>
                Rafting is the most hyped MLSB event of the summer! It is a whirlwind of a weekend with rafting, camping, tanning, and drinking events on the Ottawa river with our friends at OWL Rafting.
            </p>
            <p>
                If there is one MLSB event you shouldn’t miss, it is definitely this one because it is going to be a wild weekend!
            </p>'),
('Hitting for the cycle', false,'<p>
                HFTC is MLSB’s infamous pub crawl. For most MLSBers, this will be your only realistic chance to actually hit the cycle (by way of bar shots of course). Make your way from bar to bar in a state that is likely to keep you out of commission for the better part of the next day.
            </p>
            <p>
                Sleeve monsters are a must.
            </p>'),
('Grand Bender', true, '<p>
                MLSB hosts their annual All Star tournament, and what could be better than playing it in a baseball field in the middle of nowhere!  Those not participating in the All Star Game are in for a treat, as they get the entertainment of watching the All-Stars get clumsy on the field.
            </p>
            <p>
                Bring your tents because we will be camping out for the night!
            </p>'),
('MLSB Alumni', true, '<p>
            A weekend for those who have graduated to relive the glory days.
            The tournemant is welcome to both current players and alumni.
            It really is the tournament where legends are born.
        </p>
        <p>
            One of the best weekends of the summer.
            <a href="mailto:mlsbalumni@gmail.com?Subject=MLSB Alumni Registration">
                Sign up
            </a>
        </p>');
  
INSERT INTO league_event_date (league_event_id, date) VALUES
/* All beer olympics */
(1, '2016-05-13 13:00:00'),
(1, '2017-05-17 13:00:00'),
(1, '2018-06-9 13:00:00'),
(1, '2022-06-11 13:00:00'),
/* All Jays games */
(2, '2016-05-17 13:00:00'),
(2, '2017-05-9 13:00:00'),
(2, '2018-05-22 13:00:00'),
(2, '2022-05-24 13:00:00'),
/* All Summerweens */
(3, '2016-06-11 13:00:00'),
(3, '2017-06-3 13:00:00'),
(3, '2018-06-23 13:00:00'),
(3, '2019-06-21 13:00:00'),
(3, '2022-06-25 13:00:00'),
/* All Mystery Buses */
(4, '2016-03-19 13:00:00'),
(4, '2017-03-24 13:00:00'),
(4, '2018-03-24 13:00:00'),
(4, '2019-03-22 13:00:00'),
(4, '2020-03-7 13:00:00'),
(4, '2023-04-1 13:00:00'),
/* Rafting */
(5, '2016-07-9 13:00:00'),
(5, '2017-07-7 13:00:00'),
(5, '2018-07-6 13:00:00'),
(5, '2019-07-5 13:00:00'),
(5, '2022-07-8 13:00:00'),
/* Hittings for the cycle */
(6, '2016-07-16 13:00:00'),
(6, '2017-07-16 13:00:00'),
/* Grand Benders */
(7, '2016-07-23 13:00:00'),
(7, '2018-07-28 13:00:00'),
(7, '2019-07-29 13:00:00'),
(7, '2022-07-23 13:00:00'),
/* MLSB Alumnis */
(8, '2016-08-13 13:00:00'),
(8, '2017-08-12 13:00:00'),
(8, '2018-07-21 13:00:00'),
(8, '2019-07-20 13:00:00'),
(8, '2022-07-23 13:00:00');











