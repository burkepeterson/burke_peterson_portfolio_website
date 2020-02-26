from django.shortcuts import render, redirect
from employee_management.forms import EmployeeForm
from employee_management.models import Employee


def employee_list(request):
    context = {'employee_list': Employee.objects.all()}
    return render(request, "employee_list.html", context)


def employee_form_request(request, item_id=0):
    if request.method == "GET":
        if item_id == 0:
            form = EmployeeForm()
        else:
            employee_information = Employee.objects.get(pk=item_id)
            form = EmployeeForm(instance=employee_information)

        context = {'form': form}
        return render(request, "employee_form.html", context)

    else:
        if item_id == 0:
            form = EmployeeForm(request.POST)

        else:
            employee_information = Employee.objects.get(pk=item_id)
            form = EmployeeForm(request.POST, instance=employee_information)

        if form.is_valid():
            form.save()
        else:
            context = {'form': form}
            return render(request, "employee_form.html", context)

        return redirect("/employee/")


def employee_delete(request, item_id):
    employee_information = Employee.objects.get(pk=item_id)
    employee_information.delete()
    return redirect("/employee/")
