-- Acme Payroll — nightly MySQL backup (LEFT WORLD-READABLE BY MISTAKE)
-- Found under /backup/ — this should never be reachable from the web.
CREATE TABLE users (id INT, username VARCHAR(32), pass_md5 CHAR(32), role VARCHAR(16));
INSERT INTO users VALUES
 (1,'admin',   '5f4dcc3b5aa765d61d8327deb882cf99','superadmin'),
 (2,'j.owusu', 'e10adc3949ba59abbe56e057f20f883e','clerk'),
 (3,'finance', '25d55ad283aa400af464c76d713c07ad','approver'),
 (4,'backup',  '827ccb0eea8a706c4c34a16891f84e7b','service');
-- NOTE: passwords stored as UNSALTED MD5 — crack them to prove the point.
