@echo off

if %time:~0,2% leq 9 (set hour=0%time:~1,1%) else (set hour=%time:~0,2%) 
set dd=%date:~0,4%%date:~5,2%%date:~8,2%_%hour%%time:~3,2%%time:~6,2%

"D:\mysql-8.0.32-winx64\bin\mysqldump.exe" --default-character-set=utf8 --lock-tables=false -u root -P 3306 -p crawler  | gzip  > f:\local_mysql_bak\crawler_%dd%.sql.gz

echo bak file: f:\local_mysql_bak\crawler_%dd%.sql.gz

pause