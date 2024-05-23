import sys
import numpy as np
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QSpinBox,
    QGraphicsView,
    QGraphicsScene,
    QGraphicsEllipseItem,
    QGraphicsRectItem,
    QGraphicsTextItem,
    QGridLayout,
)
from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QTimer
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class AdvancedTankFillingGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced Tank Filling and Heating Sensor Tutorial")
        self.setGeometry(100, 100, 1200, 800)

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        self.layout = QGridLayout(self.main_widget)

        self.setup_circuit_view()
        self.setup_controls()

        self.prompt_label = QLabel(
            "Tasks:\n"
            "1. Adjust the flow rate, heater, and fan to maintain the water level at 50% and temperature at 40°C.\n"
            "2. Measure the water level using ultrasonic, capacitive, and pressure sensors.\n"
            "3. Compare the readings from different sensors and analyze the temperature effect.\n"
            "4. Ensure the water is supplied at a consistent warm temperature for heating purposes."
        )
        self.layout.addWidget(self.prompt_label, 0, 0, 1, 2)

        self.results_label = QLabel("Simulation Results will appear here.")
        self.results_label.setFixedHeight(60)
        self.layout.addWidget(self.results_label, 1, 0, 1, 2)

        self.plot_layout = QHBoxLayout()
        self.layout.addLayout(self.plot_layout, 2, 0, 1, 2)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_simulation)

        # Set up Matplotlib figure for plotting results
        self.figure, self.ax = plt.subplots(1, 2, figsize=(10, 4))
        self.canvas = FigureCanvas(self.figure)
        self.plot_layout.addWidget(self.canvas)

        self.water_levels = []
        self.flow_rates = []
        self.temperatures = []

    def setup_circuit_view(self):
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setFixedHeight(400)
        self.layout.addWidget(self.view, 3, 0, 1, 2)

        self.draw_circuit()

    def draw_circuit(self):
        pen = QPen(Qt.black)
        brush = QBrush(Qt.blue)

        # Draw tank
        self.tank = QGraphicsRectItem(500, 50, 100, 300)
        self.tank.setBrush(QBrush(Qt.white))
        self.scene.addItem(self.tank)
        self.add_annotation(self.tank, "Tank", 530, 30)

        # Draw water level indicator
        self.water_level = QGraphicsRectItem(500, 350, 100, 0)
        self.water_level.setBrush(QBrush(Qt.blue))
        self.scene.addItem(self.water_level)
        self.water_level_text = QGraphicsTextItem("Water Level: 0%", self.tank)
        self.water_level_text.setPos(510, 370)

        # Draw pumps and valves
        self.pumps = []
        for i, pos in enumerate([(50, 200), (50, 300)]):
            pump = QGraphicsEllipseItem(pos[0], pos[1], 50, 50)
            pump.setBrush(brush)
            self.scene.addItem(pump)
            self.add_annotation(pump, f"Pump {i+1}", pos[0] + 5, pos[1] - 20)
            self.pumps.append(pump)

        self.valves = []
        for i, pos in enumerate([(150, 225), (150, 325)]):
            valve = QGraphicsRectItem(pos[0], pos[1], 30, 30)
            valve.setBrush(brush)
            self.scene.addItem(valve)
            self.add_annotation(valve, f"Valve {i+1}", pos[0] + 5, pos[1] - 20)
            self.valves.append(valve)

        # Draw sensors
        self.sensors = []
        sensor_positions = [
            (250, 210),  # Flow sensor
            (520, 30),  # Ultrasonic sensor
            (570, 30),  # Capacitive sensor
            (620, 30),  # Pressure sensor
            (600, 350),  # Temperature sensor
        ]
        sensor_colors = [
            QColor(0, 0, 255),  # Blue for Flow sensor
            QColor(255, 0, 0),  # Red for Ultrasonic sensor
            QColor(0, 255, 0),  # Green for Capacitive sensor
            QColor(0, 0, 255),  # Blue for Pressure sensor
            QColor(255, 255, 0),  # Yellow for Temperature sensor
        ]
        sensor_labels = [
            "Flow Sensor",
            "Ultrasonic Sensor",
            "Capacitive Sensor",
            "Pressure Sensor",
            "Temp Sensor",
        ]
        for i, pos in enumerate(sensor_positions):
            sensor = (
                QGraphicsEllipseItem(pos[0], pos[1], 30, 30)
                if i != 4
                else QGraphicsRectItem(pos[0], pos[1], 30, 30)
            )
            sensor.setBrush(QBrush(sensor_colors[i]))
            self.scene.addItem(sensor)
            self.add_annotation(sensor, sensor_labels[i], pos[0] - 20, pos[1] - 20)
            self.sensors.append(sensor)

        # Draw heater
        self.heater = QGraphicsRectItem(650, 350, 50, 50)
        self.heater.setBrush(QBrush(QColor(255, 165, 0)))  # Orange color
        self.scene.addItem(self.heater)
        self.add_annotation(self.heater, "Heater", 650, 320)

        # Draw fan
        self.fan = QGraphicsEllipseItem(700, 50, 50, 50)
        self.fan.setBrush(QBrush(QColor(135, 206, 235)))  # Light blue color for fan
        self.scene.addItem(self.fan)
        self.add_annotation(self.fan, "Fan", 715, 20)

        # Draw connecting lines
        self.scene.addLine(75, 225, 165, 225, pen)
        self.scene.addLine(165, 225, 165, 300, pen)
        self.scene.addLine(75, 325, 165, 325, pen)
        self.scene.addLine(180, 225, 500, 225, pen)
        self.scene.addLine(180, 325, 500, 325, pen)

    def add_annotation(self, item, text, x, y):
        annotation = QGraphicsTextItem(text)
        annotation.setPos(x, y)
        self.scene.addItem(annotation)

    def setup_controls(self):
        control_layout = QHBoxLayout()

        # Flow Rate Spinner
        self.flow_label = QLabel("Set Flow Rate (L/min):")
        self.flow_spinner = QSpinBox()
        self.flow_spinner.setRange(0, 100)
        self.flow_spinner.setValue(10)

        # Heater Power Spinner
        self.heater_label = QLabel("Set Heater Power (kW):")
        self.heater_spinner = QSpinBox()
        self.heater_spinner.setRange(0, 10)
        self.heater_spinner.setValue(2)

        # Fan Power Spinner
        self.fan_label = QLabel("Set Fan Power (kW):")
        self.fan_spinner = QSpinBox()
        self.fan_spinner.setRange(0, 10)
        self.fan_spinner.setValue(2)

        # Control buttons
        self.start_button = QPushButton("Start Simulation")
        self.start_button.clicked.connect(self.start_task)
        self.adjust_button = QPushButton("Adjust Parameters")
        self.adjust_button.clicked.connect(self.adjust_parameters)
        self.finish_button = QPushButton("Finish Simulation")
        self.finish_button.clicked.connect(self.finish_task)

        # Adding Controls to Layout
        control_layout.addWidget(self.flow_label)
        control_layout.addWidget(self.flow_spinner)
        control_layout.addWidget(self.heater_label)
        control_layout.addWidget(self.heater_spinner)
        control_layout.addWidget(self.fan_label)
        control_layout.addWidget(self.fan_spinner)
        control_layout.addWidget(self.start_button)
        control_layout.addWidget(self.adjust_button)
        control_layout.addWidget(self.finish_button)

        self.layout.addLayout(control_layout, 4, 0, 1, 2)

    def start_task(self):
        self.flow_rate = self.flow_spinner.value()  # initial flow rate in L/min
        self.heater_power = self.heater_spinner.value()  # initial heater power in kW
        self.fan_power = self.fan_spinner.value()  # initial fan power in kW
        self.water_temperature = 10  # initial water temperature in °C
        self.tank_height = (
            1  # initial water level in the tank (1-300 corresponds to 0-100% height)
        )
        self.timer.start(1000)  # update every second

        self.water_levels = []
        self.flow_rates = []
        self.temperatures = [
            self.water_temperature
        ]  # Initialize with initial temperature

    def adjust_parameters(self):
        self.flow_rate = self.flow_spinner.value()
        self.heater_power = self.heater_spinner.value()
        self.fan_power = self.fan_spinner.value()
        self.update_simulation()  # Ensure immediate effect of heater and fan power change

    def finish_task(self):
        self.timer.stop()
        self.results_label.setText("Simulation finished.")

    def update_simulation(self):
        # Simulating the tank filling based on the flow rate
        max_tank_height = 300  # max height of the tank in pixels
        tank_volume = 1000  # volume of the tank in liters
        flow_rate_m3 = self.flow_rate / 1000 / 60  # convert L/min to m³/s

        # Simulating non-linear relationship for flow rate
        self.flow_rate += 0.5 * np.sin(
            len(self.flow_rates) * 0.1
        )  # introduce some non-linearity

        # Simulating heat transfer
        specific_heat_water = 4.18  # kJ/kg°C
        density_water = 997  # kg/m^3

        # Heat added by the heater (simplified model)
        heat_added = self.heater_power * 1000  # converting kW to J/s

        # Heat removed by the fan (simplified model)
        heat_removed = self.fan_power * 1000  # converting kW to J/s

        # Calculate mass of water in the tank
        if self.tank_height > 0:
            water_mass = (
                self.tank_height * tank_volume * density_water / max_tank_height
            )
        else:
            water_mass = 0.001  # Prevent division by zero

        # Temperature change (simplified)
        delta_temp = (heat_added - heat_removed) / (
            water_mass * specific_heat_water
        )  # calculating temperature change

        # Update water temperature
        self.water_temperature += delta_temp
        if self.water_temperature > 100:
            self.water_temperature = 100  # limit to boiling point for simplicity
        if self.water_temperature < 0:
            self.water_temperature = 0  # limit to freezing point for simplicity

        # Update tank height considering water expansion
        volume_expansion = (
            self.water_temperature * 0.000214
        )  # volumetric thermal expansion coefficient
        self.tank_height += (flow_rate_m3 * 1000) * (
            1 + volume_expansion
        )  # adjust for expansion

        if self.tank_height > max_tank_height:
            self.tank_height = max_tank_height
            self.timer.stop()

        water_level_percent = (self.tank_height / max_tank_height) * 100

        # Update water level indicator
        self.water_level.setRect(500, 350 - self.tank_height, 100, self.tank_height)
        self.water_level_text.setPlainText(f"Water Level: {water_level_percent:.1f}%")

        # Sensor readings (simulated)
        flow_sensor_reading = self.flow_rate  # in L/min
        ultrasonic_sensor_reading = (
            max_tank_height - self.tank_height
        ) / 3  # scaled to cm
        capacitive_sensor_reading = water_level_percent  # directly as a percentage
        pressure_sensor_reading = (
            self.tank_height / max_tank_height * 10
        )  # in kPa, assuming linear relationship with height
        temperature_sensor_reading = self.water_temperature  # in °C

        self.water_levels.append(water_level_percent)
        self.flow_rates.append(flow_sensor_reading)
        self.temperatures.append(temperature_sensor_reading)

        result_text = (
            f"Simulation Results:\n"
            f"Flow Rate: {flow_sensor_reading:.2f} L/min, "
            f"Water Level: {water_level_percent:.1f}%, "
            f"Ultrasonic: {ultrasonic_sensor_reading:.1f} cm, "
            f"Capacitive: {capacitive_sensor_reading:.1f}%, "
            f"Pressure: {pressure_sensor_reading:.1f} kPa, "
            f"Temperature: {temperature_sensor_reading:.1f} °C\n"
        )

        self.results_label.setText(result_text)

        self.plot_results()

    def plot_results(self):
        self.ax[0].clear()
        self.ax[0].plot(self.flow_rates, label="Flow Rate (L/min)")
        self.ax[0].plot(self.water_levels, label="Water Level (%)")
        self.ax[0].legend()
        self.ax[0].set_xlabel("Time (s)")
        self.ax[0].set_ylabel("Value")
        self.ax[0].set_title("Flow Rate and Water Level over Time")

        self.ax[1].clear()
        self.ax[1].plot(self.temperatures, label="Temperature (°C)", color="r")
        self.ax[1].legend()
        self.ax[1].set_xlabel("Time (s)")
        self.ax[1].set_ylabel("Temperature (°C)")
        self.ax[1].set_title("Water Temperature over Time")
        self.ax[1].set_ylim(
            [min(self.temperatures) - 5, max(self.temperatures) + 5]
        )  # Adjust y-axis to ensure better visualization

        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = AdvancedTankFillingGame()
    game.show()
    sys.exit(app.exec_())
