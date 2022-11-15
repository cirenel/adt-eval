CREATE TABLE IF NOT EXISTS public.entries
(
    show_id character varying(255) COLLATE pg_catalog."default" NOT NULL,
    media_type character varying(255) COLLATE pg_catalog."default" NOT NULL,
    title character varying(255) COLLATE pg_catalog."default" NOT NULL,
    director character varying(255) COLLATE pg_catalog."default",
    cast_list text COLLATE pg_catalog."default",
    country character varying(255) COLLATE pg_catalog."default",
    date_added character varying(255) COLLATE pg_catalog."default",
    release_year character varying(255) COLLATE pg_catalog."default",
    rating character varying(255) COLLATE pg_catalog."default",
    duration character varying(255) COLLATE pg_catalog."default",
    genre character varying(255) COLLATE pg_catalog."default",
    description text COLLATE pg_catalog."default",
    CONSTRAINT entries_pkey PRIMARY KEY (show_id)
)

TABLESPACE pg_default;