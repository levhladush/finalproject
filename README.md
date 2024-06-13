# Employee Tree


## Реалізовано

- Web page with a hierarchy of employees
- Ability to automatically populate the database using DB seed
- Web page with complete information about each employee
- CRUD operations for each employee on the List and Create pages
- Sorting by selected fields without reloading the page using DataTable lib
- User authentication and restriction of page access without authorization

## Installation


```sh
python3 -m venv venv
source venv/bin/activate
cd final_project
pip install -r requirements.txt
python3 manage.py runserver
```

How to fill the database:

```sh
python3 manage.py migrate
python3 manage.py seed [number of employee]
```



