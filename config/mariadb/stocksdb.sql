DROP TABLE IF EXISTS `symbols`;
CREATE TABLE `symbols` (
  `symbol` VARCHAR(6) NOT NULL PRIMARY KEY,
  `companyName` VARCHAR(64) NOT NULL,
  `exchange` VARCHAR(6) NOT NULL
);

/* test data */
insert into symbols values ('aapl'),('unp'), ('^DJI'), ('IXIC') ;
