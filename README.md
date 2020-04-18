# crowdsourcing-text-msg

#How to start (Part A)

- Clone this repository by running the following command (copy and paste the command to your Terminal)
```bash
git clone https://github.com/aiformankind/crowdsourcing-text-msg.git && git checkout dev && cd crowdsourcing-text-msg
```
or
```bash
git clone git@github.com:aiformankind/crowdsourcing-text-msg.git && gut cgecjiyt dev && cd crowdsourcing-text-msg
```

- This repository needs Python 3.6 and up to run

- Suggestion: set up the python virtual environment, here is the reference:
https://docs.python.org/3.6/library/venv.html

- Install all the python dependency package by run the following command:
```.bash
pip3 install -r requirements.txt
```

# How to start (Part B)

- If this is your first time to use this repository, we need to install our SQLite and create the necessary table. 
```bash
# please adjust your path if you are on Windows OS. 
python src/database_setup.py
```

##Note: We will use the dev branch as a development branch.