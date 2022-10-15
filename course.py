import re

class Course:
  dept: str
  num: int
  name: str = "No title provided"
  desc: str = "No description provided"
  reqs: str = "No listed prerequisites"

  def __init__(self, text):
    if type(text) == float:
      print(text)
      return
    textparts = text.split('\n')
    title = textparts[0]
    if len(textparts) == 1:
      body = None
    else:
      body = textparts[1]

    # get department
    match = re.search(r"[A-Z]{2,4}|Hist", title) # there's a type where one department with the HIST prefix is not all caps
    if match:
      match = match.span()
      self.dept = text[match[0]:match[1]]
    else:
      print(f"no dept for {text}")

    # get course number
    match = re.search(r"\d{4}", title)
    match = match.span()
    self.num = int(text[match[0]:match[1]])

    # get course name
    match = re.search(r"(?<=\d{4}\s).*(?=\s\()", title)
    if match:
      match = match.span()
      self.name = text[match[0]:match[1]]

    # get reqs
    if body is not None:
      match = re.search(r"(?<=Prereq\.:).*\.", body)
      if not match:
        # print(f"{self.dept}{self.num} prereqs: N/A")
        self.desc = body
        return
      match = match.span()
      desc = body[match[0]:match[1]]
      match = re.search("\.", desc).span()
      reqs = desc[0:match[0]] # remove period
      desc = desc[match[1]+1:] # remove space after period
      self.desc = desc
      self.reqs = reqs


    # reqs = re.sub(
    #   r'grade of (“[A-DF]”)\s?or (?:above|better)', r'\1', 
    #   reqs)
    # splitreqs = re.split(';|,', reqs)
    # print(splitreqs)

    # matches = re.findall("[A-Z]{2,4} \d{4}", reqs)
    # print(f"{self.dept}{self.num} prereqs: {matches}")
    # if not matches: print(reqs)

    # reqs = reqs.split('or')

    # get equiv courses
    # an honors course, ...
    # credit will not be given...

    # assign rest to desc

    # print(textparts)


  def __str__(self):
    return f"{self.dept} {self.num}"

if __name__ == "__main__":
  test_str = "ACCT 3001 Intermediate Accounting–Part I (3)\nAn honors course, ACCT 3002, is also available. Prereq.: grade of “C” or above in ACCT 2101; MATH 1431. Only Accounting and Finance students admitted to the College of Business or permission of department. Credit will not be given for both this course and ACCT 3002 or ACCT 7011. Accounting principles underlying preparation of financial statements; their application in measurement and reporting of selected balance-sheet items and related revenue and expense recognition."
  course = Course(test_str)