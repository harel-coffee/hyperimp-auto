import openml

def generate(studyid):
	tasks = openml.study.get_study(studyid).tasks
	for task in tasks:
		yield (task,)