import csv
import json
import subprocess

def create_budget(budget_name, linked_accounts, planned_budget, email_address):
    budget = {
        "BudgetName": budget_name,
        "BudgetType": "COST",
        "CostTypes": {
            "IncludeCredit": True,
            "IncludeDiscount": True,
            "IncludeOtherSubscription": True,
            "IncludeRecurring": True,
            "IncludeRefund": True,
            "IncludeSubscription": True,
            "IncludeSupport": True,
            "IncludeTax": True,
            "IncludeUpfront": True,
            "UseBlended": False
        },
        "TimeUnit": "MONTHLY",
        "PlannedBudgetLimits": planned_budget,
        "CostFilters": {
            "LinkedAccount": linked_accounts
        }
    }

    notifications_with_subscribers = [
        {
            "Notification": {
                "NotificationType": "ACTUAL",
                "ComparisonOperator": "GREATER_THAN",
                "Threshold": 105,
                "ThresholdType": "PERCENTAGE"
            },
            "Subscribers": [
                {
                    "Address": email_address,
                    "SubscriptionType": "EMAIL"
                }
            ]
        },
        {
            "Notification": {
                "NotificationType": "FORECASTED",
                "ComparisonOperator": "GREATER_THAN",
                "Threshold": 100,
                "ThresholdType": "PERCENTAGE"
            },
            "Subscribers": [
                {
                    "Address": email_address,
                    "SubscriptionType": "EMAIL"
                }
            ]
        }
    ]

    with open('budget.json', 'w') as f:
        json.dump(budget, f)

    with open('notifications-with-subscribers.json', 'w') as f:
        json.dump(notifications_with_subscribers, f)

    subprocess.run([
        'aws', 'budgets', 'create-budget',
        '--account-id', '358038564507',
        '--budget', 'file://budget.json',
        '--notifications-with-subscribers', 'file://notifications-with-subscribers.json'
    ])

def read_csv_and_create_budgets(csv_file, email_address):
    with open(csv_file, mode='r', encoding='utf-8-sig') as file:
        csv_reader = csv.DictReader(file)
        headers = csv_reader.fieldnames
        print(f"CSV Headers: {headers}")
        for row in csv_reader:
            budget_name = row["Budget_Name"]
            accounts = row["Accounts"].replace(" ", "").split(',')
            planned_budget = {timestamp: {"Amount": row[timestamp], "Unit": "USD"} for timestamp in row if timestamp not in ["Budget_Name", "Accounts"] and row[timestamp]}
            try:
                create_budget(budget_name, accounts, planned_budget, email_address)
            except subprocess.CalledProcessError as e:
                if "DuplicateRecordException" in str(e):
                    print(f"Budget {budget_name} already exists.")
                else:
                    raise e

if __name__ == "__main__":
    email_address = 'finops@collibra.com'  # Replace with desired email address
    csv_file = 'budgets.csv'  # Replace with the path to your CSV file
    read_csv_and_create_budgets(csv_file, email_address)
