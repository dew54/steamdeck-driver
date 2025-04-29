from steamdeck import SteamDeck

deck = SteamDeck()

try:
    while True:
        deck.poll()
        for event in deck.get_events():
            if event[0] == "axis":
                print(f"Axis {event[1]} moved to {event[2]}")
            elif event[0] == "button_down":
                print(f"Button {event[1]} pressed")
            elif event[0] == "button_up":
                print(f"Button {event[1]} released")

        # Example: Read specific stick positions
        left_stick_x = deck.get_axis(0)
        left_stick_y = deck.get_axis(1)
        # Do something with the values...

finally:
    deck.close()
