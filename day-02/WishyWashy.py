import random

# Generate random usage minutes
def generate_minutes():

    minutes = random.randint(30, 180)

    return minutes


# Calculate amount before VAT
def calc_amount(machine_type, minutes):

    if machine_type == "A":
        initial_cost = 50.00
        hourly_rate = 30.00

    elif machine_type == "B":
        initial_cost = 62.50
        hourly_rate = 36.25

    elif machine_type == "C":
        initial_cost = 74.87
        hourly_rate = 40.50

    # Convert minutes into hours
    hours = minutes / 60

    # Calculate amount before VAT
    amount = initial_cost + (hourly_rate * hours)

    return amount


# 3. Calculate VAT and total amount
def calc_total_amount(amount):

    vat = amount * 0.14
    total = amount + vat

    return vat, total


# 4. Display daily summary
def display_summary(payments):

    count = 0
    total_payments = 0
    highest = payments[0]
    lowest = payments[0]

    for payment in payments:

        count += 1
        total_payments += payment

        if payment > highest:
            highest = payment

        if payment < lowest:
            lowest = payment

    average = total_payments / count

    print("\n========== DAILY SUMMARY ==========")
    print("Number of customers:", count)
    print(f"Combined amount payable: R{total_payments:.2f}")
    print(f"Average payment per customer: R{average:.2f}")
    print(f"Highest payment: R{highest:.2f}")
    print(f"Lowest payment: R{lowest:.2f}")


# 5. Process customer payments
def process_payments():

    customers = int(input("Enter number of customers to process: "))

    payments = []

    for i in range(customers):

        print("\n========== CUSTOMER", i + 1, "==========")

        # Get customer details
        name = input("Enter customer's name: ")
        machine_type = input("Enter machine type (A, B or C): ").upper()

        # Generate random usage minutes
        minutes = generate_minutes()

        # Calculate amount before VAT
        amount = calc_amount(machine_type, minutes)

        # Calculate VAT and total payable
        vat, total = calc_total_amount(amount)

        # Store total payable in payments list
        payments.append(total)

        # Display customer invoice
        print("\n========== CUSTOMER INVOICE ==========")
        print("Customer name:", name)
        print("Machine type:", machine_type)
        print("Generated minutes:", minutes)
        print(f"Amount before VAT: R{amount:.2f}")
        print(f"VAT (14%): R{vat:.2f}")
        print(f"Total payable: R{total:.2f}")

    # Display daily summary
    display_summary(payments)


# Start the program
process_payments()