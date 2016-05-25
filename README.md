Coppers
=======

Something to help you figure out where the hell you're spending all that money.

Made with Django (and love).

Install & Run
-------------

1. Clone it from Github

	```
	$ git clone https://github.com/bteixeira/coppers.git
	$ cd coppers
	```

2. Install Django and other dependencies. It's probably a good idea to do it in a VirtualEnv:

	```
	$ virtualenv env
	$ source env/bin/activate
	$ pip install -r requirements.txt
	```

3. Initialize the database. Without any configuration, this will use a local instance of SQLite (using other DBs probably requires installing additional libraries)

	```
	$ ./manage.py migrate
	```

4. Create an admin user for Django Admin:

	```
	$ ./manage.py createsuperuser
	```

5. Start the development server

	```
	$ ./manage.py runserver
	```

6. Go to [http://localhost:8000/](http://localhost:8000/) and log in with the admin account you just created. Have fun!

7. Optionally, go to [http://localhost:8000/admin](http://localhost:8000/admin) and create other users
