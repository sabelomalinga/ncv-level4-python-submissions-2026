# Maxwell Fitness Centre

# Function 1: Calculate the amount due before VAT
def amount_due(facility_code, hours):

    rates = {
        "squa": 13.00,
        "swim": 12.00,
        "gym": 11.00,
        "wei": 8.00
    }

    amount = rates[facility_code] * hours

    return amount


# Function 2: Calculate the final amount including 14% VAT
def final_amount_due(amount):

    vat = amount * 0.14
    final_amount = amount + vat

    return final_amount


# Function 3: Display the customer's name and final amount
def display(name, final_amount):

    print("\n----- PAYMENT DETAILS -----")
    print("Customer name:", name)
    print(f"Final amount payable: R{final_amount:.2f}")


# Function 4: Process the payment
def process_payment():

    # Get customer details
    name = input("Enter customer's name: ")
    facility_code = input("Enter facility code (squa, swim, gym, wei): ")
    hours = float(input("Enter number of hours used: "))

    # Calculate amount before VAT
    amount = amount_due(facility_code, hours)

    # Calculate final amount including VAT
    final_amount = final_amount_due(amount)

    # Display payment details
    display(name, final_amount)


# Start the program
process_payment()