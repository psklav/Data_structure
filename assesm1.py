import random

# Initialize empty lists for queues
landing_queue = []
emergency_queue = []
takeoff_queue = []

# Flighr counter
flight_id = 1

# Simulate a number of incoming requests
for request in range(15):
    

    # Randomly decide what kind of request comes in
    action = random.choice(["landing", "takeoff", "emergency"])

    # Create a name for the flight
    flight_name = "Flight-" + str(flight_id)
    flight_id += 1

    # Add the flight to the correct queue
    if action == "landing":
        landing_queue.append(flight_name)
        #print(f"{flight_name} wants to land.")
    elif action == "takeoff":
        takeoff_queue.append(flight_name)
        #print(f"{flight_name} wants to take off.")
    else:
        emergency_queue.append(flight_name)
        #print(f"{flight_name} has an EMERGENCY and needs to land!")

    # Process one flight per step
    if len(emergency_queue) > 0:
        flight = emergency_queue.pop(0)
        print(f"{flight} is making an EMERGENCY landing.")
    elif len(landing_queue) > 0:
        flight = landing_queue.pop(0)
        print(f"{flight} is landing.")
    elif len(takeoff_queue) > 0:
        flight = takeoff_queue.pop(0)
        print(f"{flight} is taking off.")
    else:
        print("No queue.")
