from django.contrib import admin
from .models import (
    Pod, Employee, Brand, Process, BrandProcessRule,
    EmployeeAssignment, WeeklyOffRule, PublicHoliday,
    LeaveRequest, Roster, RosterEntry, CoverageIssue
)

# Register all models so they appear in the Django Admin panel
admin.site.register(Pod)
admin.site.register(Employee)
admin.site.register(Brand)
admin.site.register(Process)
admin.site.register(BrandProcessRule)
admin.site.register(EmployeeAssignment)
admin.site.register(WeeklyOffRule)
admin.site.register(PublicHoliday)
admin.site.register(LeaveRequest)
admin.site.register(Roster)
admin.site.register(RosterEntry)
admin.site.register(CoverageIssue)