CREATE TABLE IF NOT EXISTS tmp2_api_account (
    id SERIAL,
    email character varying(100) NOT NULL,
    domain_id integer NOT NULL,
    count integer NOT NULL
);
TRUNCATE TABLE tmp2_api_account;


