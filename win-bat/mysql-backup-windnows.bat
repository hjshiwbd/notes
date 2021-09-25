@echo off

if %time:~0,2% leq 9 (set hour=0%time:~1,1%) else (set hour=%time:~0,2%) 
set dd=%date:~0,4%%date:~5,2%%date:~8,2%_%hour%%time:~3,2%%time:~6,2%

"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqldump.exe" --lock-tables=false -u root -P 3306 -proot crawler | gzip  > e:\local_mysql_bak\sell_house_%dd%.sql.gz