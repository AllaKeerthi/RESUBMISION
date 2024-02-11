import csv
from statistics import mean, median
from datetime import datetime
from typing import List, Optional

class SingletonMeta(type):
    """Metaclass for creating a singleton class."""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class PlayerRecord:
    """Class representing an individual player's statistics."""
    def __init__(self, name: str, team: str, goals: int, assists: int):
        self.name = name
        self.team = team
        self.goals = goals
        self.assists = assists

    def edit(self, name: Optional[str] = None, team: Optional[str] = None,
             goals: Optional[int] = None, assists: Optional[int] = None):
        """Edit the fields of a PlayerRecord."""
        if name:
            self.name = name
        if team:
            self.team = team
        if goals is not None:
            self.goals = goals
        if assists is not None:
            self.assists = assists

    def display(self):
        print(f"Name: {self.name}, Team: {self.team}, Goals: {self.goals}, Assists: {self.assists}")

class PlayerManager(metaclass=SingletonMeta):
    """Singleton class for managing player records and performing calculations."""

    def __init__(self):
        """Initialize a PlayerManager object."""
        self.players = []

    def add_player(self, player: PlayerRecord):
        """Add a new player to the list."""
        self.players.append(player)
        print("Player added successfully.")

    def edit_player(self, index: int, updated_player: PlayerRecord):
        """Edit a player in the manager."""
        if 0 <= index < len(self.players):
            self.players[index].edit(
                name=updated_player.name,
                team=updated_player.team,
                goals=updated_player.goals,
                assists=updated_player.assists
            )
            print("Player updated successfully.")
        else:
            print("Invalid index.")

    def delete_player(self, index: int):
        """Delete a player from the manager."""
        if 0 <= index < len(self.players):
            del self.players[index]
            print("Player deleted successfully.")
        else:
            print("Invalid index.")

    def calculate_average_goals(self) -> float:
        """Calculate the average goals scored by players."""
        if self.players:
            return mean(player.goals for player in self.players)
        return 0.0

    def calculate_median_assists(self) -> float:
        """Calculate the median of assists."""
        if self.players:
            return median(player.assists for player in self.players)
        return 0.0

    def save_to_csv(self, filename: str):
        """Save player statistics to a CSV file."""
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['Name', 'Team', 'Goals', 'Assists']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for player in self.players:
                writer.writerow({
                    'Name': player.name,
                    'Team': player.team,
                    'Goals': player.goals,
                    'Assists': player.assists
                })

    def load_from_csv(self, filename: str):
        """Load player statistics from a CSV file."""
        self.players = []
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                player = PlayerRecord(
                    name=row['Name'],
                    team=row['Team'],
                    goals=int(row['Goals']),
                    assists=int(row['Assists'])
                )
                self.players.append(player)

    def filter_by_team(self, team: str) -> List[PlayerRecord]:
        """Filter players by team."""
        return [player for player in self.players if player.team == team]

    def filter_by_goal_range(self, min_goals: int, max_goals: int, ascending: bool = True) -> List[PlayerRecord]:
        """Filter players by goal range and order the result."""
        filtered_players = [player for player in self.players if min_goals <= player.goals <= max_goals]
        filtered_players.sort(key=lambda x: x.goals, reverse=not ascending)
        return filtered_players
class ConsoleApp:
    def __init__(self, player_manager):
        self.player_manager = player_manager

    def display_menu(self):
        print("-" * 90)
        print("\nMenu:")
        print("1. Add Player")
        print("2. Edit Player")
        print("3. Delete Player")
        print("4. Display All Players")
        print("5. Calculate Average Goals and Median Assists")
        print("6. Filter by Team")
        print("7. Filter by Goal Range")
        print("8. Save Players to CSV")
        print("9. Load Players from CSV")
        print("10. Exit")

    def run(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice: ")

            if choice == '1':
                self.add_player()
            elif choice == '2':
                self.edit_player()
            elif choice == '3':
                self.delete_player()
            elif choice == '4':
                self.display_all_players()
            elif choice == '5':
                self.calculate_average_goals_and_median_assists()
            elif choice == '6':
                self.filter_by_team()
            elif choice == '7':
                self.filter_by_goal_range()
            elif choice == '8':
                self.save_to_csv()
            elif choice == '9':
                self.load_from_csv()
            elif choice == '10':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")

    def add_player(self):
        """Add a player based on user input."""
        try:
            name = input("Enter player's name: ")
            team = input("Enter player's team: ")
            goals = int(input("Enter number of goals: "))
            assists = int(input("Enter number of assists: "))
            player = PlayerRecord(name, team, goals, assists)
            self.player_manager.add_player(player)
        except ValueError as e:
            print(f"Error: {e}. Please enter valid input.")

    def edit_player(self):
        index = int(input("Enter the index of the player to edit: "))
        if 0 <= index < len(self.player_manager.players):
            player = self.player_manager.players[index]
            print("\nCurrent Player Details:")
            player.display()

            print("\nEnter the updated details (leave blank to keep the existing value):")
            updated_name = input(f"Updated name ({player.name}): ") or player.name
            updated_team = input(f"Updated team ({player.team}): ") or player.team
            updated_goals = input(f"Updated goals ({player.goals}): ")
            updated_assists = input(f"Updated assists ({player.assists}): ")

            updated_goals = int(updated_goals) if updated_goals else player.goals
            updated_assists = int(updated_assists) if updated_assists else player.assists

            updated_player = PlayerRecord(updated_name, updated_team, updated_goals, updated_assists)
            self.player_manager.edit_player(index, updated_player)
            print("Player updated successfully.")
        else:
            print("Invalid index.")

    def delete_player(self):
        index = int(input("Enter the index of the player to delete: "))
        if 0 <= index < len(self.player_manager.players):
            self.player_manager.delete_player(index)
            print("Player deleted successfully.")
        else:
            print("Invalid index.")

    def display_all_players(self):
        if not self.player_manager.players:
            print("No players to display.")
        else:
            print("\nAll Players:")
            print("{:<5} {:<20} {:<15} {:<10} {:<10}".format("Index", "Name", "Team", "Goals", "Assists"))
            print("-" * 90)
            for index, player in enumerate(self.player_manager.players):
                print("{:<5} {:<20} {:<15} {:<10} {:<10}".format(index, player.name, player.team, player.goals, player.assists))

    def calculate_average_goals_and_median_assists(self):
        average_goals = self.player_manager.calculate_average_goals()
        median_assists = self.player_manager.calculate_median_assists()
        print(f"Average Goals: {average_goals}")
        print(f"Median Assists: {median_assists}")

    def filter_by_team(self):
        team = input("Enter team to filter by: ")
        filtered_players = self.player_manager.filter_by_team(team)
        if filtered_players:
            print("\nFiltered Players:")
            for player in filtered_players:
                player.display()
        else:
            print(f"No players found for team: {team}")

    def filter_by_goal_range(self):
        min_goals = int(input("Enter minimum goals: "))
        max_goals = int(input("Enter maximum goals: "))
        filtered_players = self.player_manager.filter_by_goal_range(min_goals, max_goals)
        if filtered_players:
            print("\nFiltered Players:")
            for player in filtered_players:
                player.display()
        else:
            print("No players found in the specified goal range.")

    def save_to_csv(self):
        filename = input("Enter the filename to save players (e.g., players.csv): ")
        self.player_manager.save_to_csv(filename)
        print(f"Players saved to {filename}.")

    def load_from_csv(self):
        filename = input("Enter the filename to load players from (e.g., players.csv): ")
        self.player_manager.load_from_csv(filename)
        print(f"Players loaded from {filename}.")

if __name__ == "__main__":
    manager = PlayerManager()
    console_app = ConsoleApp(manager)
    console_app.run()
