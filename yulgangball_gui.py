import tkinter as tk
from tkinter import messagebox
import random

class GuessTheBallGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Yulgang Ball - Guess the Number")
        self.root.geometry("500x600")
        self.root.configure(bg="#f0f0f0")

        self.max_rounds = 7
        self.current_round = 0
        self.secret_number = []
        self.game_over = False

        self._setup_ui()
        self.start_new_game()

    def _setup_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg="#4a90e2", pady=20)
        header_frame.pack(fill=tk.X)
        
        title_label = tk.Label(header_frame, text="✨ Guess the Ball ✨", font=("Helvetica", 24, "bold"), bg="#4a90e2", fg="white")
        title_label.pack()
        
        subtitle_label = tk.Label(header_frame, text="ทายเลข 3 หลักที่ไม่ซ้ำกัน (0-9)", font=("Helvetica", 12), bg="#4a90e2", fg="#e0e0e0")
        subtitle_label.pack()

        # Game Area
        game_frame = tk.Frame(self.root, bg="#f0f0f0", pady=20)
        game_frame.pack(fill=tk.BOTH, expand=True, padx=20)

        # Round Info
        self.round_label = tk.Label(game_frame, text="Round: 1 / 7", font=("Helvetica", 14, "bold"), bg="#f0f0f0", fg="#333")
        self.round_label.pack(pady=(0, 10))

        # Input Area
        input_frame = tk.Frame(game_frame, bg="#f0f0f0")
        input_frame.pack(pady=10)

        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(input_frame, textvariable=self.entry_var, font=("Courier", 24), width=5, justify='center', bd=2, relief="solid")
        self.entry.pack(side=tk.LEFT, padx=10)
        self.entry.bind('<Return>', self.check_guess)

        self.guess_btn = tk.Button(input_frame, text="ทาย!", command=self.check_guess, font=("Helvetica", 14, "bold"), bg="#4caf50", fg="black", activebackground="#45a049", cursor="hand2")
        self.guess_btn.pack(side=tk.LEFT)

        # Status Label (New)
        self.status_label = tk.Label(game_frame, text="", font=("Helvetica", 14), bg="#f0f0f0", fg="#d32f2f")
        self.status_label.pack(pady=5)

        # History / Log
        history_label = tk.Label(game_frame, text="ประวัติการทาย:", font=("Helvetica", 12, "underline"), bg="#f0f0f0", fg="#555")
        history_label.pack(anchor="w", pady=(10, 5))

        self.history_text = tk.Text(game_frame, height=10, font=("Courier", 14), state='disabled', bg="white", bd=1, relief="solid")
        self.history_text.pack(fill=tk.BOTH, expand=True)

        # Restart Button
        self.restart_btn = tk.Button(self.root, text="เริ่มเกมใหม่ 🔄", command=self.start_new_game, font=("Helvetica", 12), bg="#ff9800", fg="black", activebackground="#fb8c00", cursor="hand2")
        self.restart_btn.pack(pady=20)

    def start_new_game(self):
        self.secret_number = self._generate_secret_number()
        self.current_round = 0
        self.game_over = False
        self.entry_var.set("")
        self.entry.config(state='normal')
        self.guess_btn.config(state='normal')
        self.history_text.config(state='normal')
        self.history_text.delete(1.0, tk.END)
        self.history_text.config(state='disabled')
        if hasattr(self, 'status_label'):
            self.status_label.config(text="")
        self.update_round_label()
        print(f"Secret: {self.secret_number}") # Debug

    def _generate_secret_number(self):
        return random.sample("0123456789", 3)

    def update_round_label(self):
        self.round_label.config(text=f"Round: {self.current_round + 1} / {self.max_rounds}")

    def check_guess(self, event=None):
        print("Check guess triggered") # Debug
        if self.game_over:
            print("Game is over, ignoring guess") # Debug
            return

        guess = self.entry_var.get().strip()
        print(f"Guess received: '{guess}'") # Debug

        # Validation
        if len(guess) != 3 or not guess.isdigit():
            messagebox.showerror("Error", "กรุณาใส่ตัวเลข 3 หลักเท่านั้น!")
            return
        
        if len(set(guess)) < 3:
            messagebox.showwarning("Warning", "เลขต้องไม่ซ้ำกัน!")
            return

        self.current_round += 1
        
        # Logic
        bulls, cows, misses = self._calculate_score(guess)
        print(f"Score: B={bulls}, C={cows}, M={misses}") # Debug
        
        # Log result
        self._log_guess(guess, bulls, cows, misses)
        
        # Update Status Label
        self.status_label.config(text=f"ผลล่าสุด: {guess} -> ถูกตำแหน่ง: {bulls}, ถูกเลข: {cows}")

        # Check Win/Loss
        if bulls == 3:
            self._handle_win(guess)
        elif self.current_round >= self.max_rounds:
            self._handle_loss()
        else:
            self.update_round_label()
            self.entry_var.set("")
            self.entry.focus()

    def _calculate_score(self, guess):
        guess_list = list(guess)
        bulls = 0
        cows = 0
        
        # Count Bulls
        for i in range(3):
            if guess_list[i] == self.secret_number[i]:
                bulls += 1
        
        # Count Cows (correct number, wrong position)
        for digit in guess_list:
            if digit in self.secret_number:
                cows += 1
        
        cows -= bulls # Remove double counting
        misses = 3 - bulls - cows
        
        return bulls, cows, misses

    def _log_guess(self, guess, bulls, cows, misses):
        self.history_text.config(state='normal')
        result_text = f"[{self.current_round}] {guess} | B:{bulls} C:{cows} M:{misses}\n"
        self.history_text.insert(tk.END, result_text)
        self.history_text.see(tk.END)
        self.history_text.config(state='disabled')

    def _handle_win(self, guess):
        self.game_over = True
        messagebox.showinfo("Congratulations!", f"ยินดีด้วย! คุณทายถูก: {guess}\nในรอบที่ {self.current_round}")
        self._disable_input()

    def _handle_loss(self):
        self.game_over = True
        secret_str = "".join(self.secret_number)
        messagebox.showinfo("Game Over", f"เสียใจด้วย คุณใช้โควต้าหมดแล้ว\nเลขที่ถูกคือ: {secret_str}")
        self._disable_input()

    def _disable_input(self):
        self.entry.config(state='disabled')
        self.guess_btn.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    game = GuessTheBallGame(root)
    root.mainloop()
