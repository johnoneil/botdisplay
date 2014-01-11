botdisplay
==========

Django based Selenium driven web browser. Selenium drives browser via contents of database configured via Django.

This tool is meant for simple cycling large screen web page displays.


Installation
------------
To install point pip to this github (perhaps as superuser depending upon system)
```
pip install git+https://github.com/johnoneil/botdisplay
```

You can also clone the githup and run the standard setup.py
```
git clone https://github.com/johnoneil/botdisplay
...
cd botdisplay
sudo python setup.py install
```

Running
-------
Installation should give access to two command line tools: botdisplay-django-manage and botdisplay-driver. I'll speak about each in turn

### botdisplay-django-manage
Invoke this command to interact with the django webserver as one would normally use django 'manage.py'. If you're not familiar with initializing and running a django 1.6 web service, then you might want to look into it before running this aplication. However, in brief, the following steps should start up the web server:
```
botdisplay-django-manage syncdb
...
(initialize database sqlite3 file in user's home directory)
...
botdisplay-django-manage runserver
0 errors found
January 11, 2014 - 09:33:33
Django version 1.6.1, using settings 'botdisplay.django_server.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.

```
You can now contact the web server at localhost:8000 or the admin interface via localhost:8000/admin.

### botdisplay-driver
The botdisplay-driver is a simpler application that just looks up the current django webserver database and cycles a browser (firefox) around the URLs within the database. It should pick up database changes as it's updated, but not until the current page has finished displaying.
