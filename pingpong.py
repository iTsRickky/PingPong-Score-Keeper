import tkinter as tk
from tkinter import messagebox
import json

class BeginScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Ping Pong Score Keeper")

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Welcome to Ping Pong Score Keeper", font=("Helvetica", 16)).pack(pady=20)

        start_button = tk.Button(self.root, text="Start Game", command=self.open_input_screen)
        start_button.pack(pady=10)

    def open_input_screen(self):
        self.root.destroy()
        input_screen = tk.Tk()
        input_screen.title("Player Input Screen")
        PlayerInputScreen(input_screen)
        input_screen.mainloop()

class PlayerInputScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Player Input Screen")

        self.player1_name_var = tk.StringVar()
        self.player2_name_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Enter Player 1 name:").pack(pady=10)
        tk.Entry(self.root, textvariable=self.player1_name_var).pack(pady=5)

        tk.Label(self.root, text="Enter Player 2 name:").pack(pady=10)
        tk.Entry(self.root, textvariable=self.player2_name_var).pack(pady=5)

        start_button = tk.Button(self.root, text="Start", command=self.open_game_screen)
        start_button.pack(pady=10)

    def open_game_screen(self):
        player1_name = self.player1_name_var.get()
        player2_name = self.player2_name_var.get()

        if not player1_name or not player2_name:
            messagebox.showwarning("Incomplete Information", "Please enter names for both players.")
            return

        self.root.destroy()
        game_screen = tk.Tk()
        game_screen.title("Game Screen")
        GameScreen(game_screen, player1_name, player2_name)
        game_screen.mainloop()

class GameScreen:
    def __init__(self, root, player1_name, player2_name):
        self.root = root
        self.root.title("Game Screen")

        self.profiles = self.load_profiles()

        self.player1_name = player1_name
        self.player2_name = player2_name

        self.player1_score_var = tk.IntVar()
        self.player2_score_var = tk.IntVar()

        self.create_widgets()

    def load_profiles(self):
        try:
            with open('profiles.json', 'r') as file:
                profiles = json.load(file)
        except FileNotFoundError:
            profiles = {}
        return profiles

    def save_profiles(self):
        with open('profiles.json', 'w') as file:
            json.dump(self.profiles, file, indent=4)

    def create_or_get_profile(self, player_name):
        if player_name not in self.profiles:
            self.profiles[player_name] = {'wins': 0, 'losses': 0}
        return self.profiles[player_name]

    def update_scores(self, player_profile, opponent_profile, winner):
        player_profile['games_played'] = player_profile.get('games_played', 0) + 1
        opponent_profile['games_played'] = opponent_profile.get('games_played', 0) + 1

        if winner == 'player':
            player_profile['wins'] += 1
            opponent_profile['losses'] += 1
        elif winner == 'opponent':
            player_profile['losses'] += 1
            opponent_profile['wins'] += 1

    def display_scores(self, player_profile, opponent_profile):
        message = (
            f"{self.player1_name}: Wins - {player_profile['wins']}, Losses - {player_profile['losses']}\n"
            f"{self.player2_name}: Wins - {opponent_profile['wins']}, Losses - {opponent_profile['losses']}"
        )
        messagebox.showinfo("Scores", message)

    def play_game(self):
        player_score = self.player1_score_var.get()
        opponent_score = self.player2_score_var.get()

        if player_score > opponent_score:
            winner = 'player'
        elif opponent_score > player_score:
            winner = 'opponent'
        else:
            messagebox.showinfo("Tie", "It's a tie! Enter scores again.")
            return

        player_profile = self.create_or_get_profile(self.player1_name)
        opponent_profile = self.create_or_get_profile(self.player2_name)

        self.update_scores(player_profile, opponent_profile, winner)
        self.display_scores(player_profile, opponent_profile)

        self.save_profiles()

    def create_widgets(self):
        tk.Label(self.root, text=f"{self.player1_name}:").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(self.root, text=f"{self.player2_name}:").grid(row=1, column=0, padx=10, pady=10)

        tk.Button(self.root, text="⬆", command=lambda: self.player1_score_var.set(self.player1_score_var.get() + 1)).grid(row=0, column=1, pady=10)
        tk.Entry(self.root, textvariable=self.player1_score_var).grid(row=0, column=2, padx=10, pady=10)
        tk.Button(self.root, text="⬇", command=lambda: self.player1_score_var.set(max(self.player1_score_var.get() - 1, 0))).grid(row=0, column=3, pady=10)

        tk.Button(self.root, text="⬆", command=lambda: self.player2_score_var.set(self.player2_score_var.get() + 1)).grid(row=1, column=1, pady=10)
        tk.Entry(self.root, textvariable=self.player2_score_var).grid(row=1, column=2, padx=10, pady=10)
        tk.Button(self.root, text="⬇", command=lambda: self.player2_score_var.set(max(self.player2_score_var.get() - 1, 0))).grid(row=1, column=3, pady=10)

        play_game_button = tk.Button(self.root, text="End Game", command=self.play_game)
        play_game_button.grid(row=2, column=0, columnspan=4, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    begin_screen = BeginScreen(root)
    root.mainloop()