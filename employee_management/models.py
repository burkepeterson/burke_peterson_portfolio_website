from django.db import models


class Position(models.Model):
    title = models.CharField(max_length=50)
    manager_position = models.BooleanField()

    def __str__(self):
        return self.title


class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=12)
    email_address = models.EmailField(max_length=50)
    emp_code = models.CharField(max_length=3)
    position = models.ForeignKey(Position, on_delete=models.PROTECT)
    manager_name = models.ForeignKey("self", on_delete=models.SET_NULL, null=True,
                                     limit_choices_to={"position__manager_position": 1})

    def __str__(self):
        return self.first_name + ' ' + self.last_name
