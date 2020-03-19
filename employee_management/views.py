from django.shortcuts import render, redirect
from employee_management.forms import EmployeeForm, CalenderEventForm
from employee_management.models import Employee, Calendar


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


def calendar(request):
    if request.method == "POST":
        item_id = request.POST.get("item_id")
        if item_id is not None:
            event_information = Calendar.objects.get(pk=item_id)
            info = request.POST.copy()
            info["employee"] = info.get("employee", event_information.employee_id)
            form = CalenderEventForm(info, instance=event_information)
        else:
            form = CalenderEventForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            print(request.POST)
        context = {}
    else:
        context = {"events_list": Calendar.objects.select_related(), "employees": Employee.objects.all()}
    return render(request, "employee_calendar.html", context)


def calendar_delete(request, item_id):
    calendar_information = Calendar.objects.get(pk=item_id)
    calendar_information.delete()
    return redirect("/employee/calendar/")
