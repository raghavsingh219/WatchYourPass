BEGIN;
    INSERT INTO api_domain(domain,count)
    SELECT domain,count(domain) as cnt
    FROM tmp group by(domain)
    ON CONFLICT(domain) DO UPDATE SET count=(Select count from api_domain where domain=excluded.domain)+excluded.count;
commit;




