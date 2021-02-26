# Files

* Write files

`w`: write (overwrite),
`r`: read,
`a`: append
```
f = open("20210224.log", "w")
f.write("Woops! I have deleted the content!")
f.close()
```