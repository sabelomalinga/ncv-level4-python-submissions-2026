qualifiers = 0
total = 0

winner_name = ""
lowest_time = 0
winner_time = ""

while True:

    name = input("Enter athlete's name (x to end): ")

    if name.lower() == "x":
        break

    time = input("Enter time (mm:ss): ")

    # Check if time is valid
    parts = time.split(":")

    if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():

        minutes = int(parts[0])
        seconds = int(parts[1])

        if seconds < 60:

            # Convert time into total seconds
            total_seconds = minutes * 60 + seconds

            total += 1

            # Count qualifiers (25:00 or less)
            if total_seconds <= 1500:
                qualifiers += 1

            # Find the winner
            if winner_name == "" or total_seconds < lowest_time:
                lowest_time = total_seconds
                winner_name = name
                winner_time = time

        else:
            print("Invalid time! Please enter a valid mm:ss time.")

    else:
        print("Invalid time! Please enter a valid mm:ss time.")


# Display results
print("\n----- RACE RESULTS -----")

if total == 0:
    print("No valid athletes were entered.")
else:
    print("Winner:", winner_name, "(", winner_time + ")")
    print("Qualified:", qualifiers, "of", total)