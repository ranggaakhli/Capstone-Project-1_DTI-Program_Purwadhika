from tabulate import tabulate
import getpass

# Initialize admin username and password
admin_password = "123456"
admin_username = "rangga"
password_attempts = 0

def initialize_league(clubs):
    return [{'Club': club.title(), 
             'Points': 0, 
             'Matches Played': 0, 
             'Wins': 0, 
             'Losses': 0, 
             'Draws': 0, 
             'Goal For': 0, 
             'Goal Against': 0} 
            for club in clubs]

def add_club(clubs, club_name):
    club_name = club_name.title()
    if any(club['Club'] == club_name for club in clubs):
        print(f"Club '{club_name}' already exists. Please enter a different club.")
    else:
        clubs.append({'Club': club_name, 
                      'Points': 0, 
                      'Matches Played': 0, 
                      'Wins': 0, 
                      'Losses': 0, 
                      'Draws': 0, 
                      'Goal For': 0, 
                      'Goal Against': 0})

def add_match(clubs, match_results, home_team, away_team, home_score, away_score):
    home_team = home_team.title()
    away_team = away_team.title()
    home_club = next((club for club in clubs if club['Club'] == home_team), None)
    away_club = next((club for club in clubs if club['Club'] == away_team), None)
    
    if home_club is None:
        print(f"Club '{home_team} is not in the League. Please add the club first.")
        return
    if away_club is None:
        print(f" Club {away_team} is not in the league. Please add the club first")
        return
    
    home_club['Matches Played'] += 1
    away_club['Matches Played'] += 1
    home_club['Goal For'] += home_score
    away_club['Goal For'] += away_score
    home_club['Goal Against'] += away_score
    away_club['Goal Against'] += home_score
    
    if home_score > away_score:
        home_club['Points'] += 3
        home_club['Wins'] += 1
        away_club['Losses'] += 1
    elif home_score < away_score:
        away_club['Points'] += 3
        away_club['Wins'] += 1
        home_club['Losses'] += 1
    else:
        home_club['Points'] += 1
        away_club['Points'] += 1
        home_club['Draws'] += 1
        away_club['Draws'] += 1
    
    match_results.append((home_team, away_team, home_score, away_score))

def update_club(clubs, club_name, new_name):
    club_name = club_name.title()
    new_name = new_name.title()
    if not new_name:
        print("Error: New club name cannot be empty.")
        return
    club = next((club for club in clubs if club['Club'] == club_name), None)
    if club is None:
        print(f"Club '{club_name}' is not in the league")
        return
    if any(c['Club']==new_name for c in clubs if c['Club'] != club_name):
        print(f"Club name '{new_name}' already exists. Please choose a different name")
        return
    club['Club'] = new_name
    print(f"Club '{club_name}' updated to '{new_name}'.")

def delete_club(clubs, club_name):
    club_name = club_name.title()
    club = next((club for club in clubs if club['Club'] == club_name), None)
    if club is None:
        print(f"Club '{club}' is not in the league.")
        return
    clubs.remove(club)
    print(f"Club '{club_name}' deleted successfully.")

def display_table(clubs):
    headers = ["No", "Club", "Points", "Matches Played", "Wins", "Losses", "Draws", "Goal For", "Goal Against", "Goal Difference"]
    table = []
    for i, club in enumerate(sorted(clubs, key=lambda x: (x['Points'], x['Goal For'] - x['Goal Against']), reverse=True), start=1):
        goal_difference = club['Goal For'] - club['Goal Against']
        row = [i, club['Club'], club['Points'], club['Matches Played'], club['Wins'], club['Losses'], club['Draws'], club['Goal For'], club['Goal Against'], goal_difference]
        table.append(row)
    print("\nGROUP STAGE \nAFC U23 ASIAN CUP 2024\nGroup A")
    print(tabulate(table, headers=headers, tablefmt="grid"))

def display_match_results(match_results):
    print("\nGROUP STAGE \nAFC U23 ASIAN CUP 2024\nGroup A")
    print("\nMatch Results: ")
    for i, match in enumerate(match_results, start=1):
        home_team, away_team, home_score, away_score = match
        print(f"{i}. {home_team} {home_score} - {away_score} {away_team}")

def record_match(clubs, match_results):
    home_team = input("Enter home team: ")
    away_team = input("Enter away team: ")
    
    if home_team.title() == away_team.title():
        print("Error: Cannot have the same teams playing against each other.")
        return
    
    if not any(club['Club'] == home_team.title() for club in clubs):
        print(f"Club '{home_team}' is not in the league. Please add the club first.")
        return
    
    if not any(club['Club'] == away_team.title() for club in clubs):
        print(f"Club '{away_team}' is not in the league. Please add the club first.")
        return

    home_score = input("Enter home team score: ")
    away_score = input("Enter away team score: ")
    
    if not home_score.isdigit() or not away_score.isdigit():
        print("Error: Scores must be integers.")
        return

    home_score = int(home_score)
    away_score = int(away_score)

    if home_score < 0 or away_score < 0:
        print("Error: Scores cannot be negative.")
        return

    add_match(clubs, match_results, home_team, away_team, home_score, away_score)


def main():
    global password_attempts
    while password_attempts < 3:
        admin_username_input = input("Enter admin username: ")
        admin_password_input = getpass.getpass("Enter password: ")

        if admin_username_input != admin_username or admin_password_input != admin_password:
            password_attempts += 1
            print(f"Invalid admin credentials. Access denied. Attempt {password_attempts}/3")
        else:
            password_attempts = 0
            break

    if password_attempts == 3:
        print("Maximum attempts reached. Exiting...")
        return

    clubs = initialize_league(['Indonesia', 'Qatar', 'Jordan', 'Australia'])
    match_results = []
    display_table(clubs)
    
    while True:
        print("\nMenu:")
        print("1. Add Club")
        print("2. Add Match Result")
        print("3. Update Club")
        print("4. Delete Club")
        print("5. Display Match Results")
        print("6. Exit")
        
        choice = input('Enter your choice: ')
        
        if choice == "1":
            club_name = input('Enter club name: ')
            if not club_name.strip():
                print('Club cannot be empty. No club added')
            else:
                add_club(clubs, club_name)
        elif choice == '2':
            record_match(clubs, match_results)
        elif choice == '3':
            club_name = input("Enter club name to update:  ")
            new_name = input(f"Enter new name for '{club_name}': ")
            update_club(clubs, club_name, new_name)
        elif choice == '4':
            club_name = input("Enter club name to delete: ")
            delete_club(clubs, club_name)
        elif choice == '5':
            display_match_results(match_results)
        elif choice == '6':
            print("Exiting ... ")
            break
        else:
            print("Invalid choice. Please enter a valid option.")
        
        display_table(clubs)

main()
