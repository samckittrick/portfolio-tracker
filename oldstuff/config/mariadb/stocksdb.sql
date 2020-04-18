DROP TABLE IF EXISTS `symbols`;
CREATE TABLE `symbols` (
  `symbol` VARCHAR(6) NOT NULL PRIMARY KEY,
  `companyName` VARCHAR(64),
  `exchange` VARCHAR(6)
);

/* test data */
insert into symbols (`symbol`) values ('AAPL'),('UNP'), ('^DJI'), ('^IXIC') ;
