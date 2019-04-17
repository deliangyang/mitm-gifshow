
### GifShow Live Spider

#### Composition

```
mitmproxy + selenium
```

#### Description

1. ```create_db.py```, create sqlite database
2. ```export.py```, export data to excel, and created in the path ```data```
3. ```run.py```, auto control browser, and jump to other page
3. ```get_data.py```, create a http/https proxy, and get http/https response from mitmproxy

#### How to use it?

```bash
python create_db.py
# set  http or https proxy for browser
mitmdump -s get_data.py
python run.py
python export.py
```

#### Download ChromeDriver

> current version is 73.0.3683.68

```
http://chromedriver.storage.googleapis.com/index.html
```