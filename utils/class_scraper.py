from bs4 import BeautifulSoup
from requests import get
import datetime


class Course:
	def __init__(self, name, number, department, pk):
		self.name = name
		self.number = number # just the number
		self.department = department # just the abbreviation
		self.pk = pk
	def __str__(self):
		return "{}|{}|{}".format(self.number, self.name, self.department)
	def json(self):
		json_template = "{{\"model\": \"social_match.course\",\"pk\": {},\"fields\": {{\"department\": \"{}\",\"number\": {},\"name\": \"{}\"}}}}"
		return json_template.format(self.pk, self.department, self.number, self.name.replace("\"", "\\\""))

# full catalog url
url = "https://rabi.phys.virginia.edu/mySIS/CC2/CS.html"

# small test catalog url
# url = 'https://rabi.phys.virginia.edu/mySIS/CS2/page.php?Semester=1192&Type=Group&Group=CogSci'

response = get(url)

classes_soup = BeautifulSoup(response.text, 'html.parser')

classes_container = classes_soup.select('table')[1]

department_names = classes_container.find_all("td", class_='UnitName')

# dictionary to match abbreviations with course names
# departments = {}
#
# for dept_td in department_names:
# 	dept_name = dept_td.text.strip()
# 	dept_abbrev_line = dept_td.parent.next_sibling.next_sibling.text
# 	dept_abbrev = dept_abbrev_line.split(" ")[0].strip()
# 	departments[dept_abbrev] = dept_name

class_nums = classes_container.find_all("td", class_='CourseNum')

# list of all Course objects
classes = []
count = 0
for i in range(len(class_nums)):
	class_num_td = class_nums[i]
	class_num_tr = class_num_td.parent

	# contains semesters the class was offered
	class_was_offered = class_num_tr.next_sibling.next_sibling.find("div", class_='CourseWasOffered')

	# assume class is old if no past offering dates found
	recent_years = [i for i in range(datetime.datetime.now().year, datetime.datetime.now().year-5, -1)]

	if class_was_offered:
		offered_recently = False
		for y in recent_years:
			if str(y) in class_was_offered.text:
				offered_recently = True
		if not offered_recently:
			continue

		try:
			class_num = int(class_num_td.text.strip().split(" ")[1])
		except ValueError: # skip weird transfer class credits (X000T)
			continue
		class_name = class_num_td.next_sibling.text.split("(")[0].strip() # remove parenthesized credit amounts from this string
		class_dept = class_num_td.text.strip().split(" ")[0]
		course = Course(name=class_name, department=class_dept, number=class_num, pk=count+1)
		classes.append(course)
		count += 1

with open('../social_match/fixtures/class_data.json', 'w') as file:
	file.write("[")
	for c in classes[:-1]:
		file.write(c.json()+',')
	file.write(classes[-1].json())
	file.write(']')

print()