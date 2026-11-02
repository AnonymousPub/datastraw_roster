from django.db import models

# 1. Pods Table
class Pod(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# 2. Employees Table
class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    pod = models.ForeignKey(Pod, on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Add Pod Lead relationship after Employee model is defined
# (A pod can have a designated lead employee)
Pod.add_to_class('pod_lead', models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='led_pods'))


# 3. Brands Table
class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    client_name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# 4. Processes Table (CS, ACC, NDR, Retention)
class Process(models.Model):
    code = models.CharField(max_length=20, unique=True) # e.g., CS, ACC, NDR, RET
    name = models.CharField(max_length=100) # e.g., Customer Support
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


# 5. Brand Process Rules Table (Minimum staffing requirements per brand & process)
class BrandProcessRule(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='rules')
    process = models.ForeignKey(Process, on_delete=models.CASCADE, related_name='rules')
    min_staffing = models.PositiveIntegerField(default=1)
    operating_days_type = models.CharField(
        max_length=50, 
        choices=[
            ('365_DAYS', '365 Days Operations'),
            ('SUNDAYS_OFF', 'Sundays Off'),
            ('WEEKENDS_OFF', 'Weekends Off')
        ],
        default='SUNDAYS_OFF'
    )

    def __str__(self):
        return f"{self.brand.name} - {self.process.code} (Min: {self.min_staffing})"


# 6. Employee Assignments Table (Which employee can work on which brands/processes)
class EmployeeAssignment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='assignments')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='assigned_employees')
    process = models.ForeignKey(Process, on_delete=models.CASCADE, related_name='assigned_employees')

    class Meta:
        unique_together = ('employee', 'brand', 'process')

    def __str__(self):
        return f"{self.employee} -> {self.brand} [{self.process.code}]"


# 7. Weekly Off Rules Table
class WeeklyOffRule(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='weekly_off_rules')
    rule_type = models.CharField(
        max_length=50,
        choices=[
            ('SUNDAYS_AND_HOLIDAYS', 'Sundays and Public Holidays Off'),
            ('ROTATING_OFFS', 'Rotating Weekly Offs'),
            ('FIXED_WEEKDAYS', 'Fixed Weekday Offs')
        ],
        default='SUNDAYS_AND_HOLIDAYS'
    )
    specific_day = models.CharField(max_length=20, blank=True, null=True) # e.g., 'Saturday' if fixed

    def __str__(self):
        return f"{self.employee} - {self.get_rule_type_display()}"


# 8. Public Holidays Table
class PublicHoliday(models.Model):
    date = models.DateField(unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.date})"


# 9. Leave Requests Table
class LeaveRequest(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leaves')
    start_date = models.DateField()
    end_date = models.DateField()
    leave_type = models.CharField(
        max_length=30,
        choices=[
            ('PL', 'Planned Leave'),
            ('SL', 'Sick Leave'),
            ('COMP_OFF', 'Comp-Off')
        ],
        default='PL'
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', 'Pending'),
            ('APPROVED', 'Approved'),
            ('REJECTED', 'Rejected')
        ],
        default='PENDING'
    )
    reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.employee} ({self.start_date} to {self.end_date}) - {self.status}"


# 10. Rosters Table (Master container for monthly schedules)
class Roster(models.Model):
    title = models.CharField(max_length=100) # e.g., "November 2026 Roster"
    month = models.PositiveIntegerField() # e.g., 11
    year = models.PositiveIntegerField() # e.g., 2026
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# 11. Roster Entries Table (Daily shift assignments per employee)
class RosterEntry(models.Model):
    roster = models.ForeignKey(Roster, on_delete=models.CASCADE, related_name='entries')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='roster_entries')
    date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('WORKING', 'Working'),
            ('WEEKLY_OFF', 'Weekly Off'),
            ('LEAVE', 'On Leave'),
            ('HOLIDAY', 'Public Holiday')
        ],
        default='WORKING'
    )
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    process = models.ForeignKey(Process, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.date} | {self.employee} -> {self.status}"


# 12. Coverage Issues Table (Logs staffing shortages or scheduling conflicts)
class CoverageIssue(models.Model):
    roster = models.ForeignKey(Roster, on_delete=models.CASCADE, related_name='issues')
    date = models.DateField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    process = models.ForeignKey(Process, on_delete=models.CASCADE)
    required_staff = models.PositiveIntegerField()
    available_staff = models.PositiveIntegerField()
    description = models.TextField()
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"CONFLICT: {self.date} | {self.brand} ({self.process.code}) - Req: {self.required_staff}, Avail: {self.available_staff}"