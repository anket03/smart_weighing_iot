CREATE TABLE pi_sql (
    id INT IDENTITY(1,1) PRIMARY KEY,
    batch VARCHAR(20),
    [user] VARCHAR(20),
    gross FLOAT,
    tare FLOAT,
    net FLOAT,
	product VARCHAR(50),
    is_underweight BIT,
    is_overweight BIT,
    is_valid BIT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

select * from pi_sql order by id desc;

ALTER TABLE pi_sql 
DROP COLUMN product;

#drop table pi_sql;

use iot;
