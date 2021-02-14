BEGIN;
    UPDATE api_password
    SET count=pwd.count+tmp_pwd.count
    FROM tmp_api_password as tmp_pwd INNER JOIN api_password as pwd USING(hash)
    ON tmp_pwd.hash=pwd.hash;
COMMIT;