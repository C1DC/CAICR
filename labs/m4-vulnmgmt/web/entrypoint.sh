#!/bin/sh
# Render the leaked files from this student's values (env from the lab engine),
# with defaults that preserve the standalone static behaviour, then serve.
: "${CAIC_ADMIN_HASH:=5f4dcc3b5aa765d61d8327deb882cf99}"   # md5("password")
: "${CAIC_DB_PASS:=Acme#2019}"
DOC=/usr/local/apache2/htdocs

cat > "$DOC/backup/db_dump.sql" <<SQL
-- Acme Payroll — nightly MySQL backup (LEFT WORLD-READABLE BY MISTAKE)
-- Found under /backup/ — this should never be reachable from the web.
CREATE TABLE users (id INT, username VARCHAR(32), pass_md5 CHAR(32), role VARCHAR(16));
INSERT INTO users VALUES
 (1,'admin',   '${CAIC_ADMIN_HASH}','superadmin'),
 (2,'j.owusu', 'e10adc3949ba59abbe56e057f20f883e','clerk'),
 (3,'finance', '25d55ad283aa400af464c76d713c07ad','approver'),
 (4,'backup',  '827ccb0eea8a706c4c34a16891f84e7b','service');
-- NOTE: passwords stored as UNSALTED MD5 — crack them to prove the point.
SQL

cat > "$DOC/config.php.bak" <<CFG
<?php
// BACKUP - DO NOT DEPLOY
\$db_host="10.13.4.50"; \$db_user="root"; \$db_pass="${CAIC_DB_PASS}"; \$db_name="portal";
?>
CFG

exec httpd-foreground
