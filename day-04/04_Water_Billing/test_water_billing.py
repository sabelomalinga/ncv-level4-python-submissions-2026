"""Q10: Automated checks to run in Thonny; capture the Shell output."""
from water_billing import calculate_bill, classify_consumption, validate_household

print("Q10 - WATER BILLING TEST CASES")
for usage, expected in [(0, 0), (6, 0), (7, 8.50), (20, 119), (25, 179), (50, 479)]:
    actual = calculate_bill(usage)
    print(f"Usage {usage} kL: R{actual:.2f}; expected R{expected:.2f}; PASS: {abs(actual-expected)<0.001}")
for usage, expected in [(0, "LOW"), (20, "LOW"), (21, "MODERATE"), (50, "MODERATE"), (51, "HIGH")]:
    actual = classify_consumption(usage)
    print(f"Category {usage} kL: {actual}; expected {expected}; PASS: {actual == expected}")

samples = [
    ("M001,Test Person,10,15,Soshanguve", {"M001": {}}, "Duplicate"),
    ("M002,Test Person,abc,15,Soshanguve", {}, "numeric"),
    ("M003,Test Person,-1,15,Soshanguve", {}, "non-negative"),
    ("M004,Test Person,20,15,Soshanguve", {}, "below"),
    ("M005,,10,15,Soshanguve", {}, "missing"),
]
for line, existing, expected in samples:
    record, reason = validate_household(line, existing)
    print(f"Validation {line.split(',')[0]}: {reason}; PASS: {record is None and expected.lower() in reason.lower()}")
