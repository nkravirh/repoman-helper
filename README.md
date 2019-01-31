# repoman-helper

```
git clone git@github.com:nkravirh/repoman-helper.git
cd repoman-helper
```

### update code/config.ini with your credentials
```
vi code/config.ini
```

### Install requirements 

```
pip install -r requirements.txt
```

### run code
```
python3 code/repoman-solver.py AUTHN-5432
```

### This will do the following
* scan JIRA ticket for github repo
* fork repo
* clone repo to local
* create branch
* update repoman with possible values (help to fix the issue)



