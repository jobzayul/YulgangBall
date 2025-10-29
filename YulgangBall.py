import random
import tkinter as tk
from tkinter import messagebox

class GuessTheBallGame:
    """
    คลาสหลักสำหรับจัดการตรรกะของเกมและ GUI
    """
    def __init__(self, master):
        self.master = master
        master.title("✨ เกมทายลูกบอล 3 หลัก (Bulls and Cows) ✨")
        master.config(padx=20, pady=20)
        
        # กำหนดค่าเริ่มต้นของเกม
        self.max_rounds = 7
        self.current_round = 0
        self.secret_number = self._generate_secret_number()
        
        # สร้างส่วนประกอบของ GUI
        self._create_widgets()
        
        self.log_message(f"🎯 กติกา: ทายเลข 3 หลักที่ไม่ซ้ำกัน (0-9) คุณมี {self.max_rounds} รอบ")

    def _generate_secret_number(self):
        """สุ่มสร้างเลข 3 หลักที่ไม่ซ้ำกัน (0-9) คืนค่าเป็น list ของตัวอักษร"""
        return random.sample("0123456789", 3)
    
    def _create_widgets(self):
        """สร้างและจัดวางองค์ประกอบ GUI ทั้งหมด"""
        
        # 1. ส่วนการป้อนข้อมูล (Input Frame)
        input_frame = tk.Frame(self.master)
        input_frame.grid(row=0, column=0, pady=10)
        
        tk.Label(input_frame, text="ทายเลข 3 หลัก:", font=('Arial', 12)).pack(side=tk.LEFT, padx=5)
        
        self.guess_entry = tk.Entry(input_frame, width=10, font=('Arial', 14))
        self.guess_entry.pack(side=tk.LEFT, padx=5)
        self.guess_entry.bind('<Return>', lambda event=None: self.check_guess_action()) # ให้กด Enter ได้
        
        self.guess_button = tk.Button(input_frame, text="ทาย!", font=('Arial', 12, 'bold'), command=self.check_guess_action)
        self.guess_button.pack(side=tk.LEFT, padx=5)

        # 2. ส่วนแสดงผลรอบปัจจุบัน
        self.round_label = tk.Label(self.master, text=f"รอบที่ 0 / {self.max_rounds}", font=('Arial', 14, 'bold'), fg='blue')
        self.round_label.grid(row=1, column=0, pady=5)
        self.update_round_label()

        # 3. ส่วนแสดงผลลัพธ์ / ประวัติ (Log)
        tk.Label(self.master, text="ประวัติการทาย:", font=('Arial', 12, 'underline')).grid(row=2, column=0, sticky='w', pady=5)
        
        self.log_text = tk.Text(self.master, height=10, width=40, font=('Courier', 10), state=tk.DISABLED)
        self.log_text.grid(row=3, column=0, pady=10)
        
        # 4. ปุ่มเริ่มเกมใหม่
        self.new_game_button = tk.Button(self.master, text="เริ่มเกมใหม่ 🔄", font=('Arial', 12), command=self.reset_game)
        self.new_game_button.grid(row=4, column=0, pady=10)
        
    def log_message(self, message, tag=None):
        """เพิ่มข้อความในส่วนแสดงประวัติ"""
        self.log_text.config(state=tk.NORMAL) # เปิดให้แก้ไขได้
        self.log_text.insert(tk.END, message + "\n", tag)
        self.log_text.config(state=tk.DISABLED) # ปิดการแก้ไข
        self.log_text.see(tk.END) # เลื่อนไปที่บรรทัดสุดท้าย

    def update_round_label(self):
        """อัปเดตข้อความแสดงรอบปัจจุบัน"""
        self.round_label.config(text=f"รอบที่ {self.current_round} / {self.max_rounds}")

    def reset_game(self):
        """ตั้งค่าเกมใหม่ทั้งหมด"""
        self.current_round = 0
        self.secret_number = self._generate_secret_number()
        
        # ล้างประวัติ
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        
        self.guess_entry.delete(0, tk.END)
        self.guess_entry.config(state=tk.NORMAL)
        self.guess_button.config(state=tk.NORMAL)
        self.update_round_label()
        self.log_message("--- เริ่มเกมใหม่ ---")
        self.log_message(f"🎯 กติกา: ทายเลข 3 หลักที่ไม่ซ้ำกัน (0-9) คุณมี {self.max_rounds} รอบ")
        # print(f"*** คำตอบใหม่: {''.join(self.secret_number)} ***") # ดีบัก

    def check_guess_action(self):
        """ฟังก์ชันที่เรียกใช้เมื่อผู้เล่นกดปุ่ม 'ทาย!'"""
        if self.current_round >= self.max_rounds:
            messagebox.showinfo("จบเกม", "คุณทายครบ 7 รอบแล้ว! กรุณากด 'เริ่มเกมใหม่'")
            return
            
        guess = self.guess_entry.get().strip()
        self.guess_entry.delete(0, tk.END) # ล้างช่องป้อนข้อมูล

        # ตรวจสอบความถูกต้องของการทาย (Validation)
        if len(guess) != 3 or not guess.isdigit():
            messagebox.showerror("ข้อผิดพลาด", "กรุณาใส่ตัวเลข 3 หลักเท่านั้น!")
            return
            
        if len(set(guess)) < 3:
            messagebox.showwarning("คำเตือน", "เลขที่ทายควรเป็นเลข 3 หลักที่ไม่ซ้ำกัน!")
            # สามารถเปลี่ยนเป็น return เพื่อบังคับให้ทายใหม่ได้ แต่ตามโค้ดเดิมอนุญาตให้เล่นต่อ

        self.current_round += 1
        self.update_round_label()
        
        bulls, cows, misses = self._get_result(self.secret_number, guess)
        
        # แสดงผลลัพธ์ใน Log
        log_entry = f"[{self.current_round}] ทาย: {guess} | Bulls: {bulls}, Cows: {cows}, Misses: {misses}"
        self.log_message(log_entry)
        
        # ตรวจสอบชัยชนะ
        if bulls == 3:
            self.log_message(f"🎉 ยอดเยี่ยม! คุณทายถูกคือ {''.join(self.secret_number)}!", "win")
            messagebox.showinfo("ชนะ!", f"คุณทายถูกคือ {''.join(self.secret_number)} ในรอบที่ {self.current_round}!")
            self._end_game()
            return
            
        # ตรวจสอบแพ้
        if self.current_round >= self.max_rounds:
            self.log_message(f"😥 เกมจบแล้ว! เลขลับคือ: {''.join(self.secret_number)}", "lose")
            messagebox.showinfo("แพ้", f"คุณทายไม่ถูกใน {self.max_rounds} รอบ\nเลขลับคือ: {''.join(self.secret_number)}")
            self._end_game()
            
    def _get_result(self, secret: list, guess: str) -> tuple[int, int, int]:
        """
        คำนวณผลลัพธ์ (Bulls, Cows, Misses)
        (นำตรรกะมาจากฟังก์ชัน check_guess เดิม)
        """
        guess_list = list(guess)
        
        bulls = 0  
        correct_number_total = 0

        # 1. นับ Bulls (ถูกตำแหน่ง)
        for i in range(3):
            if guess_list[i] == secret[i]:
                bulls += 1

        # 2. นับตัวเลขที่ถูกทั้งหมด
        for digit in guess_list:
            if digit in secret:
                correct_number_total += 1
                
        cows = correct_number_total - bulls 
        misses = 3 - bulls - cows          

        return bulls, cows, misses
        
    def _end_game(self):
        """ล็อคการป้อนข้อมูลเมื่อเกมจบ"""
        self.guess_entry.config(state=tk.DISABLED)
        self.guess_button.config(state=tk.DISABLED)

# รันเกม
if __name__ == "__main__":
    root = tk.Tk()
    game = GuessTheBallGame(root)
    root.mainloop()
