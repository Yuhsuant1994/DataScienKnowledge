# git push

```
git pull
git clone
git status
git add (file name / --all)
git commit -m "description"
git push

git checkout (change branch)
```

# small command

`python3 -m pip install --user pandas `

`rm (-rf) (**/*.log)`:remove files

 `cp`,  `mv `: copy, move

`python3 run.py`, `cd ..`

## find file

`find -name *.git*`

`find -name *.log -delete`: dangerous delete all find file

`find . -depth -name __pycache__  -execdir rm -rf {} ;` directory

`grep -rnw '/path/to/somewhere/' -e 'pattern'`
* -r or -R is recursive,
* -n is line number, and
* -w stands for match the whole word.
* -l (lower-case L) can be added to just give the file name of matching files.
* -e is the pattern used during the search

-------------

```
vim file.py

i -> insert
exit then :wq -> write and quit
d -> delete
```

# crontab

set scheduler to run script, file name file.cron, [file setup ref](http://www.scrounge.org/linux/cron.html)

```
crontab -l  list of jobs
crontab -r  reomve all jobs
crontab file.cron  add jobs
```

[min] [hour] [day of month] [month] [day of week] [program to be run]

ex:
```
--Will run /usr/bin/foo every 15 minutes on every hour, day-of-month, month, and day-of-week. In other words, it will run every 15 minutes for as long as the machine it running.
0,15,30,45 * * * * /usr/bin/foo
```

# other

`curl -X GET "localhost:9200/"`: send an HRRP request to port 9200