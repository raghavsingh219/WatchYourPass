
BEGIN;
    INSERT INTO api_password(hash,count)
    SELECT hash,count(hash)
    FROM tmp group by(hash)
    ON CONFLICT (hash) DO UPDATE SET count=(Select count from api_password where hash=excluded.hash)+excluded.count;
commit;