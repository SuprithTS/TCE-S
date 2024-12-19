import pygame
import matplotlib.pyplot as plt
import os
from threading import Thread, Event
import random

class TrafficSimulation:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Traffic Congestion Management")
        self.clock = pygame.time.Clock()

        self.colors = {
            "intersection": {"WHITE": (255, 255, 255)},
        }

        self.vehicle_parameters = {
            "vehicle_count": {"lane_1": 0, "lane_2": 0, "lane_3": 0, "lane_4": 0},
            "processed_vehicles": {"lane_1": 0, "lane_2": 0, "lane_3": 0, "lane_4": 0},
        }

        # RL parameters
        self.q_table = {lane: [0] * 10 for lane in self.vehicle_parameters["vehicle_count"]}
        self.learning_rate = 0.1
        self.discount_factor = 0.9

    def calculate_avg_congestion(self, dti, total_vehicles):
        avg_congestion = {}
        for lane, count in total_vehicles.items():
            avg_congestion[lane] = dti.get(lane, 0) / (count + 1e-5)
        return avg_congestion

    def calculate_dti(self):
        dti = {}
        for lane, count in self.vehicle_parameters["vehicle_count"].items():
            dti[lane] = random.randint(0, 10)  # Simulate congestion values
        return dti

    def calculate_accuracy(self, old_dti, new_dti):
        old_congestion = self.calculate_avg_congestion(old_dti, self.vehicle_parameters["vehicle_count"])
        new_congestion = self.calculate_avg_congestion(new_dti, self.vehicle_parameters["vehicle_count"])

        total_old_congestion = sum(old_congestion.values())
        total_new_congestion = sum(new_congestion.values())

        if total_old_congestion == 0:
            return 100.0

        improvement = (total_old_congestion - total_new_congestion) / total_old_congestion * 100
        return max(0, improvement)

    def update_q_table(self, dti):
        for lane in self.vehicle_parameters["vehicle_count"]:
            state = dti[lane]
            reward = -state  # Reward is higher for lower congestion
            action = state % 10  # Placeholder for RL action selection logic

            # Q-learning update rule
            self.q_table[lane][action] += self.learning_rate * (
                reward + self.discount_factor * max(self.q_table[lane]) - self.q_table[lane][action]
            )

    def plot_accuracy_trend(self, accuracy_list):
        plt.figure(figsize=(10, 6))
        plt.plot(accuracy_list, label="Accuracy (%)", color="blue")
        plt.title("Traffic Management Accuracy Over Time")
        plt.xlabel("Iterations")
        plt.ylabel("Accuracy (%)")
        plt.legend()
        plt.grid(True)
        os.makedirs('plots', exist_ok=True)
        plt.savefig('plots/accuracy_trend.png')
        plt.show()

    def display_data(self, vehicle_count, processed_vehicles, generation, accuracy):
        font = pygame.font.Font(None, 24)
        info_text = f"Vehicle Count: {vehicle_count} | Processed Vehicles: {processed_vehicles} | Generation: {generation} | Accuracy: {accuracy:.2f}%"
        info_surface = font.render(info_text, True, (0, 0, 0))
        self.screen.blit(info_surface, (20, 20))

    def run_simulation(self):
        running = True
        generation = 0
        stop_event = Event()

        accuracy_list = []
        old_dti = self.calculate_dti()

        try:
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                # Simulate traffic light changes (placeholder)
                # Simulate new traffic data
                new_vehicle_count = self.vehicle_parameters["vehicle_count"].copy()
                new_dti = self.calculate_dti()

                # Update Q-table for RL-based decision-making
                self.update_q_table(new_dti)

                # Calculate accuracy and log it
                accuracy = self.calculate_accuracy(old_dti, new_dti)
                accuracy_list.append(accuracy)
                print(f"Iteration {len(accuracy_list)} - Accuracy: {accuracy:.2f}%")

                # Update old metrics
                old_dti = new_dti.copy()

                # Redraw screen
                self.screen.fill(self.colors["intersection"]["WHITE"])
                self.display_data(
                    self.vehicle_parameters["vehicle_count"],
                    self.vehicle_parameters["processed_vehicles"],
                    generation,
                    accuracy
                )

                pygame.display.flip()
                pygame.time.wait(500)  # Adjust simulation speed
                generation += 1
        finally:
            stop_event.set()

            # Plot the accuracy trend after the simulation ends
            self.plot_accuracy_trend(accuracy_list)

if __name__ == "__main__":
    simulation = TrafficSimulation()
    simulation.run_simulation()



