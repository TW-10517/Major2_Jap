#!/usr/bin/env python3
"""
Test script to verify notifications are created when:
1. Manager approves/rejects leave requests
2. Manager approves/rejects comp-off requests  
3. Manager approves/rejects overtime requests
"""

import asyncio
import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"

def test_with_api():
    """Test using API calls"""
    print("=" * 80)
    print("NOTIFICATION SYSTEM TEST")
    print("=" * 80)
    
    # Step 1: Get a manager token
    print("\n[1] Getting manager credentials...")
    manager_login = requests.post(
        f"{BASE_URL}/token",
        data={"username": "mgr1", "password": "password"}
    )
    
    if manager_login.status_code != 200:
        print(f"❌ Manager login failed: {manager_login.text}")
        return
    
    manager_token = manager_login.json()["access_token"]
    manager_headers = {"Authorization": f"Bearer {manager_token}"}
    print(f"✅ Manager logged in: mgr1")
    
    # Step 2: Get an employee token
    print("\n[2] Getting employee credentials...")
    employee_login = requests.post(
        f"{BASE_URL}/token",
        data={"username": "emp1", "password": "password"}
    )
    
    if employee_login.status_code != 200:
        print(f"❌ Employee login failed: {employee_login.text}")
        return
    
    employee_token = employee_login.json()["access_token"]
    employee_headers = {"Authorization": f"Bearer {employee_token}"}
    print(f"✅ Employee logged in: emp1")
    
    # Step 3: Check initial notifications for employee
    print("\n[3] Checking initial notifications...")
    initial_notif = requests.get(
        f"{BASE_URL}/notifications",
        headers=employee_headers
    )
    initial_count = len(initial_notif.json()) if initial_notif.status_code == 200 else 0
    print(f"✅ Employee has {initial_count} initial notifications")
    
    # Step 4: Get pending leave requests for manager
    print("\n[4] Getting pending leave requests...")
    leave_requests = requests.get(
        f"{BASE_URL}/leave-requests?status=pending",
        headers=manager_headers
    )
    
    if leave_requests.status_code != 200:
        print(f"❌ Failed to get leave requests: {leave_requests.text}")
        return
    
    leave_list = leave_requests.json()
    if len(leave_list) == 0:
        print("⚠️  No pending leave requests found. Creating one...")
        # Create a leave request
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        create_leave = requests.post(
            f"{BASE_URL}/leave-requests",
            headers=employee_headers,
            json={
                "start_date": tomorrow,
                "end_date": tomorrow,
                "leave_type": "paid",
                "duration_type": "full_day",
                "reason": "Test leave request"
            }
        )
        if create_leave.status_code == 200:
            leave_list = [create_leave.json()]
            print(f"✅ Created new leave request: ID {leave_list[0]['id']}")
        else:
            print(f"❌ Failed to create leave request: {create_leave.text}")
            return
    
    leave_id = leave_list[0]["id"]
    print(f"✅ Found leave request ID: {leave_id}")
    
    # Step 5: Approve the leave request
    print("\n[5] Approving leave request...")
    approve_leave = requests.post(
        f"{BASE_URL}/manager/approve-leave/{leave_id}",
        headers=manager_headers,
        json={"review_notes": "Approved for testing"}
    )
    
    if approve_leave.status_code == 200:
        print(f"✅ Leave approved successfully")
    else:
        print(f"❌ Failed to approve leave: {approve_leave.text}")
        return
    
    # Step 6: Check notifications for employee after approval
    print("\n[6] Checking notifications after leave approval...")
    after_approval = requests.get(
        f"{BASE_URL}/notifications",
        headers=employee_headers
    )
    
    if after_approval.status_code == 200:
        notif_list = after_approval.json()
        print(f"✅ Employee now has {len(notif_list)} notifications")
        
        # Find the leave approval notification
        leave_notif = None
        for notif in notif_list:
            if notif.get('notification_type') == 'leave_approved':
                leave_notif = notif
                break
        
        if leave_notif:
            print(f"   ✅ FOUND Leave Approval Notification:")
            print(f"      Title: {leave_notif['title']}")
            print(f"      Message: {leave_notif['message']}")
            print(f"      Type: {leave_notif['notification_type']}")
            print(f"      Read: {leave_notif['is_read']}")
        else:
            print(f"   ❌ Leave approval notification NOT found")
            print(f"   Available notifications:")
            for n in notif_list:
                print(f"      - {n['title']} ({n['notification_type']})")
    else:
        print(f"❌ Failed to get notifications: {after_approval.text}")
    
    # Step 7: Test overtime approval
    print("\n[7] Testing overtime approval...")
    today = datetime.now().strftime("%Y-%m-%d")
    create_ot = requests.post(
        f"{BASE_URL}/overtime-requests",
        headers=employee_headers,
        json={
            "overtime_date": today,
            "hours_requested": 2,
            "reason": "Test overtime"
        }
    )
    
    if create_ot.status_code == 200:
        ot_id = create_ot.json()["id"]
        print(f"✅ Created overtime request: ID {ot_id}")
        
        # Approve it
        approve_ot = requests.put(
            f"{BASE_URL}/overtime-requests/{ot_id}/approve",
            headers=manager_headers,
            json={"approval_notes": "Approved for testing"}
        )
        
        if approve_ot.status_code == 200:
            print(f"✅ Overtime approved")
            
            # Check notification
            after_ot = requests.get(
                f"{BASE_URL}/notifications",
                headers=employee_headers
            )
            
            if after_ot.status_code == 200:
                notif_list = after_ot.json()
                ot_notif = None
                for notif in notif_list:
                    if notif.get('notification_type') == 'overtime_approved':
                        ot_notif = notif
                        break
                
                if ot_notif:
                    print(f"   ✅ FOUND Overtime Approval Notification:")
                    print(f"      Title: {ot_notif['title']}")
                    print(f"      Message: {ot_notif['message']}")
                else:
                    print(f"   ❌ Overtime approval notification NOT found")
        else:
            print(f"❌ Failed to approve overtime: {approve_ot.text}")
    else:
        print(f"❌ Failed to create overtime request: {create_ot.text}")
    
    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    test_with_api()
