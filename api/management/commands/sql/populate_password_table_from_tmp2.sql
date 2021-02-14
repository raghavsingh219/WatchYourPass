
--BEGIN;
--    INSERT INTO api_password(hash,count)
--    SELECT hash,count(hash)
--    FROM tmp group by(hash)
--    ON CONFLICT (hash) DO UPDATE SET count=(Select count from api_password where hash=excluded.hash)+excluded.count;
--commit;
--BEGIN;
--    INSERT INTO api_password(hash,count)
--    SELECT tmp_api_password.hash,tmp_api_password.count
--    FROM tmp_api_password,api_password
--    WHERE tmp_api_password.hash <> api_password.hash;
--COMMIT;

--Inserting records from tmp_api_password which doesn't exist in api_password

BEGIN;

    INSERT INTO tmp2_api_password(hash,count)
    SELECT api_password.hash,api_password.count FROM api_password INNER JOIN tmp_api_password
    ON tmp_api_password.hash=api_password.hash;

--    DELETE FROM api_password WHERE hash IN
--    (SELECT hash from tmp2_api_password);

    DELETE FROM api_password pwd
    USING tmp2_api_password tmp_pwd
    WHERE pwd.hash=tmp_pwd.hash;

    INSERT INTO tmp2_api_password(hash,count)
    SELECT tmp_api_password.hash,tmp_api_password.count FROM tmp_api_password;

    CREATE INDEX pwd_hash ON tmp2_api_password(hash);

    INSERT INTO api_password(hash,count)
    SELECT hash,sum(count) as count FROM tmp2_api_password
    GROUP BY(hash);


    DROP INDEX pwd_hash;

COMMIT;