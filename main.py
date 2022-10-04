from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep

def get_text_from_row(row: WebElement, err_depth=0, max_err_depth=3):
  # print("processing row", row)
  try:
    textdiv = row.find_element(
      By.CSS_SELECTOR, 
      'td>div:nth-child(2)')
    return textdiv.text
  except Exception:
    if err_depth == max_err_depth:
      return None
    # print("Couldn't find row expansion, clicking again")
    anchor = row.find_element(By.TAG_NAME, 'a')
    anchor.click()
    sleep(0.2)
    return get_text_from_row(row, err_depth+1)

def extract_page_courses(driver: webdriver.Chrome):
  # table containing class info has class table_default
  elems = driver.find_elements(By.CLASS_NAME, "table_default")

  # last table.table_default on page is the one we want
  elem = elems[-1]

  # get all rows of table with an anchor tag (opens description)
  rows = elem.find_elements(By.CSS_SELECTOR, 'tr:has(a)')

  # extract page nav (last row)
  pagenavrow = rows[-1]

  # remove page nav from rows
  rows = rows[:-1]

  # click all anchor tags in the rows we want to open their descriptions
  sleepscale = 1
  for row in rows: 
    anchor = row.find_element(By.TAG_NAME, 'a')
    anchor.click()
    # progressively sleep slightly longer after each click so browser can process
    # may need to modify these values for yourself 
    sleep(0.05 * sleepscale)
    sleepscale += 0.02
  
  # extract text info to parse for each class
  classContents = []
  for row in rows:
    # print(row)
    classContents.append(get_text_from_row(row))
    # textdiv = row.find_element(
    #   By.CSS_SELECTOR, 
    #   'td>div:nth-child(2)')
    # classContents.append(textdiv.text)
    # print(textdiv.text)
  return classContents


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

  # Need to install chromium driver and add to path for this
  driver = webdriver.Chrome()

  # General Catalog 2022-23
  driver.get("https://catalog.lsu.edu/content.php?catoid=25&navoid=2277")

  courseTexts = extract_page_courses(driver)

  # for e in elem: print(e.text)
  # content = driver.page_source
  # soup = BeautifulSoup(content)
  # data = soup.find("table", {"class": "table_default"})
  # print(data.prettify())
  driver.close()
  driver.quit()