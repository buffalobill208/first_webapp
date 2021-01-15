from django.db import models
from django.utils import timezone
# import the user authentication module so that we use the built in authentication model in this app
from django.contrib.auth.models import User
from django.contrib import admin
from django.urls import reverse

# Create your models here.
ISSUE_STATUS_CHOICES = (
    ('new', 'New'),
    ('accepted', 'Accepted'),
    ('reviewed', 'Reviewed'),
    ('started', 'Started'),
    ('closed', 'Closed'),
)

OWNER_CHOICES = (
    ('unassigned', 'Unassigned'),
    ('randy', 'Randy'),
    ('casey', 'Casey'),
    ('pearse', 'Pearse'),
)


class Issue(models.Model):
    # requestor will be a foreign key to the User model which is already built-in Django
    requestor = models.ForeignKey(User, on_delete=models.CASCADE)
    # multichoice with defaulting to "new"
    status = models.CharField(max_length=25, choices=ISSUE_STATUS_CHOICES, default='new')
    summary = models.TextField()
    # date time field which will be set to the date time when the record is created
    opened_on = models.DateTimeField('date opened', default=timezone.now)
    modified_on = models.DateTimeField('date modified', auto_now=True)
    owner = models.CharField(max_length=12, choices=OWNER_CHOICES, default='')

    def name(self):
        return self.summary.split('\n', 1)[0]

    def __str__(self):
        return self.requestor

    def __str__(self):
        return self.owner

# Admin front end for the app.  We are also configuring some of the built in attributes for the admin interface on how to display the list, how it will be sorted what are the search fields, etc.


class IssueAdmin(admin.ModelAdmin):     # Need to import above, from django.contrib import admin
    date_hierarchy = 'opened_on'
    list_filter = ('status', 'requestor')
    list_display = ('id', 'name', 'status', 'requestor', 'modified_on', 'owner')
    search_fields = ['description', 'status']
