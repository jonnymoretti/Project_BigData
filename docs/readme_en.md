# Traffic Simulation at an Intersection

This project involves simulating traffic at an intersection of streets, where cars move in random directions. The goal is to model a realistic traffic coordination system, including traffic lights, heavy traffic conditions, and malfunctioning cars.

### Key Features

- **Random Cars:** Each car is represented by a thread and moves in random directions, starting and finishing its route at the intersection.
- **Traffic Light:** The system includes a traffic light that coordinates the movement of cars, taking into account traffic conditions and malfunctions.
- **Traffic Conditions:** Heavy traffic is simulated, and cars face additional waiting time if they are malfunctioning.
- **Detailed Reports:** The code generates detailed reports on the state of cars, their movements at the intersection, and special conditions such as heavy traffic and malfunctions.

### How to Run

To test the simulation, simply execute the main script `main()` in the file. The code creates threads for cars and one thread to update the traffic light, providing a dynamic and interactive simulation.

```
python Group6_BigData.py
```
It is also possible to run the file on Google Colab: 
<a target="_blank" href="https://colab.research.google.com/drive/12tn7Qrr3XnC6aeO6cGkT2JIpTCXd3BFn?usp=sharing">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

### Customization

- **Initial Car Directions:** The code allows for the customization of the initial directions of cars to simulate different traffic scenarios.
- **Probability of Malfunctioning Cars:** The variable `self.esta_avariado` is randomly set for each car based on a probability, providing flexibility in simulating malfunctions.

### Results

At the end of the execution, a report on the intersection's status is displayed, providing information about each car, their directions, and wait times.
