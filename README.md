Rotto-Links-Scraper
=======================

A web crawler/scraper to find the broken links in the targeted seed url based on the keywords matched in the broken links contained page .

##Installation
1. Redis
2. Python 2.7+

##Instructions
1. First install all dependencies listed in **`requirements.txt`** using *pip* package manager :(dsd)
```
    $ pip install -r requirements.txt
```

2. Set the **`DATABASE_PATH`** environment variables **`(i.e SMTP_USER, SMTP_PASSWORD)`** in your shell config file(i.e *.bashrc* , *.zshrc* or etc)
```python
    # your shell config file
    export DATABASE_PATH='/path/to/database/'
```

3. Also, set the two more environment variables required for **`SMTP Server`**  for sending email to users in your shell config file.
```python
    # your shell config file
    export SMTP_USER='smtp-username'
    export SMTP_PASSWORD='smtp-password'
```

##Commands
To run a gui app :
```
    $ python rottoscraper/run.py app
```
To run a dispatcher :
```
    $ python rottoscraper/run.py dispatcher
```
To run a worker :
```
    $ python rotttoscraper/worker.py
```
##Developer
1. [Akshay Pratap Singh](https://www.facebook.com/AKSHAYPRATAP007)
2. [Sunny Gupta](https://www.facebook.com/sunnyLA.Gupta)
