begin;

CREATE TABLE persons (
  id SERIAL,
  first_name VARCHAR(50),
  last_name VARCHAR(50),
  dob DATE,
  email VARCHAR(255),
  PRIMARY KEY (id)
);

create temporary table tmp_table as select * from pays where false;
alter table tmp_table ADD COLUMN IF NOT EXISTS code varchar(255) default NULL;
alter table tmp_table ADD COLUMN IF NOT EXISTS alpha3 varchar(255) default NULL;
alter table tmp_table ADD COLUMN IF NOT EXISTS nom_en_gb varchar(255) default NULL;

COPY temporary(id_pays, code, acronyme_pays, alpha3, nom_en_gb, nom_pays) FROM 'C:\Users\User\Documents\INFOSI\PAPPL\other\files\sql-pays.csv' WITH (FORMAT csv, HEADER false);

insert into pays (id_pays, acronyme_pays, nom_pays) select id_pays, acronyme_pays, nom_pays table from tmp_table on conflict do nothing ;

drop table if exists tmp_table;
commit;


begin;
-- create temporary table, its columns NEED to match source file
-- you can also specify all columns manually, they just need to match file.
create temporary table tmp_table as select * from source_table where false;

-- either from file 
copy tmp_table ('list of columns IN THE FILE' ) from '/data/table.csv' WITH (FORMAT csv, HEADER false);


-- you can add, drop, compute additional columns if needed
alter table tmp_table ADD COLUMN IF NOT EXISTS new_column date default NULL;

insert into source_table (columns, in, the, target, table) select columns, in, the, temp, table from tmp_table where optional=conditions on conflict  do nothing ;
drop table if exists tmp_table;
commit;