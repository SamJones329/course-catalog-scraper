import re

class CourseShort:
  def __init__(self, dept: str, num: int):
    self.dept = dept
    self.num = num

class Course:
  dept: str
  num: int
  name: str
  desc: str
  prereqs: list[CourseShort]
  coreqs: list[CourseShort]

  def __init__(self, text):
    textparts = text.split('\n')
    title = textparts[0]
    body = textparts[1]

    # get department
    match = re.search("[A-Z]{2,4}", title)
    match = match.span()
    self.dept = text[match[0]:match[1]]

    # get course number
    match = re.search("\d{4}", title)
    match = match.span()
    self.num = int(text[match[0]:match[1]])

    # get course name
    match = re.search("(?<=\d{4}\s).*(?=\s\()", title)
    match = match.span()
    self.name = text[match[0]:match[1]]

    # get reqs
    match = re.search("(?<=Prereq\.:).*\.", body)
    if not match:
      self.desc = body
      return
    match = match.span()
    desc = body[match[0]:match[1]]
    match = re.search("\.", desc).span()
    reqs = desc[0:match[0]] # remove period
    desc = desc[match[1]+1:] # remove space after period
    match = re.match("grade of \"[A-DF]\" or better in [A-Z]{2,4} \d{4}", reqs)
    if match:
      match = match.span()
      print(reqs[match[0]:match[1]])

    # reqs = reqs.split('or')

    # get equiv courses
    # an honors course, ...
    # credit will not be given...

    # assign rest to desc

    # print(textparts)


  def __str__(self):
    return f"{self.dept} {self.num}"

if __name__ == "__main__":
  test_str = 'ACCT 2000 Survey of Accounting (3)\nPrereq.: MATH 1021 or MATH 1029 or equivalent. Credit will not be given for both this course and ACCT 2001 or ACCT 2002. Students in nonbusiness curricula are advised to enroll in ACCT 2000 if they are given the option of ACCT 2000 or ACCT 2001, unless they plan to pursue a business degree at a subsequent date. All students in the E. J. Ourso College of Business are required to take ACCT 2001. Introduction to the meaning of the values presented in financial statements; management accounting concepts and internal decision making; fundamentals of individual income taxes.'
  course = Course(test_str)