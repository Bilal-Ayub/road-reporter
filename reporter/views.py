from django.shortcuts import render, redirect
from .models import Report
from .forms import ReportForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from .forms import LoginForm, ReportForm, LoginForm, RegistrationForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
import folium
import logging

# Create your views here.
def index(request):
    return render(request, 'reporter/index.html')

def map_view(request):
    all_reports = Report.objects.all()

    # create a folium map centered on Karachi
    my_map = folium.Map(location=[24.916452, 67.042635], zoom_start=10)

    # add a marker to the map for each report
    for report in all_reports:
        coordinates = (report.location_lat, report.location_lon)
        popup_content = f"Report: {report.report_type}<br>Resolved: {'Yes' if report.is_resolved else 'No'}"
        folium.Marker(coordinates, popup=popup_content).add_to(my_map)

    context = {'map': my_map._repr_html_()}
    return render(request, 'reporter/map_view.html', context)

def recursive_sort(reports):
    # Base case: if the list is empty or has one element, it's already sorted
    if len(reports) <= 1:
        return reports

    # Choose the pivot (here we take the first element)
    pivot = reports[0]
    less_than_pivot = []
    greater_than_pivot = []

    # Recursive case: separate reports into two lists
    for report in reports[1:]:
        if report.priority < pivot.priority:
            less_than_pivot.append(report)
        else:
            greater_than_pivot.append(report)

    # Combine the sorted lists
    return recursive_sort(less_than_pivot) + [pivot] + recursive_sort(greater_than_pivot)

def paginate_reports(request):
    reports = Report.objects.all()
    page_size = 5  # Number of reports per page
    total_reports = reports.count()
    page_number = int(request.GET.get('page', 1))
    start_index = (page_number - 1) * page_size

    # Create a list to hold the paginated reports
    paginated_reports = []

    # Initialize a counter for the current index
    index = start_index

    # Use a for loop to iterate over the reports starting from start_index
    for _ in range(start_index, total_reports):
        # Use a while loop to add reports to the paginated list
        while len(paginated_reports) < page_size and index < total_reports:
            paginated_reports.append(reports[index])
            index += 1  # Move to the next report

        # Break the for loop once we have enough reports for the page
        if len(paginated_reports) >= page_size:
            break

    # Sort the paginated reports using the recursive_sort function
    sorted_paginated_reports = recursive_sort(paginated_reports)

    # Calculate total pages
    total_pages = (total_reports // page_size) + (1 if total_reports % page_size > 0 else 0)

    # Render the paginated reports in the template
    context = {
        'reports': sorted_paginated_reports,  # Use sorted reports
        'current_page': page_number,
        'total_pages': total_pages,
    }
    return render(request, 'reporter/paginated_reports.html', context)

def reports(request):
    """Show all reports sorted by priority."""
    reports = Report.objects.all()
    sorted_reports = recursive_sort(list(reports))  # Sort reports using recursion

    context = {'reports': sorted_reports}
    return render(request, 'reporter/reports.html', context)


def new_report(request):
    """Add a new report"""
    if request.method != 'POST':
        # No data was submitted, create a blank form
        form = ReportForm()
    else:
        # POST data submitted, process data
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('reporter:reports')

    # Create a list of priorities
    priorities = list(range(1, 11))  # Generates [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    # Display a blank or invalid form.
    context = {'form': form, 'priorities': priorities}
    return render(request, 'reporter/new_report.html', context)

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('reporter:reports')  # Redirect to the reports page after login
    else:
        form = LoginForm()
    return render(request, 'reporter/login.html', {'form': form})

logger = logging.getLogger(__name__)

from django.contrib import messages

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user
            # Generate a success message with the username
            messages.success(request, f'Account created successfully! Your username is: {user.username}')
            return redirect('reporter:login')  # Redirect to login after registration
    else:
        form = RegistrationForm()
    return render(request, 'reporter/register.html', {'form': form})
