import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

from canvas_auth import prompt_for_token
from canvas_api import suspend_user, unsuspend_user


class CanvasSuspendApp:
    def __init__(self, root):
        self.root = root
        root.title("Canvas – Suspend / Unsuspend Users")
        root.geometry("460x220")

        tk.Label(
            root,
            text="Suspend/Unsuspend Canvas accounts from CSV / Excel",
            font=("Arial", 11)
        ).pack(pady=15)

        tk.Button(
            root,
            text="Select File",
            width=25,
            command=self.load_file
        ).pack(pady=10)

    def load_file(self):
        file_path = filedialog.askopenfilename(
            title="Select CSV or Excel file",
            filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx *.xls")]
        )

        if not file_path:
            return

        try:
            if file_path.endswith(".csv"):
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read file:\n{e}")
            return

        if "Student No" not in df.columns:
            messagebox.showerror("Missing Column", 'Column "Student No" not found.')
            return

        self.students = df["Student No"].dropna().astype(str).unique().tolist()

        self.headers = prompt_for_token()
        if not self.headers:
            return

        self.choose_action()

    def choose_action(self):
        action_window = tk.Toplevel(self.root)
        action_window.title("Choose Action")
        action_window.geometry("440x250")
        action_window.grab_set()

        preview_text = (
            f"Students selected: {len(self.students)}\n\n"
            "First 10 SIS IDs:\n" +
            "\n".join(self.students[:10])
        )

        tk.Label(action_window, text=preview_text, justify="left", wraplength=400).pack(pady=15)

        chosen_action = {"value": None}

        def select(action):
            chosen_action["value"] = action
            action_window.destroy()

        btn_frame = tk.Frame(action_window)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Suspend", width=12, command=lambda: select("suspend")).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Un-suspend", width=12, command=lambda: select("unsuspend")).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Cancel", width=12, command=lambda: select(None)).grid(row=0, column=2, padx=5)

        action_window.wait_window()

        if chosen_action["value"]:
            self.show_processing_dialog()
            try:
                if chosen_action["value"] == "suspend":
                    self.run_suspension()
                else:
                    self.run_unsuspension()
            finally:
                self.processing_dialog.destroy()

    def show_processing_dialog(self):
        self.processing_dialog = tk.Toplevel(self.root)
        self.processing_dialog.title("Processing")
        self.processing_dialog.geometry("300x120")
        self.processing_dialog.grab_set()
        self.processing_dialog.resizable(False, False)

        tk.Label(self.processing_dialog, text="Processing, please wait...", font=("Arial", 11)).pack(pady=30)
        self.processing_dialog.protocol("WM_DELETE_WINDOW", lambda: None)  # disable closing

    def run_suspension(self):
        success, failed = 0, []
        for sis_id in self.students:
            try:
                suspend_user(int(sis_id.strip()), self.headers)
                success += 1
            except Exception as e:
                failed.append(f"{sis_id}: {e}")

        self.show_result("Suspended", success, failed)

    def run_unsuspension(self):
        success, failed = 0, []
        for sis_id in self.students:
            try:
                unsuspend_user(int(sis_id.strip()), self.headers)
                success += 1
            except Exception as e:
                failed.append(f"{sis_id}: {e}")

        self.show_result("Unsuspended", success, failed)

    @staticmethod
    def show_result(action, success, failed):
        msg = f"{action}: {success}"
        if failed:
            msg += f"\nFailed: {len(failed)}\n\n" + "\n".join(failed[:10])
        messagebox.showinfo("Completed", msg)


if __name__ == "__main__":
    root = tk.Tk()
    app = CanvasSuspendApp(root)
    root.mainloop()
