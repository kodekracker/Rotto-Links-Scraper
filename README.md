Rotto-Links-Scraper
=======================

A web crawler/scraper to find the broken links in the targeted seed url based on the keywords matched in the broken links contained page .

##Installation
1. Redis
2. Python 2.7+

##Instructions
1. First install all dependencies listed in **requirements.txt** using *pip* package manager :
```
    $ pip install -r requirements.txt
```

2. Set the **DATABASE_PATH** environment variable in your shell config file(i.e *.bashrc* , *.zshrc* or etc)
```
    export DATABASE_PATH='/path/to/database/'
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
