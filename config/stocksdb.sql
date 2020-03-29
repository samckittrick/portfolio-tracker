DROP TABLE IF EXISTS `symbols`;
CREATE TABLE `symbols` (
  `symbol` VARCHAR(6) NOT NULL PRIMARY KEY
);

/* test data */
insert into symbols values ('aapl'),('unp');
