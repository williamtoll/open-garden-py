select * from watering_schedule where status='pending';


update watering_schedule set date_from="2020-11-22 12:45:00" where status='pending' ;

update watering_schedule set date_from="2020-11-22 12:47:00", date_to='2020-11-22 13:00:00' where status='pending' ;


insert into watering_schedule(date_from,date_to,zone_id,status) values('2020-11-20 13:05:00','2020-11-20 13:10:00',2,'pending');

insert into watering_schedule(date_from,date_to,zone_id,status) values('2020-11-20 13:19:00','2020-11-20 13:15:00',3,'pending');

