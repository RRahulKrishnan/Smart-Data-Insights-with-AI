import sys

def reducer():
    print("Reducer started", file=sys.stderr)
    min_duration = float('inf')
    max_duration = float('-inf')
    max_duration_count = 0

    for line in sys.stdin:
        line = line.strip()
        print(f"Processing line: {line}", file=sys.stderr)
        if not line:
            continue  # Skip empty lines
        try:
            user_id, loan_duration = line.split('\t')
            loan_duration = int(loan_duration)

            if loan_duration < min_duration:
                min_duration = loan_duration

            if loan_duration > max_duration:
                max_duration = loan_duration
                max_duration_count = 1
            elif loan_duration == max_duration:
                max_duration_count += 1
        except ValueError as e:
            print(f"Error processing line: {line}, {e}", file=sys.stderr)
            continue  # Skip lines with unexpected format

    print(f"Minimum Loan Duration: {min_duration} days")
    print(f"Maximum Loan Duration: {max_duration} days")
    print(f"Frequency of Maximum Loan Duration: {max_duration_count}")

if __name__ == "__main__":
    reducer()
