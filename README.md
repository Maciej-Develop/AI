```
python -m venv .venv
set-ExecutionPolicy Unrestricted -Scope Process
pip install -r .\requirements.txt
.\.venv\Scripts\activate
python .\pacman.py
```

To make requirements.txt :
```
pip freeze > requirements.txt
```
