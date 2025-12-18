import tkinter as tk
from tkinter import ttk, messagebox
import random
import sys

class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        
        self.root.minsize(500, 700)
        
        self.board = [""] * 9
        self.player = "X"
        self.ai = "O"
        self.current_turn = "X"
        self.game_active = True

        self.player_score = 0
        self.ai_score = 0
        self.draws = 0

        self.difficulty = tk.StringVar(value="Expert")

        self.colors = {
            "bg": "#0f0c29",
            "card": "#24243e",
            "button": "#302b63",
            "button_hover": "#3a3573",
            "text": "#f8fafc",
            "x": "#00dbde",
            "o": "#fc00ff",
            "win": "#00ff88",
            "accent": "#6366f1",
            "refresh": "#f59e0b",
            "stats": "#10b981",
            "exit": "#ef4444"
        }

        self.title_font_size = 28
        self.board_font_size = 40
        self.button_font_size = 11
        self.stats_font_size = 14
        self.status_font_size = 14
        
        self.setup_style()
        self.create_ui()
        
        self.center_window()
        
        self.root.bind("<Configure>", self.on_window_resize)

    def center_window(self):
        self.root.update_idletasks()
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        window_width = min(int(screen_width * 0.8), 900)
        window_height = min(int(screen_height * 0.85), 1100)
        
        self.root.geometry(f"{window_width}x{window_height}")
        
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        self.window_width = window_width
        self.window_height = window_height
        self.original_width = window_width
        self.original_height = window_height

    def on_window_resize(self, event):
        if event.widget == self.root:
            self.window_width = event.width
            self.window_height = event.height
            
            self.update_font_sizes()
            self.update_board_button_sizes()
            self.update_layout()

    def update_font_sizes(self):
        if not hasattr(self, 'title_label'):
            return
            
        width_scale = self.window_width / self.original_width
        height_scale = self.window_height / self.original_height
        scale_factor = min(width_scale, height_scale, 1.5)
        
        self.title_font_size = max(20, int(28 * scale_factor * 0.8))
        self.board_font_size = max(24, int(40 * scale_factor * 0.7))
        self.button_font_size = max(9, int(11 * scale_factor * 0.9))
        self.stats_font_size = max(10, int(14 * scale_factor * 0.8))
        self.status_font_size = max(12, int(14 * scale_factor))
        
        try:
            self.title_label.config(font=("Segoe UI Black", self.title_font_size))
            self.score_label.config(font=("Segoe UI Semibold", self.stats_font_size))
            self.status_label.config(font=("Segoe UI", self.status_font_size, "bold"))
            
            for btn in self.buttons:
                btn.config(font=("Segoe UI Black", self.board_font_size))
            
            for child in self.action_frame.winfo_children():
                if isinstance(child, tk.Button):
                    child.config(font=("Segoe UI", self.button_font_size, "bold"))
            
            self.subtitle.config(font=("Segoe UI", max(10, self.button_font_size - 1)))
            self.footer.config(font=("Segoe UI", max(9, self.button_font_size - 2)))
            
            for child in self.diff_frame.winfo_children():
                if isinstance(child, tk.Label):
                    child.config(font=("Segoe UI", self.button_font_size))
            
            self.diff_combo.config(font=("Segoe UI", self.button_font_size - 1))
        except:
            pass

    def update_board_button_sizes(self):
        if not hasattr(self, 'buttons'):
            return
            
        board_size = min(self.window_width * 0.6, self.window_height * 0.35)
        btn_width = max(2, int(board_size // 30))
        btn_height = max(1, int(board_size // 60))
        
        for btn in self.buttons:
            btn.config(width=btn_width, height=btn_height)

    def update_layout(self):
        try:
            pad_y = max(10, int(self.window_height * 0.02))
            self.header_frame.pack_configure(pady=(pad_y, pad_y//2))
            
            pad_x = max(20, int(self.window_width * 0.05))
            pad_y = max(5, int(self.window_height * 0.01))
            self.stats_card.pack_configure(padx=pad_x, pady=pad_y)
            
            pad_y = max(10, int(self.window_height * 0.02))
            self.board_container.pack_configure(pady=pad_y)
            
            pad_y = max(10, int(self.window_height * 0.02))
            self.action_frame.pack_configure(pady=pad_y)
            
            pad_y = max(10, int(self.window_height * 0.015))
            self.footer.pack_configure(pady=pad_y)
        except:
            pass

    def setup_style(self):
        self.root.configure(bg=self.colors["bg"])
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "TButton",
            font=("Segoe UI", self.button_font_size, "bold"),
            padding=10,
            relief="flat",
            borderwidth=0
        )

        style.configure(
            "TLabel",
            background=self.colors["bg"],
            foreground=self.colors["text"],
            font=("Segoe UI", self.button_font_size)
        )

    def create_ui(self):
        self.root.pack_propagate(False)
        
        main_container = tk.Frame(self.root, bg=self.colors["bg"])
        main_container.pack(fill="both", expand=True, padx=10, pady=10)

        self.header_frame = tk.Frame(main_container, bg=self.colors["bg"])
        self.header_frame.pack(fill="x", pady=(10, 5))

        title_frame = tk.Frame(self.header_frame, bg=self.colors["bg"])
        title_frame.pack()

        self.title_label = tk.Label(
            title_frame,
            text="TIC-TAC-TOE",
            font=("Segoe UI Black", self.title_font_size),
            fg=self.colors["x"],
            bg=self.colors["bg"]
        )
        self.title_label.pack(side=tk.LEFT)

        tk.Label(
            title_frame,
            text="⚡",
            font=("Segoe UI", self.title_font_size),
            fg=self.colors["o"],
            bg=self.colors["bg"]
        ).pack(side=tk.LEFT, padx=5)

        self.subtitle = tk.Label(
            self.header_frame,
            text="AI Powered Strategy Game",
            font=("Segoe UI", max(10, self.button_font_size - 1)),
            fg="#94a3b8",
            bg=self.colors["bg"]
        )
        self.subtitle.pack(pady=(5, 10))

        self.stats_card = tk.Frame(
            main_container,
            bg=self.colors["card"],
            relief="ridge",
            bd=1,
            highlightbackground="#4f46e5",
            highlightthickness=2
        )
        self.stats_card.pack(fill="x", padx=20, pady=5)

        self.score_label = tk.Label(
            self.stats_card,
            text=self.get_score_text(),
            font=("Segoe UI Semibold", self.stats_font_size),
            bg=self.colors["card"],
            fg=self.colors["text"],
            padx=20,
            pady=10
        )
        self.score_label.pack()

        control_panel = tk.Frame(main_container, bg=self.colors["bg"])
        control_panel.pack(fill="x", pady=10)

        self.diff_frame = tk.Frame(control_panel, bg=self.colors["bg"])
        self.diff_frame.pack(side=tk.LEFT, padx=(20, 10))

        tk.Label(
            self.diff_frame,
            text="🛡️ AI Difficulty:",
            font=("Segoe UI", self.button_font_size),
            fg="#cbd5e1",
            bg=self.colors["bg"]
        ).pack(side=tk.LEFT, padx=(0, 5))

        self.diff_combo = ttk.Combobox(
            self.diff_frame,
            values=["Easy", "Medium", "Hard", "Expert"],
            textvariable=self.difficulty,
            state="readonly",
            width=12,
            font=("Segoe UI", self.button_font_size - 1)
        )
        self.diff_combo.pack(side=tk.LEFT)
        self.diff_combo.bind("<<ComboboxSelected>>", lambda e: self.reset_game())

        self.status_indicator = tk.Frame(
            control_panel,
            bg=self.colors["x"],
            height=8,
            width=120
        )
        self.status_indicator.pack(side=tk.LEFT, padx=20)

        self.status_label = tk.Label(
            control_panel,
            text="🎮 Your Turn (X)",
            font=("Segoe UI", self.status_font_size, "bold"),
            fg=self.colors["x"],
            bg=self.colors["bg"]
        )
        self.status_label.pack(side=tk.LEFT)

        self.board_container = tk.Frame(
            main_container,
            bg=self.colors["accent"],
            padx=2,
            pady=2
        )
        self.board_container.pack(pady=10, expand=True)

        board_frame = tk.Frame(
            self.board_container,
            bg=self.colors["card"]
        )
        board_frame.pack(expand=True)

        self.buttons = []
        btn_width = 3
        btn_height = 1
        
        for i in range(9):
            btn = tk.Button(
                board_frame,
                text="",
                font=("Segoe UI Black", self.board_font_size),
                width=btn_width,
                height=btn_height,
                bg=self.colors["button"],
                fg=self.colors["text"],
                activebackground=self.colors["button_hover"],
                relief="flat",
                cursor="hand2",
                command=lambda i=i: self.player_move(i)
            )
            btn.grid(row=i//3, column=i%3, padx=3, pady=3, sticky="nsew")
            
            board_frame.grid_rowconfigure(i//3, weight=1)
            board_frame.grid_columnconfigure(i%3, weight=1)
            
            btn.bind("<Enter>", lambda e, b=btn: self.on_button_hover(b, True))
            btn.bind("<Leave>", lambda e, b=btn: self.on_button_hover(b, False))
            
            self.buttons.append(btn)

        self.action_frame = tk.Frame(main_container, bg=self.colors["bg"])
        self.action_frame.pack(fill="x", pady=15)

        action_buttons = [
            ("🔄 Next Round", self.colors["accent"], self.start_next_round),
            ("🆕 New Game", "#8B5CF6", self.new_game_with_confirmation),
            ("📊 Statistics", self.colors["stats"], self.show_stats),
            ("🚪 Exit", self.colors["exit"], self.exit_game)
        ]
        
        for idx, (text, color, command) in enumerate(action_buttons):
            btn = tk.Button(
                self.action_frame,
                text=text,
                font=("Segoe UI", self.button_font_size, "bold"),
                bg=color,
                fg="white",
                activebackground=color,
                activeforeground="white",
                relief="flat",
                padx=10,
                pady=8,
                cursor="hand2",
                command=command
            )
            
            btn.bind("<Enter>", lambda e, b=btn, c=color: b.config(bg=self.lighten_color(c)))
            btn.bind("<Leave>", lambda e, b=btn, c=color: b.config(bg=c))
            
            btn.grid(row=0, column=idx, padx=5, pady=5, sticky="ew")
            self.action_frame.grid_columnconfigure(idx, weight=1)

        self.footer = tk.Label(
            main_container,
            text="Made with ❤️ | AI Internship Project",
            font=("Segoe UI", max(9, self.button_font_size - 2)),
            fg="#64748b",
            bg=self.colors["bg"]
        )
        self.footer.pack(side="bottom", pady=10)

    def on_button_hover(self, button, enter):
        if enter and button["text"] == "" and self.game_active:
            button.config(bg=self.colors["button_hover"])
        elif button["text"] == "":
            button.config(bg=self.colors["button"])

    def lighten_color(self, color):
        if color.startswith("#"):
            rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
            light_rgb = tuple(min(255, c + 30) for c in rgb)
            return f"#{light_rgb[0]:02x}{light_rgb[1]:02x}{light_rgb[2]:02x}"
        return color

    def player_move(self, index):
        if not self.game_active or self.board[index] != "" or self.current_turn != self.player:
            return

        self.make_move(index, self.player)

        if self.check_game_end():
            self.root.after(1000, self.offer_next_round)
            return

        self.current_turn = self.ai
        self.update_status_indicator(self.ai)
        self.status_label.config(text="🤖 AI Thinking...", fg=self.colors["o"])
        self.root.after(600, self.ai_move)

    def ai_move(self):
        move = self.get_ai_move()
        self.make_move(move, self.ai)

        if self.check_game_end():
            self.root.after(1000, self.offer_next_round)
            return

        self.current_turn = self.player
        self.update_status_indicator(self.player)
        self.status_label.config(text="🎮 Your Turn (X)", fg=self.colors["x"])

    def make_move(self, index, symbol):
        self.board[index] = symbol
        self.buttons[index].config(
            text=symbol,
            fg=self.colors["x"] if symbol == "X" else self.colors["o"],
            bg=self.colors["button"]
        )

    def offer_next_round(self):
        if messagebox.askyesno("Play Again?", "Do you want to play another round?\n\nScores will be kept."):
            self.start_next_round()
        else:
            self.show_stats()

    def start_next_round(self):
        self.reset_game()
        self.status_label.config(text="🎮 Your Turn (X)", fg=self.colors["x"])
        
        notification = tk.Label(
            self.root,
            text="Round Started!",
            font=("Segoe UI", 10, "bold"),
            bg="#10B981",
            fg="white",
            padx=10,
            pady=5
        )
        notification.place(relx=0.5, rely=0.92, anchor="center")
        
        self.root.after(1000, notification.destroy)

    def new_game_with_confirmation(self):
        if messagebox.askyesno("New Game", "Are you sure you want to start a new game?\nThis will reset all scores to zero."):
            self.reset_all_scores()
            self.reset_game()
            self.status_label.config(text="🎮 New Game Started!", fg=self.colors["x"])
            self.root.after(1500, lambda: self.status_label.config(
                text="🎮 Your Turn (X)", 
                fg=self.colors["x"]
            ))

    def reset_all_scores(self):
        self.player_score = 0
        self.ai_score = 0
        self.draws = 0
        self.update_score()

    def update_status_indicator(self, turn):
        color = self.colors["x"] if turn == "X" else self.colors["o"]
        self.status_indicator.config(bg=color)

    def get_ai_move(self):
        empty = [i for i in range(9) if self.board[i] == ""]

        if self.difficulty.get() == "Easy":
            return random.choice(empty)

        if self.difficulty.get() in ["Medium", "Hard"]:
            for i in empty:
                self.board[i] = self.ai
                if self.check_winner() == self.ai:
                    self.board[i] = ""
                    return i
                self.board[i] = ""
            
            for i in empty:
                self.board[i] = self.player
                if self.check_winner() == self.player:
                    self.board[i] = ""
                    return i
                self.board[i] = ""
            
            if self.difficulty.get() == "Hard" and len(empty) > 0:
                preferred = [4, 0, 2, 6, 8, 1, 3, 5, 7]
                for pos in preferred:
                    if pos in empty:
                        return pos
            
            return random.choice(empty)

        return self.minimax_best_move()

    def minimax_best_move(self):
        best_score = -float('inf')
        best_move = None

        for i in range(9):
            if self.board[i] == "":
                self.board[i] = self.ai
                score = self.minimax(0, False)
                self.board[i] = ""
                if score > best_score:
                    best_score = score
                    best_move = i
        return best_move if best_move is not None else random.choice([i for i in range(9) if self.board[i] == ""])

    def minimax(self, depth, is_maximizing):
        winner = self.check_winner()
        if winner == self.ai:
            return 10 - depth
        if winner == self.player:
            return depth - 10
        if "" not in self.board:
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for i in range(9):
                if self.board[i] == "":
                    self.board[i] = self.ai
                    score = self.minimax(depth + 1, False)
                    self.board[i] = ""
                    best_score = max(best_score, score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if self.board[i] == "":
                    self.board[i] = self.player
                    score = self.minimax(depth + 1, True)
                    self.board[i] = ""
                    best_score = min(best_score, score)
            return best_score

    def check_winner(self):
        combos = [
            (0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)
        ]
        for a,b,c in combos:
            if self.board[a] == self.board[b] == self.board[c] != "":
                return self.board[a]
        return None

    def check_game_end(self):
        winner = self.check_winner()
        if winner:
            self.game_active = False
            combos = [
                (0,1,2),(3,4,5),(6,7,8),
                (0,3,6),(1,4,7),(2,5,8),
                (0,4,8),(2,4,6)
            ]
            for a,b,c in combos:
                if self.board[a] == self.board[b] == self.board[c] != "":
                    for i in (a,b,c):
                        self.buttons[i].config(
                            bg=self.colors["win"],
                            relief="ridge",
                            bd=3
                        )
            
            if winner == self.player:
                self.player_score += 1
            else:
                self.ai_score += 1
            self.update_score()
            return True

        if "" not in self.board:
            self.game_active = False
            self.draws += 1
            self.update_score()
            return True
        return False

    def reset_game(self):
        self.board = [""] * 9
        self.game_active = True
        self.current_turn = "X"
        self.update_status_indicator("X")
        for btn in self.buttons:
            btn.config(
                text="", 
                bg=self.colors["button"],
                relief="flat",
                bd=0
            )

    def update_score(self):
        self.score_label.config(text=self.get_score_text())

    def get_score_text(self):
        total = self.player_score + self.ai_score + self.draws
        win_rate = (self.player_score / total * 100) if total > 0 else 0
        return f"👤 Player: {self.player_score}  |  🤖 AI: {self.ai_score}  |  🤝 Draws: {self.draws}  |  📈 Win Rate: {win_rate:.1f}%"

    def show_stats(self):
        total = self.player_score + self.ai_score + self.draws
        player_rate = (self.player_score / total * 100) if total > 0 else 0
        ai_rate = (self.ai_score / total * 100) if total > 0 else 0
        draw_rate = (self.draws / total * 100) if total > 0 else 0
        
        message = f"""🏆 Total Games: {total}
🎯 Player Wins: {self.player_score} ({player_rate:.1f}%)
🤖 AI Wins: {self.ai_score} ({ai_rate:.1f}%)
🤝 Draws: {self.draws} ({draw_rate:.1f}%)

🛡️ Current Difficulty: {self.difficulty.get()}
🎮 Current Turn: {self.current_turn}

{'🔥 Hot Streak!' if self.player_score > self.ai_score else 
 '💡 Keep Trying!' if self.player_score == self.ai_score else 
 '🤖 AI Dominating!'}"""
        
        response = messagebox.askyesno(
            "📊 Game Statistics", 
            message + "\n\nDo you want to play another round?"
        )
        
        if response:
            self.start_next_round()

    def exit_game(self):
        if messagebox.askyesno("Exit Game", "Are you sure you want to exit?\n\nYour current scores will be lost."):
            self.root.destroy()
            sys.exit()

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()