
[![forthebadge](https://forthebadge.com/images/badges/cc-0.svg)](https://forthebadge.com) 
[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/uses-css.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/uses-js.svg)](https://forthebadge.com)

# vigilant-broccoli

## How to install locally your project

Prerequisites : you need to have installed git, pipenv and postgresql on your machine
(If you are on windows we suggest you run all these commands in WSL).

1. Get your repo locally by running : `git clone https://github.com/Kariss83/vigilant-broccoli.git`.
2. Install all dependencies using pipenv (previously installed using pip) : `pipenv install`.
3. Create a postgresql DB named `purbeurredb2` on you computer.
4. Set up your environnement variables in a .env file at the root of your project.
    - DB_USER='your_db_user'
    - DB_PWD='users_db_pwd'
5. Set the virtual environment by running : `pipenv shell`
6. Start the server using `python manage.py runserver` ou `python3 manage.py runserver`
    - (optionnal) If you try to launch the app for the first time you'll need to populate the DB by running `python manage.py populatedb` ou `python3 manage.py populatedb` (this operation might take some time, please wait for the success message to pop).
7. You can now go to the page http://127.0.0.1:8000 and have fun on your PurBeurre app.

## How to launch tests
1. If you want to just run the tests after you've initiated your virtual environment, you can run : `python manage.py test`
2. If you want something with a bit more verbosity and to check coverage.
    - you can create a file called 'coverage.sh' at the root of the project that contains the following:
    ```
    #!/bin/sh
    set -e  # Configure shell so that if one command fails, it exits
    coverage erase
    coverage run manage.py test --verbosity 2
    coverage report
    ```
    - make it executable using : `chmod +x coverage.sh`
    - run the command : `./coverage.sh`
3. 



## Technologies
- Python --> Django
- CSS --> Bootstrap
- JS

## Authors

Romain VACHE

## Licensing

This project was built under the Creative Commons licence.