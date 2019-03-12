def majors_to_models(list_path, fixture_path):
	json_template = "{{\"model\": \"social_match.major\",\"pk\": {},\"fields\": {{\"name\": \"{}\"}}}}"

	names = []
	with open(list_path) as list_file:
		i = 0
		for line in list_file:
			i += 1
			names.append(line.strip())

	with open(fixture_path, 'w') as file:
		file.write("[")
		for i in range(len(names[:-1])):
			file.write(json_template.format(i+1, names[i])+',')
		file.write(json_template.format(len(names), names[-1]))
		file.write("]")

def minors_to_models(list_path, fixture_path):
	json_template = "{{\"model\": \"social_match.minor\",\"pk\": {},\"fields\": {{\"name\": \"{}\"}}}}"

	names = []
	with open(list_path) as list_file:
		i = 0
		for line in list_file:
			i += 1
			names.append(line.strip())

	with open(fixture_path, 'w') as file:
		file.write("[")
		for i in range(len(names[:-1])):
			file.write(json_template.format(i+1, names[i])+',')
		file.write(json_template.format(len(names), names[-1]))
		file.write("]")

majors_to_models("major_list.json", "../social_match/fixtures/major_data.json")
minors_to_models("minor_list.json", "../social_match/fixtures/minor_data.json")
