@echo off
::start python server.py
cd /d spider\govcrawl
scrapy crawl govspider
cd ..\..\
::for /l %%i in (1,1,1) do (python main.py < txt\parameter.txt)
::python query.py >> result.txt
pause
