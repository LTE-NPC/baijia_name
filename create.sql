create table baijia_name (
	id int not null auto_increment,
	name varchar(512),
	gender varchar(4),
	constraint pk_baijia_name primary key(id)
	) engine=innodb default charset=utf8;


-- 建索引
create index ix_baijia_name_name on baijia_name (name);

-- 去重
select count(*) from baijia_name;


-- 备份表
create table temp_baijia_result as select distinct name,gender from baijia_name;


-- 清空
truncate table baijia_name;


drop index ix_baijia_name_name on baijia_name;

-- 建索引
create unique index ux_baijia_name_name_gender on baijia_name (name,gender)

insert into baijia_name (name,gender) values ('a','f');


