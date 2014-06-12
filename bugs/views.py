## views
from .models import Bugs
from django.shortcuts import render
import json
from django.http import HttpResponse
from django.db.models import Count

def landing(request):
	manager_ids = Bugs.objects.values('manager_id').annotate(mcount=Count('manager_id'))

	context = {"status" : "under construction",
				"manager_ids" : [m['manager_id'] for m in manager_ids]}

	return render(request, 'landing.html', context)

def dataview(request):
	managers = request.GET.get('managers', None)
	severity = request.GET.get('severity', None)
	product = request.GET.get('product', None)
	status = request.GET.get('status', None)
	age = request.GET.get('age', None)

	bugs = Bugs.objects.all()

	if managers != None:
		managers = managers.split(',')
		bugs = bugs.filter(manager_id__in=managers)

	if severity != None:
		severity = severity.split(',')
		bugs = bugs.filter(severity__in=severity)

	if product != None:
		product = product.split(',')
		bugs = bugs.filter(product__in=product)

	if status != None:
		status = status.split(',')
		bugs = bugs.filter(status__in=status)



	matrix_data = []
	formatted_data = {}
	for bug in bugs:
		bug_date = bug.entry_date.strftime("%B")
		if bug_date not in formatted_data:
			formatted_data[bug_date] = {}

		severity = str(bug.severity)
		if severity not in formatted_data[bug_date]:
			formatted_data[bug_date][severity] = 0

		formatted_data[bug_date][severity] += 1
	
	matrix_data.append(['Bug File Date', '1', '2', '3', '4', '5', '6'])
	for bug_date, severities in formatted_data.iteritems():
		matrix_data.append([bug_date,
							severities.get('1', 0),
							severities.get('2', 0),
							severities.get('3', 0),
							severities.get('4', 0),
							severities.get('5',0),
							severities.get('6',0),
						])


	return HttpResponse(json.dumps(matrix_data), mimetype="application/json")