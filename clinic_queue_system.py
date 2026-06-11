import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

# ---------- BACKEND LOGIC (Modular) ----------
patients = []
next_id = 1


def add_patient_logic(name, age, symptoms, priority):
    global next_id
    if not name or not age or not symptoms:
        return False, "All fields required"
    try:
        age = int(age)
    except:
        return False, "Age must be a number"

    patient = {
        "id": next_id,
        "name": name,
        "age": age,
        "symptoms": symptoms,
        "priority": priority,  # "Emergency" or "Normal"
        "arrival_time": datetime.now()
    }
    patients.append(patient)
    next_id += 1
    return True, f"Patient {name} added. Queue position: {len(patients)}"


def process_next_patient_logic():
    if not patients:
        return None, "No patients in queue"
    # Priority: Emergency first, then by arrival time
    emergency = [p for p in patients if p["priority"] == "Emergency"]
    normal = [p for p in patients if p["priority"] == "Normal"]
    emergency.sort(key=lambda x: x["arrival_time"])
    normal.sort(key=lambda x: x["arrival_time"])
    sorted_queue = emergency + normal
    next_patient = sorted_queue[0]
    patients.remove(next_patient)
    return next_patient, f"Now processing: {next_patient['name']} (ID: {next_patient['id']})"


def get_queue_display():
    if not patients:
        return "Queue is empty"
    # Sort same way
    emergency = [p for p in patients if p["priority"] == "Emergency"]
    normal = [p for p in patients if p["priority"] == "Normal"]
    emergency.sort(key=lambda x: x["arrival_time"])
    normal.sort(key=lambda x: x["arrival_time"])
    sorted_queue = emergency + normal
    output = "Current Queue:\n"
    for idx, p in enumerate(sorted_queue, 1):
        output += f"{idx}. {p['name']} ({p['priority']}) - {p['symptoms']}\n"
    return output


# ---------- GUI ----------
class ClinicQueueApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Clinic Queue System - Sierra Leone")
        self.root.geometry("600x500")

        # Input Frame
        frame = tk.LabelFrame(root, text="Patient Registration", padx=10, pady=10)
        frame.pack(padx=10, pady=10, fill="x")

        tk.Label(frame, text="Name:").grid(row=0, column=0, sticky="w")
        self.name_entry = tk.Entry(frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Age:").grid(row=1, column=0, sticky="w")
        self.age_entry = tk.Entry(frame, width=30)
        self.age_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Symptoms:").grid(row=2, column=0, sticky="w")
        self.symptoms_entry = tk.Entry(frame, width=30)
        self.symptoms_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame, text="Priority:").grid(row=3, column=0, sticky="w")
        self.priority_var = tk.StringVar(value="Normal")
        tk.Radiobutton(frame, text="Emergency", variable=self.priority_var, value="Emergency").grid(row=3, column=1,
                                                                                                    sticky="w")
        tk.Radiobutton(frame, text="Normal", variable=self.priority_var, value="Normal").grid(row=3, column=2,
                                                                                              sticky="w")

        # Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Add Patient", command=self.add_patient_gui, width=15, bg="lightblue").grid(row=0,
                                                                                                              column=0,
                                                                                                              padx=5)
        tk.Button(btn_frame, text="Process Next", command=self.process_next_gui, width=15, bg="lightgreen").grid(row=0,
                                                                                                                 column=1,
                                                                                                                 padx=5)
        tk.Button(btn_frame, text="Show Queue", command=self.show_queue_gui, width=15).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Clear Fields", command=self.clear_fields, width=15).grid(row=0, column=3, padx=5)
        tk.Button(btn_frame, text="Exit", command=self.exit_app, width=15, bg="red", fg="white").grid(row=0, column=4,
                                                                                                      padx=5)

        # Output Area
        self.output_area = tk.Text(root, height=15, width=70)
        self.output_area.pack(padx=10, pady=10)

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = tk.Label(root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def add_patient_gui(self):
        name = self.name_entry.get()
        age = self.age_entry.get()
        symptoms = self.symptoms_entry.get()
        priority = self.priority_var.get()

        success, msg = add_patient_logic(name, age, symptoms, priority)
        if success:
            self.status_var.set(msg)
            self.clear_fields()
            messagebox.showinfo("Success", msg)
        else:
            self.status_var.set("Error: " + msg)
            messagebox.showerror("Error", msg)

    def process_next_gui(self):
        patient, msg = process_next_patient_logic()
        if patient:
            self.output_area.insert(tk.END, f"\n--- {msg} ---\n")
            self.output_area.see(tk.END)
            self.status_var.set(f"Processed {patient['name']}")
            messagebox.showinfo("Process", msg)
        else:
            self.status_var.set("Queue empty")
            messagebox.showwarning("No Patients", msg)

    def show_queue_gui(self):
        display = get_queue_display()
        self.output_area.delete(1.0, tk.END)
        self.output_area.insert(tk.END, display)
        self.status_var.set("Queue displayed")

    def clear_fields(self):
        self.name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.symptoms_entry.delete(0, tk.END)
        self.priority_var.set("Normal")

    def exit_app(self):
        if messagebox.askyesno("Exit", "Are you sure?"):
            self.root.destroy()


# ---------- MAIN ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = ClinicQueueApp(root)
    root.mainloop()