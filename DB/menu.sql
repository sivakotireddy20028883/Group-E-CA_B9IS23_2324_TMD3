-- Table: public.menu

CREATE SEQUENCE IF NOT EXISTS menu_id_seq START 1;

CREATE TABLE IF NOT EXISTS public.menu
(
    id integer NOT NULL DEFAULT nextval('menu_id_seq'::regclass),
    name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    description text COLLATE pg_catalog."default",
    price numeric(10,2) NOT NULL,
    availability boolean DEFAULT true,
    CONSTRAINT menu_pkey PRIMARY KEY (id)
);

-- Create sequence if it doesn't exist


-- Set ownership of the sequence
ALTER SEQUENCE IF EXISTS menu_id_seq OWNER TO postgres;

-- Set default value of id column to use the sequence
ALTER TABLE menu ALTER COLUMN id SET DEFAULT nextval('menu_id_seq'::regclass);



ALTER TABLE IF EXISTS public.menu
    OWNER to postgres;
