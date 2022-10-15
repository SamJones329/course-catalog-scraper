from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
import pandas as pd
from time import sleep, perf_counter
from course import Course

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

  # get page num and next page and print progress
  curpage = pagenavrow.find_element(By.CSS_SELECTOR, 'span[aria-current=page]')
  try:
    lastpage = pagenavrow.find_element(By.CSS_SELECTOR, 'a:last-child')
    nextpage = pagenavrow.find_element(By.CSS_SELECTOR, 'span[aria-current=page]+a')
  except Exception:
    lastpage = curpage
    nextpage = None
  print(f"Processing page {curpage.text}/{lastpage.text}...")

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
    classContents.append(get_text_from_row(row))
  
  more_pages = False
  if nextpage:
    more_pages = True
    nextpage.click()
    sleep(5) # sleep for 5 seconds to let page load

  return more_pages, classContents

USE_CSV = True
RAW_DATA_FILE = 'rawcoursedata.csv'
PROC_DATA_FILE = 'coursedata.csv'
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

  start = perf_counter()
  print()
  if USE_CSV:
    print('Reading raw data from csv...')
    df = pd.read_csv(RAW_DATA_FILE)
    coursetexts = df['coursetext'].values.tolist()
  else: 
    # Need to install chromium driver and add to path for this
    print('Starting driver...')
    driver = webdriver.Chrome()

    # set implicit wait time
    driver.implicitly_wait(1)

    # General Catalog 2022-23
    print('Opening course catalog...')
    driver.get("https://catalog.lsu.edu/content.php?catoid=25&navoid=2277")

    print('Extracting course data...')
    coursetexts = []
    is_more_pages = True
    while is_more_pages:
      is_more_pages, page_courses = extract_page_courses(driver)
      coursetexts += page_courses

    print('Closing driver...')
    driver.close()
    driver.quit()

    print('Writing raw data...')
    ctdf = pd.DataFrame(coursetexts, columns=['coursetext'])
    ctdf.to_csv(RAW_DATA_FILE)

  print('Processing raw data...')
  badelems = []
  for idx, text in enumerate(coursetexts):
    if type(text) != str:
      badelems.append(idx)
      print(f'Found non string value: {text}; is probably the general reqs listed for all CHE classes')

  badelems = list(reversed(badelems))
  for elem in badelems:
    if elem == 0:
      coursetexts = coursetexts[elem+1]
    elif elem == len(coursetexts) - 1:
      coursetexts = coursetexts[:elem]
    else:
      coursetexts = coursetexts[:elem] + coursetexts[elem+1:]

  courses = [Course(text) for text in coursetexts]

  print('Writing processed data...')
  courses = [
    [course.dept, course.num, course.name, course.desc, course.reqs] 
    for course in courses]
  courses = pd.DataFrame(data=courses, columns=['Dept', 'Num', 'Name', 'Desc', 'Reqs'])
  courses.to_csv(PROC_DATA_FILE)

  print('Done! Processed data can be found in coursedata.csv')

  end = perf_counter()
  duration = end - start
  minutes = int(duration // 60)
  seconds = duration % 60
  print(f"Finished in {minutes} minutes and {seconds:.2f} seconds\n")
  # TODO - also extract actual names of prefixes maybes