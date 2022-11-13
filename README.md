# Team *Kangaroo* Small Group project

## Team members
The members of the team are:
- *Ubayd Khan* ([ubayd.khan@kcl.ac.uk](ubayd.khan@kcl.ac.uk))
- *Erikas Staugas* ([erikas.staugas@kcl.ac.uk](erikas.staugas@kcl.ac.uk))
- *Krishna Prasanna Kumar* ([krishna.prasanna_kumar@kcl.ac.uk](krishna.prasanna_kumar@kcl.ac.uk)) 
- *Matushan Yogaraj* ([matushan.yogaraj@kcl.ac.uk](matushan.yogaraj@kcl.ac.uk))
- *Tri Pham* ([tri.pham@kcl.ac.uk](tri.pham@kcl.ac.uk))

## Project structure
The project is called `msms` (Music School Management System).  It currently consists of a single app `lessons` where all functionality resides.
**A project description can be found in the `PROJECT.md` file.**

## Deployed version of the application
The deployed version of the application can be found at *<[enter URL here](URL)>*.

## Installation instructions
To install the software and use it in your local development environment, you must first set up and activate a local development environment.  From the root of the project:

```
$ virtualenv venv
$ source venv/bin/activate
```

Install all required packages:

```
$ pip3 install -r requirements.txt
```

Migrate the database:

```
$ python3 manage.py migrate
```

Seed the development database with:

```
$ python3 manage.py seed
```

Run all tests with:
```
$ python3 manage.py test
```
## Deployment instructions

Migrate models into database schema:
(You may need to run ```makemigrations``` first.)

```
$ python3 manage.py migrate
```

Run the server:

```
$ python3 manage.py runserver
```

*The above instructions should work in your version of the application.  If there are deviations, declare those here in bold.  Otherwise, remove this line.*

## Sources
The packages used by this application are specified in `requirements.txt`

*Declare other sources here.*
