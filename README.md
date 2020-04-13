# examresults

Welcome, this is a basic Django application. In order to clone/sync and start using/contributing, please proceed as below

- Creating the virtual environment
```
[wpinheir@ironman ~]$ python3.7 -m venv ~/.venv/exam-results
[wpinheir@ironman ~]$ source ~/.venv/exam-results/bin/activate
(exam-results) [wpinheir@ironman ~]$
```

- Creating the code directory
```
(exam-results) [wpinheir@ironman ~]$ mkdir new_projects
(exam-results) [wpinheir@ironman ~]$ cd new_projects/
(exam-results) [wpinheir@ironman new_projects]$ 
```

- Cloning the project
```
(exam-results) [wpinheir@ironman new_projects]$ git clone git@github.com:phess/exam-results.git
Cloning into 'exam-results'...
remote: Enumerating objects: 209, done.
remote: Counting objects: 100% (209/209), done.
remote: Compressing objects: 100% (143/143), done.
remote: Total 209 (delta 91), reused 169 (delta 57), pack-reused 0
Receiving objects: 100% (209/209), 460.31 KiB | 1.48 MiB/s, done.
Resolving deltas: 100% (91/91), done.
(exam-results) [wpinheir@ironman new_projects]$ ll
total 4
drwxrwxr-x. 5 wpinheir wpinheir 4096 Apr 10 13:34 exam-results
(exam-results) [wpinheir@ironman new_projects]$
```

Great, at this moment you are here with the virtual environment created and the project. Let's proceed.

- Installing the requirements
```
(exam-results) [wpinheir@ironman new_projects]$ cd exam-results/
(exam-results) [wpinheir@ironman exam-results]$ pip install -r requirements.txt
...
(exam-results) [wpinheir@ironman exam-results]$ pip install --upgrade pip
```

- Preparing the DB
```
(exam-results) [wpinheir@ironman exam-results]$ cd examresults/
(exam-results) [wpinheir@ironman examresults]$ ./manage.py makemigrations lab_use
(exam-results) [wpinheir@ironman examresults]$ ./manage.py migrate
```

- And now, starting the server
```
(exam-results) [wpinheir@ironman examresults]$ ./manage.py runserver
```

here is the expected output
```
(exam-results) [wpinheir@ironman examresults]$ ./manage.py runserver
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
April 10, 2020 - 20:37:25
Django version 3.0.5, using settings 'examresults.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

In order to access the admin console via `http://localhost:8000/admin/` you have to follow the steps below

- Creating the admin user
```
$ ./manage.py createsuperuser --username admin --email admin@admin.local
```

Once you proceed with changes on the `models.py`, proceed as below to update the DB schema
```
(exam-results) [wpinheir@ironman examresults]$ ./manage.py makemigrations
(exam-results) [wpinheir@ironman examresults]$ ./manage.py migrate
```

- If you would like to complement adding the translation to pt_BR, you should
  - Run the command below to create the file `exam-results/examresults/locale/pt_BR/LC_MESSAGES/django.po`
```
(exam-results) [wpinheir@ironman examresults]$ ./manage.py makemessages
```
  - Add the entry related to your translation
  - Run the commands below
```
(exam-results) [wpinheir@ironman examresults]$ ./manage.py compilemessages
```
After that, you should be able to see the translated text on your browser.


I hope you enjoy it.

Best