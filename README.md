# 2018_02_16_python_projet_5
This project is part of 'DA-Python' path of OpenClassrooms platform : Project_5 : 'Let's use public data of OpenFoodFacts platform !'

The application created here helps you to improve your food choices, giving you an alternative product to the unhealthy product you submit. It also provides stores information so you can easily find it.
Note that this application was primarily designed for French consumers, so it mainly contains French products, sold in French stores.

This application needs to prior installation of MySQL. If not already completed, please visit : https://dev.mysql.com/doc/refman/5.7/en/installing.html

When it is done, please follow these few more steps :
- Clone this repository on your own computer
- Download the last version of python 3 for your operating system, see : https://www.python.org/
- Create a new virtual environment :
    - 'py -3 -m venv env' (for Windows)
    - 'python3 -m venv env' (for other os)
- Activate the virtual environment : 'source env/bin/activate'
- Install the dependancies : 'pip install -r requirements.txt'
- Open 'params.py.dist' file, replace identifier and password as required and rename file as 'params.py' (i.e. just remove '.dist' extension)
- At first use, execute 'app.py' file with '--db_create' argument (this will create a local MySQL database and fill it with 'OpenFoodFacts' data) :
    - 'py -3 app.py --db_create' (for Windows)
    - 'python3 app.py --db_create' (for other os)
- For further uses, forgot '--db_create' argument, just execute 'app.py'
- Note that the application launches a database update if delay from last update is greater than 7 days
- Nevertheless, manual update can be forced using '--db_update' argument while executing 'app.py' file
- Ready to eat better :-)
