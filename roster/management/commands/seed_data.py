from datetime import date
from django.core.management.base import BaseCommand
from roster.models import Pod, Employee, Brand, Process, EmployeeAssignment, PublicHoliday, LeaveRequest

class Command(BaseCommand):
    help = 'Seeds initial sample data, allocations, holidays, and leaves for DataStraw Smart Roster System'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # 1. Create Processes
        processes_data = [
            {'code': 'CS', 'name': 'Customer Support'},
            {'code': 'ACC', 'name': 'Accounts'},
            {'code': 'NDR', 'name': 'Non-Delivery Report'},
            {'code': 'RET', 'name': 'Retention'},
        ]
        
        proc_objs = {}
        for p in processes_data:
            obj, _ = Process.objects.get_or_create(code=p['code'], defaults={'name': p['name']})
            proc_objs[p['code']] = obj

        # 2. Create Pods & Employees
        alpha_pod, _ = Pod.objects.get_or_create(name='Pod Alpha')
        
        lead_emp, _ = Employee.objects.get_or_create(
            email='lead.alpha@datastraw.com',
            defaults={'first_name': 'Aarav', 'last_name': 'Sharma', 'pod': alpha_pod}
        )
        alpha_pod.pod_lead = lead_emp
        alpha_pod.save()

        employees = []
        for i in range(1, 6):
            emp, _ = Employee.objects.get_or_create(
                email=f'emp{i}.alpha@datastraw.com',
                defaults={'first_name': f'Employee{i}', 'last_name': 'Alpha', 'pod': alpha_pod}
            )
            employees.append(emp)

        # 3. Create Brands
        brands_data = ['Brand Apex', 'Brand Nexus', 'Brand Zenith']
        brand_objs = []
        for b_name in brands_data:
            b_obj, _ = Brand.objects.get_or_create(name=b_name)
            brand_objs.append(b_obj)

        # 4. Create Employee Assignments
        if employees and brand_objs:
            EmployeeAssignment.objects.get_or_create(
                employee=employees[0], brand=brand_objs[0], process=proc_objs['CS']
            )
            EmployeeAssignment.objects.get_or_create(
                employee=employees[1], brand=brand_objs[1], process=proc_objs['ACC']
            )
            EmployeeAssignment.objects.get_or_create(
                employee=employees[2], brand=brand_objs[2], process=proc_objs['NDR']
            )

        # 5. Create Public Holidays
        PublicHoliday.objects.get_or_create(
            date=date(2026, 11, 1),
            defaults={'name': 'Foundation Day', 'description': 'Company annual holiday'}
        )
        PublicHoliday.objects.get_or_create(
            date=date(2026, 11, 15),
            defaults={'name': 'Diwali Holiday', 'description': 'National public holiday'}
        )

        # 6. Create Sample Leave Requests
        LeaveRequest.objects.get_or_create(
            employee=employees[3],
            start_date=date(2026, 11, 10),
            end_date=date(2026, 11, 12),
            defaults={'leave_type': 'PL', 'status': 'APPROVED', 'reason': 'Family function'}
        )

        self.stdout.write(self.style.SUCCESS('Successfully seeded all data including holidays and leaves!'))