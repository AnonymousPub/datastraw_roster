from datetime import date, timedelta
from django.shortcuts import render, redirect
from .models import (
    Employee, Pod, Brand, Process, BrandProcessRule, 
    EmployeeAssignment, PublicHoliday, LeaveRequest, 
    Roster, RosterEntry, CoverageIssue
)

def dashboard_view(request):
    total_employees = Employee.objects.filter(is_active=True).count()
    total_pods = Pod.objects.count()
    total_brands = Brand.objects.count()
    total_rosters = Roster.objects.count()
    recent_issues = CoverageIssue.objects.all().select_related('roster', 'brand', 'process').order_by('-id')[:5]
    
    context = {
        'total_employees': total_employees,
        'total_pods': total_pods,
        'total_brands': total_brands,
        'total_rosters': total_rosters,
        'recent_issues': recent_issues,
    }
    return render(request, 'roster/dashboard.html', context)

def employee_list_view(request):
    employees = Employee.objects.all().select_related('pod')
    pods = Pod.objects.all()
    context = {'employees': employees, 'pods': pods}
    return render(request, 'roster/employee_list.html', context)

def brand_management_view(request):
    brands = Brand.objects.all()
    processes = Process.objects.all()
    rules = BrandProcessRule.objects.all().select_related('brand', 'process')
    context = {'brands': brands, 'processes': processes, 'rules': rules}
    return render(request, 'roster/brand_management.html', context)

def resource_allocation_view(request):
    assignments = EmployeeAssignment.objects.all().select_related('employee', 'brand', 'process')
    context = {'assignments': assignments}
    return render(request, 'roster/resource_allocation.html', context)

def leave_holiday_view(request):
    holidays = PublicHoliday.objects.all().order_by('date')
    leaves = LeaveRequest.objects.all().select_related('employee').order_by('start_date')
    context = {'holidays': holidays, 'leaves': leaves}
    return render(request, 'roster/leave_holiday.html', context)

def generate_roster_view(request):
    if request.method == 'POST':
        month = int(request.POST.get('month', 11))
        year = int(request.POST.get('year', 2026))
        title = f"Roster - {year}-{month:02d}"

        # Create or get master Roster container
        roster, created = Roster.objects.get_or_create(title=title, defaults={'month': month, 'year': year})
        
        # Clear previous entries and issues to regenerate cleanly
        roster.entries.all().delete()
        roster.issues.all().delete()

        # Get all active employees, holidays, and rules
        employees = Employee.objects.filter(is_active=True)
        holidays_set = set(PublicHoliday.objects.filter(date__year=year, date__month=month).values_list('date', flat=True))
        approved_leaves = LeaveRequest.objects.filter(status='APPROVED', start_date__year=year)
        brand_rules = BrandProcessRule.objects.all().select_related('brand', 'process')

        # Loop through each day of the month
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = date(year, month + 1, 1) - timedelta(days=1)

        current_date = start_date
        while current_date <= end_date:
            is_holiday = current_date in holidays_set
            is_sunday = (current_date.weekday() == 6)

            daily_coverage = {}

            for emp in employees:
                status = 'WORKING'
                assigned_brand = None
                assigned_process = None

                if is_holiday:
                    status = 'HOLIDAY'
                elif is_sunday:
                    status = 'WEEKLY_OFF'
                else:
                    on_leave = any(l.employee == emp and l.start_date <= current_date <= l.end_date for l in approved_leaves)
                    if on_leave:
                        status = 'LEAVE'
                    else:
                        assignment = EmployeeAssignment.objects.filter(employee=emp).first()
                        if assignment:
                            assigned_brand = assignment.brand
                            assigned_process = assignment.process
                            key = (assigned_brand.id, assigned_process.id)
                            daily_coverage[key] = daily_coverage.get(key, 0) + 1

                RosterEntry.objects.create(
                    roster=roster,
                    employee=emp,
                    date=current_date,
                    status=status,
                    brand=assigned_brand,
                    process=assigned_process
                )

            # Coverage Validation
            if not is_holiday and not is_sunday:
                for rule in brand_rules:
                    key = (rule.brand.id, rule.process.id)
                    available_count = daily_coverage.get(key, 0)
                    if available_count < rule.min_staffing:
                        CoverageIssue.objects.create(
                            roster=roster,
                            date=current_date,
                            brand=rule.brand,
                            process=rule.process,
                            required_staff=rule.min_staffing,
                            available_staff=available_count,
                            description=f"Staffing shortage on {current_date}: Required {rule.min_staffing}, got {available_count}."
                        )

            current_date += timedelta(days=1)

        return redirect('roster_view', roster_id=roster.id)

    rosters = Roster.objects.all().order_by('-created_at')
    context = {'rosters': rosters}
    return render(request, 'roster/generate_roster.html', context)

def roster_detail_view(request, roster_id):
    roster = Roster.objects.get(id=roster_id)
    entries = roster.entries.all().select_related('employee', 'brand', 'process').order_by('date', 'employee')
    context = {'roster': roster, 'entries': entries}
    return render(request, 'roster/roster_detail.html', context)