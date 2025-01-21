import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
import subprocess
from datetime import datetime
from collections import defaultdict
import webbrowser
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import ttkbootstrap as ttk 
import matplotlib.pyplot as plt
import textwrap


class CPJournalGUI:
    def open_link(self, event):
        webbrowser.open_new(event.widget.cget("text"))
    def __init__(self, root):
        self.root = root
        self.root.title("Competitive Programming Journal")
        self.root.geometry("1600x1200")
        
        # Initialize data
        self.problemsfile = "problems.json"
        self.problems = self.load_problems()
        self.contestsfile = "contests.json"
        self.contests = self.load_contests()
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=5)
        
        # Create tabs
        self.create_add_entry_tab()
        self.create_edit_entry_tab()
        self.create_stats_tab()
        self.create_search_tab()
        self.create_plot_tab()
        self.create_timer_tab()
        self.create_cpp_testing_tab()
        self.create_contests_tab()
        
        

        
        
    def load_problems(self):
        if os.path.exists(self.problemsfile):
            with open(self.problemsfile, 'r') as f:
                return json.load(f)
        return []
    
    def load_contests(self):
        if os.path.exists(self.contestsfile):
            with open(self.contestsfile, 'r') as f:
                return json.load(f)
        return []
    
    def save_problems(self):
        with open(self.problemsfile, 'w') as f:
            json.dump(self.problems, f, indent=2)

    def save_contests(self):
        with open(self.contestsfile, 'w') as f:
            json.dump(self.contests, f, indent=2)
            
    def create_add_entry_tab(self):
        contest_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(contest_frame, text="Add Contest/Problem")

        #Will use the same fields as add entry tab, but with more fields for contest info
        # Entry fields
        ttk.Label(contest_frame, text="Problem Name:").grid(row=0, column=0, sticky='w', pady=5)
        self.problem_name = ttk.Entry(contest_frame, width=40)
        self.problem_name.grid(row=0, column=1, sticky='w', pady=5)
        
        ttk.Label(contest_frame, text="Difficulty Level:").grid(row=1, column=0, sticky='w', pady=5)
        self.difficulty = ttk.Entry(contest_frame, width=40)
        self.difficulty.grid(row=1, column=1, sticky='w', pady=5)
        
        ttk.Label(contest_frame, text="Topics (comma-separated):").grid(row=2, column=0, sticky='w', pady=5)
        self.topics = ttk.Entry(contest_frame, width=40)
        self.topics.grid(row=2, column=1, sticky='w', pady=5)
        
        ttk.Label(contest_frame, text="Time Spent (MM:SS):").grid(row=3, column=0, sticky='w', pady=5)
        self.time_spent = ttk.Entry(contest_frame, width=40)
        self.time_spent.grid(row=3, column=1, sticky='w', pady=5)
        
        self.passed_var = tk.BooleanVar()
        ttk.Checkbutton(contest_frame, text="Passed", variable=self.passed_var).grid(row=4, column=1, sticky='w', pady=5)

        self.solved_in_contest_var = tk.BooleanVar()
        ttk.Checkbutton(contest_frame, text="Solved in contest", variable=self.solved_in_contest_var).grid(row=4, column=0, sticky='w', pady=5)

        
        ttk.Label(contest_frame, text="Learnings:").grid(row=5, column=0, sticky='w', pady=5)
        self.learnings = scrolledtext.ScrolledText(contest_frame, width=40, height=5)
        self.learnings.grid(row=5, column=1, sticky='w', pady=5)

        ttk.Label(contest_frame, text="Link: ").grid(row=6, column=0, sticky='w', pady=5)
        self.link = ttk.Entry(contest_frame, width=40)
        self.link.grid(row=6, column=1, sticky='w', pady=5)

        #Number of attempts
        ttk.Label(contest_frame, text="Number of Attempts").grid(row=7, column=0, sticky='w', pady=5)
        self.num_attempts = ttk.Entry(contest_frame, width=40)
        self.num_attempts.grid(row=7, column=1, sticky='w', pady=5)

        # Contest id (leave blank if not part of a contest)
        ttk.Label(contest_frame, text="Contest ID (leave blank if no contest):").grid(row=8, column=0, sticky='w', pady=5)
        self.contest_id = ttk.Entry(contest_frame, width=40)
        self.contest_id.grid(row=8, column=1, sticky='w', pady=5)

        
        ttk.Button(contest_frame, text="Save Entry", command=self.save_entry, style='primary.TButton').grid(row=9, column=1, sticky='w', pady=20)

        #Contest specific fields
        ttk.Label(contest_frame, text="Contest Name:").grid(row=0, column=3, sticky='w', pady=5)
        self.contest_name = ttk.Entry(contest_frame, width=40)
        self.contest_name.grid(row=0, column=4, sticky='w', pady=5)

        ttk.Label(contest_frame, text="Contest Date:").grid(row=1, column=3, sticky='w', pady=5)
        self.contest_date = ttk.Entry(contest_frame, width=40)
        self.contest_date.grid(row=1, column=4, sticky='w', pady=5)

        ttk.Label(contest_frame, text="Contest Duration (HH:MM):").grid(row=2, column=3, sticky='w', pady=5)
        self.contest_duration = ttk.Entry(contest_frame, width=40)
        self.contest_duration.grid(row=2, column=4, sticky='w', pady=5)

        ttk.Label(contest_frame, text="Contest Rank:").grid(row=3, column=3, sticky='w', pady=5)
        self.contest_rank = ttk.Entry(contest_frame, width=40)
        self.contest_rank.grid(row=3, column=4, sticky='w', pady=5)

        ttk.Label(contest_frame, text="Contest Rating Change:").grid(row=4, column=3, sticky='w', pady=5)
        self.contest_rating_change = ttk.Entry(contest_frame, width=40)
        self.contest_rating_change.grid(row=4, column=4, sticky='w', pady=5)

        ttk.Label(contest_frame, text="Contest Learnings:").grid(row=5, column=3, sticky='w', pady=5)
        self.contest_learnings = scrolledtext.ScrolledText(contest_frame, width=40, height=5)
        self.contest_learnings.grid(row=5, column=4, sticky='w', pady=5)

        ttk.Label(contest_frame, text="Contest Link: ").grid(row=6, column=3, sticky='w', pady=5)
        self.contest_link = ttk.Entry(contest_frame, width=40)
        self.contest_link.grid(row=6, column=4, sticky='w', pady=5)

        ttk.Button(contest_frame, text="Save Contest", command=self.save_contest, style='primary.TButton').grid(row=7, column=4, sticky='w', pady=20)

    def save_contest(self):
        try:
            entry = {
                "contest_name": self.contest_name.get(),
                "contest_date": self.contest_date.get(),
                "contest_duration": self.contest_duration.get(),
                "contest_rank": self.contest_rank.get(),
                "contest_rating_change": self.contest_rating_change.get(),
                "contest_learnings": self.contest_learnings.get("1.0", tk.END).strip(),
                "contest_link": self.contest_link.get(),
                "contest_id": len(self.contests)+1,
                "problems": []
            }
            
            self.contests.append(entry)
            self.save_contests()
            
            # Clear fields
            self.problem_name.delete(0, tk.END)
            self.difficulty.delete(0, tk.END)
            self.topics.delete(0, tk.END)
            self.time_spent.delete(0, tk.END)
            self.passed_var.set(False)
            self.learnings.delete("1.0", tk.END)
            self.link.delete(0, tk.END)
            self.contest_name.delete(0, tk.END)
            self.contest_date.delete(0, tk.END)
            self.contest_duration.delete(0, tk.END)
            self.contest_rank.delete(0, tk.END)
            self.contest_rating_change.delete(0, tk.END)
            self.contest_learnings.delete("1.0", tk.END)
            self.contest_link.delete(0, tk.END)
            
            messagebox.showinfo("Success", "Entry saved successfully! Contest ID: " + str(entry["contest_id"]))
            self.update_stats()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save entry: {str(e)}")

    def copy_template(self):
        #copy template code to clipboard
        self.root.clipboard_clear()
        self.root.clipboard_append(self.template_code)
        self.root.update()

    def on_tab_code(self, event):
        # Get the current line number
        current_line = self.code_text.index(tk.INSERT).split('.')[0]
        
        # Get the previous line's content to check indentation level
        previous_line = self.code_text.get(f"{int(current_line)-1}.0", f"{int(current_line)-1}.end")
        
        # Count leading spaces/tabs of the previous line
        leading_spaces = len(previous_line) - len(previous_line.lstrip(' '))

        # Insert the same amount of indentation as the previous line
        self.code_text.insert(tk.INSERT, ' ' * leading_spaces)
        
        return "break"  # Prevent the default behavior of the Tab key
    def create_cpp_testing_tab(self):
        cpp_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(cpp_frame, text="C++ Testing")

        # Timer
        #Big timer in the middle of the page
        self.timer = ttk.Entry(cpp_frame, width=12, font=('Helvetica', 40), justify='center')
        self.timer.grid(row=0, column=0, sticky='w')
        self.timer.insert(0, "00:00")
        self.timer.config(state='readonly')

        #Start button
        timer_start = ttk.Button(cpp_frame, text="Start", command=self.start_timer,
                        width=30)  # Set background to green and text to white
        timer_start.grid(row=1, column=0, sticky='w')  # Anchor to the left, but no expansion
        #Stop button
        timer_stop = ttk.Button(cpp_frame, text="Stop", command=self.stop_timer, width=30)
        timer_stop.grid(row=2, column=0, sticky='w')

        #Reset button
        timer_reset = ttk.Button(cpp_frame, text="Reset", command=self.reset_timer, width=30)
        timer_reset.grid(row=3, column=0, sticky='w')

        #Timer variables
        self.timer_running = False
        self.timer_start = None
        self.timer_id = None

        #Template code - underneath timer
        with open("template.cpp", "r") as f:
            self.template_code = f.read()

        self.template_text = tk.Text(cpp_frame, width=30, height=20)
        self.template_text.insert(tk.END, self.template_code)
        self.template_text.grid(row=5, column=0, padx=0, pady=10)
        self.template_text.config(state='disabled')

        #button to copy template
        self.copy_template = ttk.Button(cpp_frame, text="Copy Template", command=self.copy_template, width=30)
        self.copy_template.grid(row=4, column=0, padx=10, pady=0, sticky='w')

        
        # Code editor area (Text widget)
        
        self.code_text = ttk.Text(cpp_frame, height=20, width=60)
        self.code_text.grid(rowspan = 4, row=0, column=1, padx=10, pady=10, sticky = 'n')
        self.code_text.bind("<Enter>", self.on_tab_code)
        self.code_text.config(tabs=12)

        # Compile and Run Button
        self.run_button = ttk.Button(cpp_frame, text="Compile & Run", command=self.compile_and_run, width=30)
        self.run_button.grid(row=4, column=1, padx=10, pady=0)

        # Output Display (Label or Text widget for the results)
        self.output_label = ttk.Text(cpp_frame, width=60, height=20)
        self.output_label.grid(row=5, column=1, padx=10, pady=10, sticky = 's')
        #default text
        self.output_label.insert(tk.END, "Output will be displayed here.")
        

        # Input box for test cases - label fills up entire row
        self.input_text = ttk.Text(cpp_frame, height=20, width=30)
        self.input_text.grid(row=5, column=2, padx=10, pady=10, sticky = 'n')
        self.input_text.insert(tk.END, "//Input test cases here.")

        # Box for problem statement
        self.problem_text = ttk.Text(cpp_frame, width=30, height = 20)
        self.problem_text.grid(rowspan = 4, row=0, column=2, padx=10, pady=10, sticky = 'n')
        self.problem_text.insert(tk.END, "Problem statement goes here.")



    def compile_and_run(self):
        # Save the code to a temporary file
        with open("temp.cpp", "w") as f:
            f.write(self.code_text.get("1.0", tk.END))

        # Compile the code
        try:
            subprocess.run(["g++", "temp.cpp", "-o", "temp.exe"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
        except subprocess.CalledProcessError as e:
            self.output_label.delete("1.0", tk.END)
            self.output_label.insert(tk.END, f"Compilation Error: {e.stderr.decode()}")
            return

        
        # Run the executable - wait for it to finish

        try:
            result = subprocess.run(["./temp.exe"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = result.stdout.decode()
            if not output:
                output = result.stderr.decode()
            self.output_label.delete("1.0", tk.END)
            self.output_label.insert(tk.END, output)
        except subprocess.CalledProcessError as e:
            self.output_label.delete("1.0", tk.END)
            self.output_label.insert(tk.END, f"Runtime Error: {e.stderr.decode()}")
                                     

    def create_timer_tab(self):
        cpp_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(cpp_frame, text="Timer")
        
        #Big timer in the middle of the page
        self.timer = ttk.Entry(cpp_frame, width=10, font=('Helvetica', 40))
        self.timer.grid(row=0, column=0, pady=10)
        self.timer.insert(0, "00:00")
        self.timer.config(state='readonly')

        #Start button
        ttk.Button(cpp_frame, text="Start", command=self.start_timer, style='primary.TButton').grid(row=1, column=0, sticky='w', pady=5)
        #Stop button
        ttk.Button(cpp_frame, text="Stop", command=self.stop_timer, style='primary.TButton').grid(row=2, column=0, sticky='w', pady=5)
        #Reset button
        ttk.Button(cpp_frame, text="Reset", command=self.reset_timer, style='primary.TButton').grid(row=3, column=0, sticky='w', pady=5)
        #Timer variables
        self.timer_running = False
        self.timer_start = None
        self.timer_id = None

    def toggle_timer(self, event):
        if self.timer_running:
            self.stop_timer()
        else:
            self.start_timer()

    def start_timer(self):
        if not self.timer_running:
            self.timer_start = datetime.now()
            self.timer_running = True
            self.timer_id = self.root.after(1000, self.update_timer)

    def stop_timer(self):
        if self.timer_running:
            self.timer_running = False
            self.root.after_cancel(self.timer_id)
    
    def reset_timer(self):
        self.stop_timer()
        self.timer.config(state='normal')
        self.timer.delete(0, tk.END)
        self.timer.insert(0, "00:00")
        self.timer.config(state='readonly')
        self.timer_running = False
        self.timer_start = None



    def update_timer(self):
        if self.timer_running:
            elapsed = datetime.now() - self.timer_start
            seconds = elapsed.total_seconds()
            minutes = int(seconds // 60)
            seconds = int(seconds % 60)
            self.timer.config(state='normal')
            self.timer.delete(0, tk.END)
            self.timer.insert(0, f"{minutes:02}:{seconds:02}")
            self.timer.config(state='readonly')
            self.timer_id = self.root.after(1000, self.update_timer)
    
        
    def create_stats_tab(self):
        stats_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(stats_frame, text="Statistics")
        
        self.overall_stats_text = scrolledtext.ScrolledText(stats_frame, width=70, height=30)
        self.overall_stats_text.pack(expand=True, fill='both', side='left')
        self.overall_stats_text.config(state='disabled')

        self.contest_stats_text = scrolledtext.ScrolledText(stats_frame, width=70, height=30)
        self.contest_stats_text.pack(expand=True, fill='both', side='right')
        self.contest_stats_text.config(state='disabled')
        
        self.update_stats()

        # Bind the event to update tabs on selection
        self.notebook.bind("<<NotebookTabChanged>>", self.update_stats)
        
    def create_search_tab(self):
        self.search_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.search_frame, text="Search")
        
        # Search bar
        search_box_frame = ttk.Frame(self.search_frame)
        search_box_frame.pack(fill='x', pady=5)
        
        self.search_entry = ttk.Entry(search_box_frame, width=50)
        self.search_entry.pack(side='left', padx=5)
        
        ttk.Button(search_box_frame, text="Search", command=self.perform_search, style='primary.TButton').pack(side='left', padx=5)

    def create_edit_entry_tab(self):
        edit_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(edit_frame, text="Edit Entry")

        # Entry fields
        ttk.Label(edit_frame, text="Problem ID:").grid(row=0, column=0, sticky='w', pady=5)
        self.problem_id = ttk.Entry(edit_frame, width=40)
        self.problem_id.grid(row=0, column=1, sticky='w', pady=5)
        self.problem_id.config(state='normal')

        #Same formatting as add entry tab
        ttk.Label(edit_frame, text="Problem Name:").grid(row=1, column=0, sticky='w', pady=5)
        self.edit_problem_name = ttk.Entry(edit_frame, width=40)
        self.edit_problem_name.grid(row=1, column=1, sticky='w', pady=5)

        ttk.Label(edit_frame, text="Difficulty Level:").grid(row=2, column=0, sticky='w', pady=5)
        self.edit_difficulty = ttk.Entry(edit_frame, width=40)
        self.edit_difficulty.grid(row=2, column=1, sticky='w', pady=5)

        ttk.Label(edit_frame, text="Topics (comma-separated):").grid(row=3, column=0, sticky='w', pady=5)
        self.edit_topics = ttk.Entry(edit_frame, width=40)
        self.edit_topics.grid(row=3, column=1, sticky='w', pady=5)

        ttk.Label(edit_frame, text="Time Spent (MM:SS):").grid(row=4, column=0, sticky='w', pady=5)
        self.edit_time_spent = ttk.Entry(edit_frame, width=40)
        self.edit_time_spent.grid(row=4, column=1, sticky='w', pady=5)

        self.edit_passed_var = tk.BooleanVar()
        ttk.Checkbutton(edit_frame, text="Passed", variable=self.edit_passed_var).grid(row=5, column=1, sticky='w', pady=5)

        ttk.Label(edit_frame, text="Learnings:").grid(row=6, column=0, sticky='w', pady=5)
        self.edit_learnings = scrolledtext.ScrolledText(edit_frame, width=40, height=5)
        self.edit_learnings.grid(row=6, column=1, sticky='w', pady=5)

        ttk.Label(edit_frame, text="Link: ").grid(row=7, column=0, sticky='w', pady=5)
        self.edit_link = ttk.Entry(edit_frame, width=40)
        self.edit_link.grid(row=7, column=1, sticky='w', pady=5)

        ttk.Button(edit_frame, text="Fill from Problem ID", command=self.find_problem, style='primary.TButton').grid(row=0, column=2, sticky='w', pady=5)

        ttk.Button(edit_frame, text="Submit Edit", command=self.edit_entry, style='primary.TButton').grid(row=1, column=2, sticky='w', pady=20)

    def edit_entry(self):
        #retrieve problem info from problem id
        problem_id = self.problem_id.get()
        try:
            problem_id = int(problem_id)
            entry = next(p for p in self.problems if p["problem_id"] == problem_id)
            entry.update({
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "problem_name": self.edit_problem_name.get(),
                "difficulty": self.edit_difficulty.get(),
                "topics": [t.strip() for t in self.edit_topics.get().split(",")],
                "passed": self.edit_passed_var.get(),
                "time_spent": self.edit_time_spent.get(),
                "learnings": self.edit_learnings.get("1.0", tk.END).strip(),
                "link": self.edit_link.get(),
            })

            self.save_problems()
            messagebox.showinfo("Success", "Entry updated successfully!")
            self.update_stats()
            
        except (ValueError, StopIteration):
            messagebox.showerror("Error", "Problem ID not found.")
            return


    def find_problem(self):
        #retrieve problem info from problem id
        problem_id = self.problem_id.get()
        try:
            problem_id = int(problem_id)
            entry = next(p for p in self.problems if p["problem_id"] == problem_id)

            # Clear and fill in fields
            self.edit_problem_name.delete(0, tk.END)
            self.edit_difficulty.delete(0, tk.END)
            self.edit_topics.delete(0, tk.END)
            self.edit_time_spent.delete(0, tk.END)
            self.edit_learnings.delete("1.0", tk.END)
            self.edit_link.delete(0, tk.END)

            self.edit_problem_name.insert(0, entry["problem_name"])
            self.edit_difficulty.insert(0, entry["difficulty"])
            self.edit_topics.insert(0, ", ".join(entry["topics"]))
            self.edit_time_spent.insert(0, entry["time_spent"])
            self.edit_passed_var.set(entry["passed"])
            self.edit_learnings.insert(tk.END, entry["learnings"])
            self.edit_link.insert(0, entry["link"])

        except (ValueError, StopIteration):
            messagebox.showerror("Error", "Problem ID not found.")
            return

    def create_plot_tab(self):
        plot_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(plot_frame, text="Performance Graph")

        # Create a figure and plot on it
        fig, ax = plt.subplots(figsize=(8, 5))
        topics = []
        ratings = []
        colors = []
        for entry in self.problems:
            for topic in entry["topics"]:
                topics.append(topic)
                ratings.append(entry["difficulty"])
                colors.append("green" if entry["passed"] else "red")

        ax.scatter(topics, ratings, c=colors)
        ax.set_xlabel("Topics")
        ax.set_ylabel("Difficulty")
        ax.set_title("Performance Graph")
        ax.invert_yaxis()  # Invert y-axis to have the highest rating at the top
        fig.tight_layout()

        # Embed the plot in the Tkinter tab
        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill='both')

        
    def save_entry(self):
        try:
            entry = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "problem_name": self.problem_name.get(),
                "difficulty": self.difficulty.get(),
                "topics": [t.strip() for t in self.topics.get().split(",")],
                "passed": self.passed_var.get(),
                "solved_in_contest": self.solved_in_contest_var.get(),
                "time_spent": self.time_spent.get(),
                "learnings": self.learnings.get("1.0", tk.END).strip(),
                "link": self.link.get(),
                "num_attempts": self.num_attempts.get(),
                "problem_id": len(self.problems)+1,
                "contest_id": self.contest_id.get() if self.contest_id.get() else 0

            }
            
            #add problem to contest if applicable
            if entry["contest_id"]:
                for contest in self.contests:
                    if contest["contest_id"] == int(entry["contest_id"]):
                        contest["problems"].append(entry["problem_id"])
                        break
                self.save_contests()
            self.problems.append(entry)
            self.save_problems()
            
            # Clear fields
            self.problem_name.delete(0, tk.END)
            self.difficulty.delete(0, tk.END)
            self.topics.delete(0, tk.END)
            self.time_spent.delete(0, tk.END)
            self.passed_var.set(False)
            self.learnings.delete("1.0", tk.END)
            self.link.delete(0, tk.END)
            self.contest_id.delete(0, tk.END)
            self.solved_in_contest_var.set(False)
            
            messagebox.showinfo("Success", "Entry saved successfully!")
            self.update_stats()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save entry: {str(e)}")
    
    def update_stats(self):
        self.overall_stats_text.delete("1.0", tk.END)
        self.contest_stats_text.delete("1.0", tk.END)
        self.overall_stats_text.config(state='normal')
        self.contest_stats_text.config(state='normal')

        self.load_contests()
        self.load_problems()

        # Overall stats
        total = len(self.problems)
        if total == 0:
            self.overall_stats_text.insert(tk.END, "No problems yet!\n")
            return
            
        passed = sum(1 for entry in self.problems if entry["passed"])
        totalWithTime = sum(1 for entry in self.problems if entry["time_spent"] != 0)
        sumTime = 0
        #Parse time spent and calculate average time spent per problem
            #Format will be MM:SS

        for entry in self.problems:
            if entry["time_spent"] and entry["time_spent"] != "0":
                minutes, seconds = map(int, entry["time_spent"].split(':'))
                sumTime += minutes + seconds/60
            else:
                entry["time_spent"] = 0
        avg_time = sumTime/totalWithTime

        #Average problem difficulty
        #convert to int first
        difficulties = [int(entry["difficulty"]) for entry in self.problems]
        avg_difficulty = sum(difficulties) / total
        passed_difficulty = sum(difficulties[i] for i in range(total) if self.problems[i]["passed"]) / passed
        #Convert back to MM:SS format
        avg_time = str(int(avg_time)) + ":" + str(int((avg_time - int(avg_time))*60))
        overall_stats_text = "Overall Statistics:\n"
        overall_stats_text += "=" * 50 + "\n"
        overall_stats_text += f"Total problems attempted: {total}\n"
        overall_stats_text += f"Overall pass rate: {(passed/total*100):.1f}% ({passed}/{total})\n"
        overall_stats_text += f"Average time per problem: {avg_time}\n\n"
        overall_stats_text += f"Overall problem average difficulty: {avg_difficulty}\n\n"
        overall_stats_text += f"Passed problem average difficulty: {passed_difficulty}\n\n"
        
        # Topic stats
        topic_stats = defaultdict(lambda: {"total": 0, "passed": 0})
        for entry in self.problems:
            for topic in entry["topics"]:
                topic_stats[topic]["total"] += 1
                if entry["passed"]:
                    topic_stats[topic]["passed"] += 1
        
        overall_stats_text += "Topic-wise Statistics:\n"
        overall_stats_text += "=" * 50 + "\n"
        for topic, stats in topic_stats.items():
            pass_rate = (stats["passed"] / stats["total"] * 100)
            overall_stats_text += f"{topic}:\n"
            overall_stats_text += f"  Total attempts: {stats['total']}\n"
            overall_stats_text += f"  Pass rate: {pass_rate:.1f}%\n\n"
            
        # Difficulty stats
        diff_stats = defaultdict(lambda: {"total": 0, "passed": 0})
        for entry in self.problems:
            diff = entry["difficulty"]
            diff_stats[diff]["total"] += 1
            if entry["passed"]:
                diff_stats[diff]["passed"] += 1
                
        overall_stats_text += "Difficulty-wise Statistics:\n"
        overall_stats_text += "=" * 50 + "\n"
        for diff, stats in diff_stats.items():
            pass_rate = (stats["passed"] / stats["total"] * 100)
            overall_stats_text += f"Difficulty {diff}:\n"
            overall_stats_text += f"  Total attempts: {stats['total']}\n"
            overall_stats_text += f"  Pass rate: {pass_rate:.1f}%\n\n"
            
        self.overall_stats_text.insert(tk.END, overall_stats_text)

        # Contest stats - right side of the page
        contest_stats = "Contest Statistics:\n"
        contest_stats += "=" * 50 + "\n"
        total = len(self.contests)
        if total == 0:
            contest_stats += "No contests yet!\n"
            return
        passed = sum(1 for entry in self.contests if entry["contest_rank"] != 0)
        totalWithRating = sum(1 for entry in self.contests if entry["contest_rating_change"] != 0)
        sumRating = 0
        for entry in self.contests:
            if entry["contest_rating_change"] and entry["contest_rating_change"] != "0":
                sumRating += int(entry["contest_rating_change"])
            else:
                entry["contest_rating_change"] = 0
        avg_rating = sumRating/totalWithRating
        avg_rating = str(avg_rating)
        contest_stats += f"Total contests attempted: {total}\n"
        contest_stats += f"Overall pass rate: {(passed/total*100):.1f}% ({passed}/{total})\n"
        contest_stats += f"Average rating change per contest: {avg_rating}\n\n"
        self.contest_stats_text.insert(tk.END, contest_stats)

        self.overall_stats_text.config(state='disabled')
        self.contest_stats_text.config(state='disabled')

        
    def perform_search(self):
        keyword = self.search_entry.get().lower()
        
        matching_problems = []
        for entry in self.problems:
            if (keyword in entry["problem_name"].lower() or
            any(keyword in topic.lower() for topic in entry["topics"])):
                matching_problems.append(entry)
        
        if matching_problems:
            # Create a canvas and a scrollbar
            canvas = tk.Canvas(self.search_frame)
            scrollbar = ttk.Scrollbar(self.search_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)

            scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            # Make frame scrollable with trackpad or mousewheel
            def _on_mousewheel(event):
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
                canvas.bind_all("<MouseWheel>", _on_mousewheel)

            for entry in matching_problems:
                left_text = f"""
    Date: {entry['date']}
    Problem: {entry['problem_name']}
    Difficulty: {entry['difficulty']}
    Topics: {', '.join(entry['topics'])}
    Passed: {'Yes' if entry['passed'] else 'No'}
    Solved in Contest: {'Yes' if entry['solved_in_contest'] else 'No'}
    Time spent: {entry['time_spent']} minutes
    Number of Attempts: {entry['num_attempts']}
    Link: {entry['link']} 
    """
                right_text = f"""
    Contest ID: {entry['contest_id']}
    Problem ID: {entry['problem_id']}
    Learnings: {entry['learnings']}
    """
                
                left_label = ttk.Label(scrollable_frame, text=left_text, anchor='nw', wraplength=int(self.root.winfo_screenwidth() / 2.1))
                right_label = ttk.Label(scrollable_frame, text=right_text, anchor='nw', wraplength=int(self.root.winfo_screenwidth() / 2.1))

                left_label.grid(row=matching_problems.index(entry) * 2, column=0, sticky='w', pady=0)
                right_label.grid(row=matching_problems.index(entry) * 2, column=1, sticky='w', pady=0)

                # Make divider between entries - don't wrap
                ttk.Label(scrollable_frame, text="-" * 200).grid(row=matching_problems.index(entry) * 2 + 1, column=0, columnspan=2, sticky='nsew', pady=0)

                # Enforce that each cell in the grid is the same size
                scrollable_frame.grid_columnconfigure(0, weight=1)
                scrollable_frame.grid_columnconfigure(1, weight=1)
                scrollable_frame.grid_rowconfigure(matching_problems.index(entry), weight=1)
                scrollable_frame.grid_rowconfigure(matching_problems.index(entry) + 1, weight=0)

        else:
            no_match_label = ttk.Label(self.search_frame, text="No matching entries found.")
            no_match_label.pack(pady=10)

    def create_contests_tab(self):
        contests_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(contests_frame, text="View Contests")
        self.update_stats()
        self.load_contests()
        
        # Display all contests
        for entry in self.contests:
            contest_frame = ttk.Frame(contests_frame)
            contest_frame.pack(fill='x', pady=5)
            
            contest_info = f"""
Contest Name: {entry['contest_name']}
Date: {entry['contest_date']}
Duration: {entry['contest_duration']}
Rank: {entry['contest_rank']}
Rating Change: {entry['contest_rating_change']}
Learnings: {entry['contest_learnings']}
Link: {entry['contest_link']}"""
            #wrap after half width of screen without removing existing newlines
            contest_info = textwrap.fill(contest_info, width=50, replace_whitespace=False)
            ttk.Label(contest_frame, text=contest_info, anchor='w').pack(side='left', padx=10)
            
            if entry["problems"]:
                problems_info = "Problems:\n"
                for problem_id in entry["problems"]:
                    problem = next(p for p in self.problems if p["problem_id"] == problem_id)
                    problems_info += f"""
Problem: {problem['problem_name']}, Problem ID: {problem['problem_id']}, Passed: {'Yes' if problem['passed'] else 'No'}
"""
                ttk.Label(contest_frame, text=problems_info).pack(side='right',padx=10)
            
            ttk.Label(contests_frame, text="-" * 500).pack(fill='x', pady=5)


def main():
    root = ttk.Window(themename="cosmo")  # Using ttkbootstrap for modern styling
    app = CPJournalGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

