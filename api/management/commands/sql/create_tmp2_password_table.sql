CREATE TABLE IF NOT EXISTS tmp2_api_password (
    id SERIAL,
    hash character varying(100) NOT NULL,
    count integer NOT NULL
);
TRUNCATE TABLE tmp2_api_password;

