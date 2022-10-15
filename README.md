# Course Catalog Scraper
Python web scraper to extract class and course data from the [LSU General Catalog](https://www.lsu.edu/academics/catalogs.php)

System Requirements
- Python 3
- Chromedriver

Provided you have Python 3 installed, you can create and activate an environment with all the requirements by running these commands from the root project folder:

`python -m venv .`

`pip install -r requirements.txt`

(for Mac/Linux) `source ./bin/active`

(for Windows Powershell) `./bin/Activate.ps1`

To run the scraper yourself, simply run `python main.py` from a terminal in the root directory of the project. Make sure to set the `USE_CSV` variable in `main.py` to your desired value, as this determines whether the scraper will open a chromedriver instance or read from `rawcoursedata.csv`.
