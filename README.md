# Smart Courses API

MVP application with a set of CRUD endpoints for managing course entities.

Code was formatted with black, linted with .flake8 and covered in tests.

## Stack

* **Django** (*DRF*)
* **Sqlite**
* **Docker**/**docker-compose**


## Local running

To run this project locally you need to: 

* Clone it first: `git clone https://github.com/RedBullDogE/smart-courses-api`

* Setup env file at your discretion or use the default one.

* Run: `docker-compose up -d`

* Apply migrations: `docker-compose exec web python manage.py migrate`

* Done! Now you can access your application via http://localhost:8000/api/
