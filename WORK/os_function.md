# My often used os function

* set project path
```python
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DOWNLOAD_PATH = os.path.join(PROJECT_ROOT, 'data', 'input')
```
* make directory if the path not exist

`os.makedirs(DOWNLOAD_PATH, exist_ok=True)`

* remove useless file / directory in the end

```python
import os, shutil
folder = '/path/to/folder'
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))
```