# DBL
DBL Embedded Systems TU/e 2023 Max Ultra Turbo Deluxe Nebula Edition

Team members:
- Samuel Boor
- Alec Boyadjiev Boyd
- Eryk Kiepuszewski
- Alex Metaxa
- Hargun Kour Raina
- Matúš Sevcik

In this DBL we were intrsucted to create a robot that would sort white and black disks on a moving conveyor belt and detect a set amount of errors in its system. It would only have to sort a fraction of the disks in order to leave some on the belt for the other teams present.

Thus, our team has created this specification for our robot:
- Sorts black and white disks into different bins by:
    - detecting disk presence using light intensity measurement from an RGB sensor
    - detecting disk colour using RGB sensor
    - using a windmill mechanism to push disks onto a ramp
    - using a stick mechanism to push disk into correct bin
- Only sorts every fourth disk detected
- Has an LCD screen that will display:
    - a counter showing the number of disks sorted
    - the color of each detected disk

Credits:
- https://github.com/adafruit/Adafruit_CircuitPython_TCS34725 - colour sensor
- https://stackoverflow.com/questions/9694165/convert-rgb-color-to-english-color-name-like-green-with-python - LCD screen
