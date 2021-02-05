--CREATE OR REPLACE PROCEDURE populate_tmp()
--    language plpgsql
--    as $$
--    begin
--        COPY tmp(email, domain, hash)
--        FROM '/tmp/tmp.txt'
--        DELIMITER ';';
--
--        commit;
--    end;$$;

CREATE OR REPLACE PROCEDURE populate_tmp()
    language plpgsql
    as $$
    begin
        COPY tmp(email, domain, hash)
        FROM '/tmp/tmp.txt'
        DELIMITER ';';
        STATEMENT := 'COPY (select * from ' || quote_ident(tablename) || ') to ''savedir' || outname ||'.txt''';

        EXECUTE STATEMENT;
        commit;
    end;$$;

