Ramon’s arm and head thingy

•	Helmet will be motorized with servos and LEDs
o	Either take speech, or a button
	Commands a Boolean to be true or false
•	True: Helmet opens, LEDs turn off
•	False: Helmet closes, LEDs turn on

•	Chest LED lights
o	Perhaps use transistor circuit for 12V lights
o	Need 5V-12V stepper

•	Arm will have a shocker (boost converter) which takes 5V but relies on a relay
o	Either take speech, or a button
	Will run for 2 seconds

•	For speech detect:
o	Parse strings
o	“Helmet” will command helmet to open, close
o	“Shock” will command boost converter to turn on
o	“Wake” will command awareness
	Then looks for either “Helmet” or “Shock” for 5 seconds, then closes
	Might use button

Design requirements:
•	Waterproof or water resistant 
•	Removable components
o	Helmet circuit
o	Arm 
o	Brain (pi)
•	Pi can connect to phone


Distribution of files:
•	Github

Deadline: Oct 29

Questions:
•	Does Pi Zero W have a V_in?
•	Can we connect to Pi Zero reliably with mobile?
•	
