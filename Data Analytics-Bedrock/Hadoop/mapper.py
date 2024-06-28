import sys
from datetime import datetime

def mapper():
    print("Mapper started", file=sys.stderr)
    for line in sys.stdin:
        line = line.strip()
        print(f"Processing line: {line}", file=sys.stderr)
        parts = line.split(',')
        if len(parts) != 3:
            print(f"Skipping line due to incorrect format: {line}", file=sys.stderr)
            continue  # Skip this line if it does not have exactly 3 parts
        user_id, loan_grant_date, loan_repayment_date = parts
        try:
            loan_grant_date = datetime.strptime(loan_grant_date, '%Y-%m-%d')
            loan_repayment_date = datetime.strptime(loan_repayment_date, '%Y-%m-%d')
            loan_duration = (loan_repayment_date - loan_grant_date).days
            print(f"{user_id}\t{loan_duration}")
        except ValueError as e:
            print(f"Error parsing dates: {e}", file=sys.stderr)
            continue  # Skip this line if date parsing fails

if __name__ == "__main__":
    mapper()
 