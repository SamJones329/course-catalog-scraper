from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

if __name__ == "__main__":
  # find elem table.table_default
  # table rows will be course names with anchor tags that load course info
  # last table row has page nav with 
  # skip table rows that describe categories
  # prereqs indicated with "Prereq.:AAA0000" coreq is similarly structures, data ends at first period after "Prereq.:"
  # multiple prereqs separate with "or"
  # semi-equivalent courses notated with "Credit will not be given for both this course and DEPT ####[ or DEPT ####]."
  # min grade in prereq indicated as - "grade of "C" or better in DEPT ####[, DEPT ####]"
  # if pre/coreq contains lists, they will be separated with ;
  # for multiple options this, this, or that
  # Course name structured as - DEPT #### Course Name (#)
  # first #### indicates course #, second indicates # hrs
  driver = webdriver.Chrome()
  driver.get("https://catalog.lsu.edu/content.php?catoid=25&navoid=2277")
  content = driver.page_source
  soup = BeautifulSoup(content)
  print(soup)
  pass