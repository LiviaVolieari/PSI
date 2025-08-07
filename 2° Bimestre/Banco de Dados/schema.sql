drop table if not exists users;
create table if not exists users (
    id integer primary key autoincrement,
    Nome text not null
)