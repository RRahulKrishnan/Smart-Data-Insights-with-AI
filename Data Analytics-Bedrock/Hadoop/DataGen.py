import random
import datetime

def generate_sample_data(filename, num_records):
    start_date = datetime.date(2000, 1, 1)
    end_date = datetime.date(2020, 12, 31)

    with open(filename, 'w') as f:
        for i in range(num_records):
            user_id = f"user{i:05d}"
            loan_grant_date = start_date + datetime.timedelta(days=random.randint(0, (end_date - start_date).days))
            loan_repayment_date = loan_grant_date + datetime.timedelta(days=random.randint(30, 3650))
            f.write(f"{user_id},{loan_grant_date},{loan_repayment_date}\n")

generate_sample_data('loans.csv', 1000)