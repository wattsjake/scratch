TODO
====

- [TODO] contact Sartorius to figure out how to hid the menu
- [X] Try to communicate with the scale and have it return its Name and ID
- [TODO] Figure out how to lock out the menu after setting up the scale. 
- [TODO] Add miscellaneous information to README.md
- [TODO] Migrate sartorius_scale to its own repository
- [TODO] Create standardized format for scale readings using scale subclasses to change proprietary
    formats to the standardized one
- [X] The Sartorius Entris uses a proprietary serial pin format, so we need to either:
    (1) Customize the pin figuration somehow using PySerial (Preferred)
    (X) Buy or make a proprietary connector so communication can be established
- [TODO] Organize scale commands by having important ones as constants and putting the rest in a dict