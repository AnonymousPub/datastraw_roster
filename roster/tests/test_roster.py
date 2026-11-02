from datetime import date
import pytest
from roster.models import Employee, Pod, Brand, Process, Roster, RosterEntry

@pytest.mark.django_db
def test_employee_creation():
    pod = Pod.objects.create(name="Test Pod")
    emp = Employee.objects.create(
        first_name="Test",
        last_name="User",
        email="test.user@datastraw.com",
        pod=pod
    )
    assert emp.first_name == "Test"
    assert emp.pod.name == "Test Pod"
    assert emp.is_active is True

@pytest.mark.django_db
def test_brand_and_process_creation():
    brand = Brand.objects.create(name="Test Brand")
    process = Process.objects.create(code="TS", name="Test Support")
    
    assert brand.name == "Test Brand"
    assert process.code == "TS"

@pytest.mark.django_db
def test_roster_container_creation():
    roster = Roster.objects.create(title="Roster - 2026-11", month=11, year=2026)
    assert roster.month == 11
    assert roster.year == 2026