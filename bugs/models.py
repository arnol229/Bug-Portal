from django.db import models

class Bugs(models.Model):
	bug_id = models.CharField(max_length=64, db_index=True)
	manager_id = models.CharField(max_length=16, db_index=True)
	entry_date = models.DateTimeField(auto_now=False)
	age = models.IntegerField()
	status = models.CharField(max_length=8)
	severity = models.IntegerField()
	product = models.CharField(max_length=36)
	is_open = models.BooleanField(default=False)
	month_start = models.BooleanField(default=False)

	def to_json(self):
		return {
		'bug_id':self.bug_id,
		'manager_id':self.manager_id,
		'entry_date':self.entry_date.isoformat(),
		'age':self.age,
		'status':self.status,
		'severity':self.severity,
		'product':self.product,
		'is_open':self.is_open,
		'month_start':self.month_start
		}
