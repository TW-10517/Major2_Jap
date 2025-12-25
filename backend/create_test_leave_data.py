#!/usr/bin/env python3
"""
Create Test Leave Data for Notification Testing
Creates an employee with paid leave taken to test the notification
Run: python create_test_leave_data.py
"""

import asyncio
from datetime import date, timedelta
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.database import DATABASE_URL
from app.models import (
    User, UserType, Department, Employee, Role, Manager,
    LeaveRequest, LeaveStatus
)
from app.auth import get_password_hash


async def create_test_leave_data():
    """Create test employee and leave requests"""
    
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        print("\n📊 Creating Test Leave Data for Notification Testing")
        print("=" * 60)

        # Check if test employee exists
        result = await session.execute(
            select(User).filter(User.username == "testemployee")
        )
        test_user = result.scalar_one_or_none()

        if not test_user:
            print("\n❌ Test employee not found!")
            print("   Please create test data using generate_november_2025_data.py first")
            return

        # Get employee record
        emp_result = await session.execute(
            select(Employee).filter(Employee.user_id == test_user.id)
        )
        employee = emp_result.scalar_one_or_none()

        if not employee:
            print("❌ Employee record not found!")
            return

        print(f"\n✅ Found Employee: {employee.employee_id} - {employee.first_name} {employee.last_name}")
        print(f"   Annual Paid Leave Entitlement: {employee.paid_leave_per_year} days")

        # Delete existing leave requests for this employee
        await session.execute(
            select(LeaveRequest).filter(
                LeaveRequest.employee_id == employee.id
            )
        )
        print("\n🧹 Clearing existing leave requests...")

        # Create test leave request - 1 day taken
        print("\n📝 Creating test leave request...")
        today = date.today()
        
        leave = LeaveRequest(
            employee_id=employee.id,
            start_date=today - timedelta(days=5),  # 5 days ago
            end_date=today - timedelta(days=5),     # 1 day leave
            leave_type="paid",
            duration_type="full_day",
            reason="Testing leave notification",
            status=LeaveStatus.APPROVED,
            manager_id=employee.manager_id
        )
        
        session.add(leave)
        await session.commit()

        print(f"   ✅ Created 1-day paid leave (APPROVED)")
        print(f"      Date: {leave.start_date.strftime('%B %d, %Y')}")
        print(f"      Type: Paid Leave")
        print(f"      Status: APPROVED")

        # Get updated statistics
        from sqlalchemy import func
        from app.models import LeaveRequest

        result = await session.execute(
            select(func.sum(
                func.cast(
                    LeaveRequest.end_date - LeaveRequest.start_date + 1,
                    int
                )
            )).filter(
                LeaveRequest.employee_id == employee.id,
                LeaveRequest.leave_type == "paid",
                LeaveRequest.status == LeaveStatus.APPROVED
            )
        )
        total_taken = result.scalar() or 0
        available = max(0, employee.paid_leave_per_year - total_taken)

        print("\n📊 Updated Leave Statistics:")
        print(f"   Total Entitlement: {employee.paid_leave_per_year} days")
        print(f"   Taken (Paid): {total_taken} day(s)")
        print(f"   Available: {available} days")

        print("\n✅ Test Data Created Successfully!")
        print("\n🔍 What to Check:")
        print("   1. Login as testemployee (password: password123)")
        print("   2. Go to Dashboard")
        print("   3. You should see the notification:")
        print(f"      'You have taken {total_taken} day of paid leave.'")
        print(f"      'You have {available} days paid leave available.'")
        print("\n💡 The notification appears when taken_paid_leave <= 1")
        print("   (Shows for 0 or 1 day of leave taken)")


if __name__ == "__main__":
    asyncio.run(create_test_leave_data())
