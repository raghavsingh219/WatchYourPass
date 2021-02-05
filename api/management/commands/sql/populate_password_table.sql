INSERT INTO api_password(hash,count)
SELECT hash,count(hash)
FROM tmp group by(hash);
commit;