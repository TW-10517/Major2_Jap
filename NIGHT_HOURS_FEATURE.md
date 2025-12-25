# Night Hours Allowance Feature

## Overview
Added night hours tracking and calculation for employee attendance reports. Night hours are calculated as hours worked after 22:00 (10 PM), which is used for night shift allowance eligibility.

## Implementation Details

### Backend Changes

#### 1. Night Hours Calculation Function
**File**: `/backend/app/main.py`
**Function**: `calculate_night_hours(in_time_str, out_time_str, night_start_hour=22)`

Calculates the number of hours worked after 22:00 for any given shift.

**Logic**:
- Accepts check-in and check-out times in HH:MM format
- Handles midnight wrap-around (shifts that cross midnight)
- Returns total hours worked between 22:00 and 06:00 (next day 22:00)

**Test Results**:
```
✓ Day shift (9:00-17:00) → 0.00 hrs
✓ Night shift (20:00-04:00) → 6.00 hrs  
✓ Full night shift (22:00-06:00) → 8.00 hrs
✓ Partial night (21:00-23:00) → 1.00 hrs
✓ Shift before 22:00 (18:00-02:00) → 4.00 hrs
```

#### 2. Employee Monthly Report Export
**Endpoint**: `GET /attendance/export/employee-monthly`

**Added Features**:
- Night hours calculated for each day
- Night hours column in daily attendance sheet
- Total night hours summary in summary sheet

**Excel Output Structure**:

**Sheet 1: Summary**
- Employee details (name, ID)
- Attendance statistics
- Leave summary
- Comp-off summary
- **Hours Summary** (includes):
  - Total Hours Worked
  - Total Overtime Hours
  - **Total Night Hours (After 22:00)** ← NEW

**Sheet 2: Daily Attendance**
- Date
- Day of week
- Assigned Shift
- Check-In time
- Check-Out time
- Hours Worked
- **Night Hours (After 22:00)** ← NEW COLUMN
- Break time
- Overtime Hours
- Status
- Comp-Off Earned/Used
- Notes

### Frontend Changes

**File**: `/frontend/src/pages/Manager.jsx`

**UI Enhancement**:
- Updated "Download Individual Employee Monthly Report" section description
- Added note: "Includes: Daily attendance details with night hours (after 22:00), overtime, leave info, and summary statistics"

### How to Use

1. **Download Individual Employee Report**:
   - Manager login → Attendance tab
   - Enter Employee ID
   - Select Month and Year
   - Click "Download"
   - Excel file contains night hours calculation

2. **View Night Hours**:
   - Open the downloaded Excel file
   - Go to "Daily Attendance" sheet
   - Look for "Night Hours (After 22:00)" column
   - Go to "Summary" sheet
   - Check "Total Night Hours (After 22:00)" in the Hours Summary section

### Examples

**Example 1: Employee with night shift**
- Check-in: 20:00
- Check-out: 04:00 (next day)
- Night Hours: 6.00 hrs (22:00-04:00 = 6 hours)

**Example 2: Employee with day shift**
- Check-in: 09:00
- Check-out: 17:00
- Night Hours: 0.00 hrs (no work after 22:00)

**Example 3: Employee with mixed shift**
- Check-in: 18:00
- Check-out: 02:00 (next day)
- Night Hours: 4.00 hrs (22:00-02:00 = 4 hours)

## Database Tables Used
- `Attendance`: Stores check-in/check-out times
- `Schedule`: Stores shift information
- `Employee`: Employee master data
- `LeaveRequest`: Leave records
- `CompOffDetail`: Comp-off tracking

## Technical Specifications

**Night Allowance Threshold**: 22:00 (10 PM)
**Calculation Window**: 22:00 - 06:00 (next day 22:00)

**Notes**:
- Only actual worked hours count (presence in check-in/check-out records)
- Hours are calculated to 2 decimal places
- Works with shifts crossing midnight
- Integrates with existing overtime and comp-off tracking

## Testing

All calculation scenarios tested and verified:
- ✓ Day shifts (no night hours)
- ✓ Full night shifts (all hours after 22:00)
- ✓ Mixed shifts (crossing 22:00)
- ✓ Midnight wrap-around shifts
- ✓ Partial shifts in night period

## Files Modified

1. `/backend/app/main.py`:
   - Added `calculate_night_hours()` function
   - Updated `export_employee_monthly_attendance()` endpoint
   - Added night hours to Excel sheets
   - Updated column headers and styling

2. `/frontend/src/pages/Manager.jsx`:
   - Enhanced employee report download description

## Related Features
- Attendance tracking
- Overtime calculation
- Leave management
- Comp-off tracking
- Monthly attendance reports
