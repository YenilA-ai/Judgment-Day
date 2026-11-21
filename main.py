
import tkinter as tk
from environment import GridEnvironment
from human_agents import JohnConnor


class SimulationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Terminator 2: Judgment Day")
        self.root.geometry("1280x900")
        self.root.minsize(1150, 780)
        self.root.configure(bg="#101820")

        self.cell_size = 28
        self.environment = GridEnvironment(cell_size=self.cell_size)
        self.john = JohnConnor(self.environment)

        self.threat_position = None
        self.running = False
        self.after_id = None
        self.last_action = "Simulation ready"

        self.build_interface()
        self.update_display()

        self.add_log("Simulation environment initialised.")
        self.add_log("John Connor entered the environment.")

    def build_interface(self):
        header = tk.Frame(self.root, bg="#172635", height=75)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="TERMINATOR 2",
            font=("Arial", 22, "bold"),
            fg="#E5EDF5",
            bg="#172635"
        ).pack(side="left", padx=22, pady=15)

        tk.Label(
            header,
            text="JUDGMENT DAY SIMULATION",
            font=("Arial", 10, "bold"),
            fg="#6FA8DC",
            bg="#172635"
        ).pack(side="left", pady=24)

        main_area = tk.Frame(self.root, bg="#101820")
        main_area.pack(fill="both", expand=True, padx=18, pady=14)

        map_panel = tk.Frame(main_area, bg="#172635")
        map_panel.pack(side="left", fill="both", expand=True, padx=(0, 14))

        tk.Label(
            map_panel,
            text="SIMULATION ENVIRONMENT",
            font=("Arial", 12, "bold"),
            fg="#E5EDF5",
            bg="#172635"
        ).pack(anchor="w", padx=15, pady=12)

        canvas_width = self.environment.columns * self.cell_size
        canvas_height = self.environment.rows * self.cell_size

        self.canvas = tk.Canvas(
            map_panel,
            width=canvas_width,
            height=canvas_height,
            bg="#101820",
            highlightthickness=0
        )
        self.canvas.pack(padx=12, pady=(0, 10))

        self.create_terrain_legend(map_panel)

        side_panel = tk.Frame(
            main_area,
            bg="#172635",
            width=340
        )
        side_panel.pack(side="right", fill="y")
        side_panel.pack_propagate(False)

        self.create_agent_panel(side_panel)
        self.create_control_panel(side_panel)
        self.create_log_panel(side_panel)

        footer = tk.Frame(self.root, bg="#172635", height=32)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)

        tk.Label(
            footer,
            text="SIMULATION STATUS",
            font=("Arial", 8, "bold"),
            fg="#6FA8DC",
            bg="#172635"
        ).pack(side="left", padx=15, pady=7)

        self.footer_status = tk.Label(
            footer,
            text="READY",
            font=("Arial", 8, "bold"),
            fg="#77BFA3",
            bg="#172635"
        )
        self.footer_status.pack(side="left")

    def create_terrain_legend(self, parent):
        legend_panel = tk.Frame(parent, bg="#203246")
        legend_panel.pack(fill="x", padx=12, pady=(0, 12))

        tk.Label(
            legend_panel,
            text="TERRAIN LEGEND",
            font=("Arial", 9, "bold"),
            fg="#6FA8DC",
            bg="#203246"
        ).pack(anchor="w", padx=10, pady=(8, 5))

        items = [
            ("Ground", "#D9E2D0"),
            ("Road", "#777777"),
            ("Building", "#455A64"),
            ("Restricted", "#C65D5D"),
            ("Hazard", "#E5A83B"),
            ("Safe zone", "#77BFA3"),
            ("John Connor", "#39B6E8"),
            ("Threat", "#E74C3C")
        ]

        items_frame = tk.Frame(legend_panel, bg="#203246")
        items_frame.pack(fill="x", padx=8, pady=(0, 8))

        for index, (name, color) in enumerate(items):
            item = tk.Frame(items_frame, bg="#203246")
            item.grid(
                row=index // 4,
                column=index % 4,
                sticky="w",
                padx=5,
                pady=4
            )

            tk.Label(
                item,
                text="  ",
                bg=color,
                width=2,
                relief="flat"
            ).pack(side="left", padx=(0, 5))

            tk.Label(
                item,
                text=name,
                font=("Arial", 8),
                fg="#DCE6F0",
                bg="#203246"
            ).pack(side="left")

    def create_agent_panel(self, parent):
        panel = tk.Frame(
            parent,
            bg="#203246",
            padx=14,
            pady=12
        )
        panel.pack(fill="x", padx=12, pady=(12, 8))

        tk.Label(
            panel,
            text="HUMAN AGENT",
            font=("Arial", 10, "bold"),
            fg="#6FA8DC",
            bg="#203246"
        ).pack(anchor="w")

        tk.Label(
            panel,
            text="JOHN CONNOR",
            font=("Arial", 17, "bold"),
            fg="#FFFFFF",
            bg="#203246"
        ).pack(anchor="w", pady=(8, 2))

        self.health_label = tk.Label(
            panel,
            text="Health: 100 / 100",
            font=("Arial", 10),
            fg="#DCE6F0",
            bg="#203246"
        )
        self.health_label.pack(anchor="w", pady=(8, 4))

        self.health_canvas = tk.Canvas(
            panel,
            width=280,
            height=15,
            bg="#34495E",
            highlightthickness=0
        )
        self.health_canvas.pack(anchor="w")

        self.state_label = tk.Label(
            panel,
            text="Behaviour: Seeking Safety",
            font=("Arial", 10, "bold"),
            fg="#77BFA3",
            bg="#203246"
        )
        self.state_label.pack(anchor="w", pady=(12, 5))

        self.position_label = tk.Label(
            panel,
            text="Position: (10, 2)",
            font=("Arial", 10),
            fg="#DCE6F0",
            bg="#203246"
        )
        self.position_label.pack(anchor="w", pady=3)

        self.distance_label = tk.Label(
            panel,
            text="Distance travelled: 0",
            font=("Arial", 10),
            fg="#DCE6F0",
            bg="#203246"
        )
        self.distance_label.pack(anchor="w", pady=3)

        self.threat_label = tk.Label(
            panel,
            text="Threat: Not detected",
            font=("Arial", 10),
            fg="#77BFA3",
            bg="#203246"
        )
        self.threat_label.pack(anchor="w", pady=3)

    def create_control_panel(self, parent):
        panel = tk.Frame(
            parent,
            bg="#203246",
            padx=14,
            pady=12
        )
        panel.pack(fill="x", padx=12, pady=8)

        tk.Label(
            panel,
            text="SIMULATION CONTROLS",
            font=("Arial", 10, "bold"),
            fg="#6FA8DC",
            bg="#203246"
        ).pack(anchor="w", pady=(0, 8))

        self.create_button(
            panel, "START",
            self.start_simulation, "#287A60"
        )

        self.create_button(
            panel, "PAUSE",
            self.pause_simulation, "#A56D35"
        )

        self.create_button(
            panel, "STEP",
            self.step_simulation, "#356A9A"
        )

        self.create_button(
            panel, "TEST THREAT",
            self.toggle_threat, "#A94444"
        )

        self.create_button(
            panel, "RESET",
            self.reset_simulation, "#566573"
        )

    def create_button(self, parent, label, command, color):
        button = tk.Button(
            parent,
            text=label,
            command=command,
            font=("Arial", 9, "bold"),
            fg="white",
            bg=color,
            activebackground=color,
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=7
        )
        button.pack(fill="x", pady=3)

    def create_log_panel(self, parent):
        panel = tk.Frame(
            parent,
            bg="#203246",
            padx=12,
            pady=12
        )
        panel.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=8
        )

        tk.Label(
            panel,
            text="SIMULATION EVENT LOG",
            font=("Arial", 10, "bold"),
            fg="#6FA8DC",
            bg="#203246"
        ).pack(anchor="w", pady=(0, 8))

        log_frame = tk.Frame(panel, bg="#101820")
        log_frame.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(log_frame)
        scrollbar.pack(side="right", fill="y")

        self.event_log = tk.Text(
            log_frame,
            height=8,
            bg="#101820",
            fg="#DCE6F0",
            font=("Consolas", 9),
            relief="flat",
            wrap="word",
            state="disabled",
            yscrollcommand=scrollbar.set
        )
        self.event_log.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.config(command=self.event_log.yview)

    def create_log_entry(self, message):
        self.event_log.configure(state="normal")
        self.event_log.insert("end", message + "\n")
        self.event_log.see("end")
        self.event_log.configure(state="disabled")

    def add_log(self, message):
        self.create_log_entry(message)

    def draw_map(self):
        self.canvas.delete("all")
        self.environment.draw(self.canvas)

        row, col = self.john.position

        x = col * self.cell_size + self.cell_size // 2
        y = row * self.cell_size + self.cell_size // 2

        self.canvas.create_oval(
            x - 11,
            y - 11,
            x + 11,
            y + 11,
            fill="#39B6E8",
            outline="white",
            width=2
        )

        self.canvas.create_text(
            x,
            y,
            text="J",
            fill="white",
            font=("Arial", 9, "bold")
        )

        if self.threat_position is not None:
            threat_row, threat_col = self.threat_position

            threat_x = (
                threat_col * self.cell_size
                + self.cell_size // 2
            )
            threat_y = (
                threat_row * self.cell_size
                + self.cell_size // 2
            )

            self.canvas.create_oval(
                threat_x - 11,
                threat_y - 11,
                threat_x + 11,
                threat_y + 11,
                fill="#E74C3C",
                outline="white",
                width=2
            )

            self.canvas.create_text(
                threat_x,
                threat_y,
                text="T",
                fill="white",
                font=("Arial", 9, "bold")
            )

    def update_display(self):
        self.draw_map()

        self.health_label.config(
            text=f"Health: {self.john.health} / {self.john.max_health}"
        )

        self.health_canvas.delete("all")

        max_health = max(self.john.max_health, 1)
        health_width = 280 * self.john.health / max_health

        if self.john.health > 50:
            health_color = "#43B581"
        elif self.john.health > 20:
            health_color = "#E5A83B"
        else:
            health_color = "#E74C3C"

        self.health_canvas.create_rectangle(
            0,
            0,
            health_width,
            15,
            fill=health_color,
            outline=""
        )

        state = self.john.state.replace("_", " ").title()

        self.state_label.config(
            text=f"Behaviour: {state}"
        )

        if self.john.state == "safe":
            state_color = "#43B581"
        elif self.john.state in ("evading", "searching_for_safety"):
            state_color = "#E5A83B"
        elif self.john.state == "eliminated":
            state_color = "#E74C3C"
        else:
            state_color = "#77BFA3"

        self.state_label.config(fg=state_color)

        self.position_label.config(
            text=f"Position: {self.john.position}"
        )

        self.distance_label.config(
            text=f"Distance travelled: {self.john.distance_travelled}"
        )

        if self.john.detected_threat is not None:
            threat_text = "Threat: Detected"
            threat_color = "#E57373"
        else:
            threat_text = "Threat: Not detected"
            threat_color = "#77BFA3"

        self.threat_label.config(
            text=threat_text,
            fg=threat_color
        )

        if self.running:
            self.footer_status.config(
                text="RUNNING",
                fg="#43B581"
            )
        elif not self.john.alive:
            self.footer_status.config(
                text="ELIMINATED",
                fg="#E74C3C"
            )
        else:
            self.footer_status.config(
                text="PAUSED",
                fg="#77BFA3"
            )

    def step_simulation(self):
        if not self.john.alive:
            self.add_log("John Connor is eliminated.")
            return

        action = self.john.update(self.threat_position)

        self.last_action = action

        messages = {
            "moving_to_safety": "John moved towards the safe zone.",
            "evading_threat": "John changed position to evade the threat.",
            "waiting": "John is waiting for a safe route.",
            "no_safe_escape": "John could not find a safe escape.",
            "movement_blocked": "John's movement was blocked.",
            "eliminated": "John Connor has been eliminated."
        }

        self.add_log(messages.get(action, action))
        self.update_display()

    def start_simulation(self):
        if not self.john.alive or self.running:
            return

        self.running = True
        self.update_display()
        self.add_log("Simulation started.")

        self.after_id = self.root.after(700, self.auto_step)

    def auto_step(self):
        self.after_id = None

        if not self.running:
            return

        self.step_simulation()

        if self.running and self.john.alive:
            self.after_id = self.root.after(700, self.auto_step)
        else:
            self.running = False
            self.update_display()

    def pause_simulation(self):
        if self.running:
            self.running = False

            if self.after_id is not None:
                self.root.after_cancel(self.after_id)
                self.after_id = None

            self.add_log("Simulation paused.")
            self.update_display()

    def toggle_threat(self):
        if self.threat_position is None:
            self.threat_position = (10, 4)
            self.add_log("Test threat activated.")
        else:
            self.threat_position = None
            self.add_log("Test threat deactivated.")

        self.update_display()

    def reset_simulation(self):
        self.running = False

        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None

        self.environment = GridEnvironment(
            cell_size=self.cell_size
        )
        self.john = JohnConnor(self.environment)

        self.threat_position = None
        self.last_action = "Simulation reset"

        self.event_log.configure(state="normal")
        self.event_log.delete("1.0", "end")
        self.event_log.configure(state="disabled")

        self.add_log("Simulation reset.")
        self.add_log("John Connor returned to his starting position.")

        self.update_display()


def main():
    root = tk.Tk()
    SimulationApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()