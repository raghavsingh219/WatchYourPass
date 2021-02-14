
CREATE TABLE IF NOT EXISTS tmp_api_password (
    id SERIAL,
    hash character varying(100) UNIQUE NOT NULL,
    count integer NOT NULL
);
TRUNCATE TABLE tmp_api_password;

BEGIN;
    INSERT INTO tmp_api_password(hash,count)
    SELECT hash,count(hash)
    FROM tmp group by(hash);
commit;


