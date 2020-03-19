from django.db import models


class Position(models.Model):
    title = models.CharField(max_length=50)
    manager_position = models.BooleanField()
    color = models.CharField(max_length=50)

    def __str__(self):
        return self.title


emp_code_choices = (
    ("IC ", "Contractor"),
    ("FTE", "Full Time"),
)


class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=12)
    email_address = models.EmailField(max_length=50)
    emp_code = models.CharField(max_length=3, choices=emp_code_choices, default="FTE")
    position = models.ForeignKey(Position, on_delete=models.PROTECT)
    manager_name = models.ForeignKey("self", on_delete=models.SET_NULL, null=True,
                                     limit_choices_to={"position__manager_position": 1})

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


class Calendar(models.Model):
    title = models.CharField(max_length=50)
    start = models.CharField(max_length=255)
    end = models.CharField(max_length=255)
    allDay = models.BooleanField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
