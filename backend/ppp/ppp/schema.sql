drop table if exists entries;
create table entries (
    id integer primary key autoincrement,
    action text not null,
    toiletId integer,
		ts text
);
