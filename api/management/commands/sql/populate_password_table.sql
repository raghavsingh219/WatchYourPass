
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
    INSERT INTO api_password(hash,count)
    SELECT tmp_api_password.hash,tmp_api_password.count
    FROM tmp_api_password LEFT JOIN api_password ON tmp_api_password.hash=api_password.hash
    WHERE api_password.hash IS NULL;
COMMIT;