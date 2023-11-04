CREATE TABLE public.users
(
    userid integer NOT NULL,
    name text COLLATE pg_catalog."default",
    CONSTRAINT userid PRIMARY KEY (userid)
)


CREATE TABLE public.movies
(
    movieid integer NOT NULL,
    title text COLLATE pg_catalog."default",
    CONSTRAINT movieid PRIMARY KEY (movieid)
)


CREATE TABLE public.Taginfo
(
    tagid integer NOT NULL,
    content text COLLATE pg_catalog."default",
    CONSTRAINT tagid PRIMARY KEY (tagid)
)


CREATE TABLE public.genres
(
    genreid integer NOT NULL,
    name text COLLATE pg_catalog."default",
    CONSTRAINT genreid PRIMARY KEY (genreid)
)


CREATE TABLE public.ratings
(
    userid integer,
    movieid integer,
    rating numeric,
    timestamp bigint,
    CONSTRAINT movieid FOREIGN KEY (userid)
        REFERENCES public.movies (movieid) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID,
    CONSTRAINT userid FOREIGN KEY (userid)
        REFERENCES public.users (userid) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
)




CREATE INDEX fki_userid
    ON public.ratings USING btree
    (userid)
    TABLESPACE pg_default;
CREATE TABLE public.tags
(
    userid integer,
    movieid integer,
    timestamp bigint,
    tagid integer,
    CONSTRAINT movieid FOREIGN KEY (movieid)
        REFERENCES public.movies (movieid) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID,
    CONSTRAINT tagid FOREIGN KEY (tagid)
        REFERENCES public.Taginfo (tagid) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID,
    CONSTRAINT userid FOREIGN KEY (userid)
        REFERENCES public.users (userid) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
)


CREATE INDEX fki_movieid
    ON public.tags USING btree
    (movieid)
    

CREATE INDEX fki_tagid
    ON public.tags USING btree
    (userid)
CREATE TABLE public.hasagenre
(
    movieid integer,
    genreid integer,
    CONSTRAINT genreid FOREIGN KEY (genreid)
        REFERENCES public.genres (genreid) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID,
    CONSTRAINT movieid FOREIGN KEY (movieid)
        REFERENCES public.movies (movieid) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
)




CREATE INDEX fki_genreid
    ON public.hasagenre USING btree
    (genreid)
   