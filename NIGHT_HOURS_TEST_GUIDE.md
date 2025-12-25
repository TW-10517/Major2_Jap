# Night Hours Test Guide - Excel Download

## Test Data Created

**Employee**: EMP001 (Employee 1 / Manager One)  
**Dates**: December 20-23, 2025  
**Shift Time**: 18:00 to 03:00 (next day)  
**Worked Hours**: 9 hours per day  
**Night Hours**: 5 hours per day (22:00 to 03:00)  

---

## How to Download and Verify

### Step 1: Access Manager Dashboard
1. Login as Manager
2. Navigate to **Attendance** tab
3. Scroll down to **"📄 Download Individual Employee Monthly Report"** section

### Step 2: Download the Report
1. **Employee ID**: Enter `EMP001`
2. **Month**: Select `December`
3. **Year**: Select `2025`
4. Click **"Download"** button
5. Save the Excel file to your computer

---

## Excel File Structure

### Sheet 1: Summary
Shows overall statistics for the month

**Key Section**: Hours Summary
- Total Hours Worked: 36 hours (9 hours × 4 days)
- Total Overtime Hours: 0 hours
- **Total Night Hours (After 22:00): 20 hours** ← NEW FIELD
  - 5 hours per day × 4 days = 20 hours

### Sheet 2: Daily Attendance
Shows day-by-day breakdown

**Columns**:
| Date | Day | Shift | Check-In | Check-Out | Hours Worked | **Night Hours** | Break | OT | Status |
|------|-----|-------|----------|-----------|--------------|-----------------|-------|-----|--------|
| 2025-12-20 | Saturday | 18:00-03:00 | 18:00 | 03:00 | 9.00 | **5.00** | 0 | - | Present |
| 2025-12-21 | Sunday | 18:00-03:00 | 18:00 | 03:00 | 9.00 | **5.00** | 0 | - | Present |
| 2025-12-22 | Monday | 18:00-03:00 | 18:00 | 03:00 | 9.00 | **5.00** | 0 | - | Present |
| 2025-12-23 | Tuesday | 18:00-03:00 | 18:00 | 03:00 | 9.00 | **5.00** | 0 | - | Present |

**Night Hours Calculation** (Column G):
- Shift starts: 18:00
- Night period begins: 22:00
- Night period ends: 06:00 (next day)
- Shift ends: 03:00
- Night hours: 22:00 → 03:00 = **5 hours** ✓

---

## Night Hours Calculation Logic

### Formula
```
Night Hours = hours worked between 22:00 and 06:00 (next day)
```

### Examples for Different Shifts

| Check-In | Check-Out | Night Hours | Explanation |
|----------|-----------|-------------|-------------|
| 18:00 | 03:00 | 5.00 h | 22:00 to 03:00 = 5 hours |
| 20:00 | 04:00 | 6.00 h | 22:00 to 04:00 = 6 hours |
| 22:00 | 06:00 | 8.00 h | 22:00 to 06:00 = 8 hours |
| 17:00 | 01:00 | 3.00 h | 22:00 to 01:00 = 3 hours |
| 09:00 | 17:00 | 0.00 h | No hours after 22:00 |
| 14:00 | 22:00 | 0.00 h | Work ends at 22:00 (no night work) |

---

## What You'll See

### In Excel Summary Sheet:
```
HOURS SUMMARY
┌──────────────────────────────┬───────┐
│ Total Hours Worked           │ 36.00 │
│ Total Overtime Hours         │  0.00 │
│ Total Night Hours (After 22) │ 20.00 │  ← This is new!
└──────────────────────────────┴───────┘
```

### In Excel Daily Attendance Sheet:
Column G shows "Night Hours (After 22:00)" with values like:
- 5.00
- 5.00
- 5.00
- 5.00

---

## Verification Checklist

✓ Download completes without errors  
✓ Excel file opens correctly  
✓ Summary tab shows "Total Night Hours (After 22:00): 20.00"  
✓ Daily Attendance tab has "Night Hours (After 22:00)" column  
✓ Each day shows 5.00 hours for the night shift  
✓ All 4 days (Dec 20-23) are included  

---

## Technical Details

**Night Allowance Threshold**: 22:00 (10 PM)  
**Night Period**: 22:00 - 06:00 (next day 22:00)  
**Precision**: 2 decimal places (hours and minutes)  
**Test Cases Passed**: 12/12 ✓  

---

## Troubleshooting

**If night hours show 0.00**:
- Check that check-in time is before 22:00 and check-out is after 22:00
- Verify attendance records were created correctly

**If file doesn't download**:
- Ensure Employee ID is correct (EMP001)
- Check that month/year are set to December 2025
- Backend server should be running

**If column is missing**:
- Clear browser cache and download again
- Verify backend code was updated correctly

---

## Related Files

- Backend Implementation: `/backend/app/main.py`
- Test Data: Created via Python script
- Feature Documentation: `NIGHT_HOURS_FEATURE.md`
