INSERT INTO api_domain(domain,count)
SELECT domain,count(domain)
FROM tmp group by(domain);
commit;

