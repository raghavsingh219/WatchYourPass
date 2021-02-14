CREATE TABLE IF NOT EXISTS tmp2_api_password (
    id SERIAL,
    hash character varying(100) NOT NULL,
    count integer NOT NULL
);

BEGIN;

    INSERT INTO tmp2_api_password(hash,count)
    SELECT tmp_api_password.hash,tmp_api_password.count FROM api_password INNER JOIN tmp_api_password
    ON tmp_api_password.hash=api_password.hash;

--    DELETE FROM api_password WHERE hash IN
--    (SELECT hash from tmp2_api_password);

    DELETE FROM api_password pwd
    USING tmp2_api_password tmp_pwd
    WHERE pwd.hash=tmp_pwd.hash;

    INSERT INTO tmp2_api_password(hash,count)
    SELECT tmp_api_password.hash,tmp_api_password.count FROM tmp_api_password INNER JOIN tmp2_api_password
    ON tmp2_api_password.hash=tmp_api_password.hash;

    CREATE INDEX pwd_hash ON tmp2_api_password(hash);

    INSERT INTO api_password(hash,count)
    SELECT hash,sum(count) as count FROM tmp2_api_password
    GROUP BY(hash);

    DROP INDEX pwd_hash;

COMMIT;
