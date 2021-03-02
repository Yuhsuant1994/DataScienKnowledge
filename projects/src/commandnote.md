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

`find -name *.git*`

`find -name *.log -delete`: dangerous delete all find file

`find . -depth -name __pycache__  -execdir rm -rf {} ;` directory

```
Use -execdir, not -exec
From man find:

There are unavoidable security problems surrounding use of the -exec action; you should use the -execdir option instead.

In most case, -execdir is a drop-in replacement for -exec.

Use +, not ;
From man find:

As with the -exec action, the `+' form of -execdir will build a command line to process more than one matched file, but any given invocation of command will only list files that exist in the same subdirectory.

When looking for an exact name match, + and ; will do the same, as you cannot have two files with the same name in the same directory, but + will provide increased performance when several files/directories match your find expression within the same directory.

Also, ; needs escaping from your shell, + does not.
```

```
vim file.py

i -> insert
exit then :wq -> write and quit
d -> delete
```

# crontab

file name file.cron

```
crontab -l  list of jobs
crontab -r  reomve all jobs
crontab file.cron  add jobs
```

