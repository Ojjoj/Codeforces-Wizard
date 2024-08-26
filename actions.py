from helper_actions import *
import tqdm


def show_all_names():
    headers = ["Usernames"]
    usernames = []
    names = get_names()
    if isinstance(names, str):
        print_message(names)
        return headers, usernames
    usernames = [[username] for username in names]
    return headers, usernames


def search_names():
    query = get_input("Search for username")
    if query == -1:
        print_message("Note: Cancelled !")
        return

    headers = ["Usernames"]
    matched_usernames = []
    usernames = get_names()
    if isinstance(usernames, str):
        print_message(usernames)
        return headers, matched_usernames

    matched_usernames = search_algorithm(usernames, query)
    usernames = [[username] for username in matched_usernames]

    if not usernames:
        print_message(f"Error: Oops ! {query} was not found !")
    elif usernames[0][0] == query:
        print_message(f"Success: {query} is found !")
    else:
        print_message(f"Note: {query} was not found, did you mean :")
    return headers, usernames


def show_all_ratings(names: List[str] = None):
    headers = ["Username", "Rating", "Rank"]
    all_ratings = []
    usernames = names if names else get_names()

    if isinstance(usernames, str):
        print_message(usernames)
        return headers, all_ratings

    user_info = get_users_info(usernames)

    if isinstance(user_info, str):
        print_message(user_info)
        return headers, all_ratings

    for user in user_info:
        username = user.get('handle')
        rating = user.get('rating', 'N/A')
        rank = user.get('rank', 'N/A')
        user_rating_row = [username, rating, rank]
        all_ratings.append(user_rating_row)

    all_ratings.sort(key=lambda x: (x[1] if x[1] != 'N/A' else -1), reverse=True)

    return headers, all_ratings


def search_ratings():
    headers, usernames = search_names()
    matched_usernames = []
    if not usernames:
        return headers, matched_usernames

    matched_usernames = [username[0] for username in usernames]
    headers, ratings = show_all_ratings(matched_usernames)
    return headers, ratings


def show_all_solved_problems(names: List[str] = None):
    headers = ["Usernames", "Solved Problems"]
    all_solved_problems = []
    usernames = names if names else get_names()

    if isinstance(usernames, str):
        print_message(usernames)
        return headers, all_solved_problems

    progress_bar = tqdm.tqdm(total=len(usernames), desc="Loading solved problems ...")
    for username in usernames:
        user_solved_problems = get_user_solved_problems(username)
        if isinstance(user_solved_problems, str):
            print_message(user_solved_problems)
            continue
        user_solved_problems_row = [username, user_solved_problems]
        all_solved_problems.append(user_solved_problems_row)
        progress_bar.update(1)
    all_solved_problems.sort(key=lambda x: x[1], reverse=True)
    progress_bar.close()

    return headers, all_solved_problems


def search_solved_problems():
    headers, usernames = search_names()
    matched_usernames = []
    if not usernames:
        return headers, matched_usernames

    matched_usernames = [username[0] for username in usernames]
    headers, solved_problems = show_all_solved_problems(matched_usernames)
    return headers, solved_problems


def add_user(filename: str = '.usernames.csv'):
    username = get_input()
    if username == -1:
        print_message("Note: Cancelled !")
        return
    usernames = get_names()
    if isinstance(usernames, str):
        print_message(usernames)
        return
    if username in usernames:
        print_message(f"Error: Username {username} already exists.")
        return
    user_info = get_users_info([username])
    if isinstance(user_info, str):
        print_message(user_info)
        return

    usernames.append(username)
    with open(filename, 'w') as file:
        file.write(',\n'.join(usernames))
    print_message(f"Success: Username {username} has been added.")


def remove_user(filename: str = '.usernames.csv'):
    username = get_input()
    if username == -1:
        print_message("Note: Cancelled !")
        return
    usernames = get_names()
    if isinstance(usernames, str):
        print_message(usernames)
        return
    if username not in usernames:
        print_message(f"Error: Username {username} not found in the list.")
        return

    usernames.remove(username)
    with open(filename, 'w') as file:
        file.write(',\n'.join(usernames))
    print_message(f"Success: Username {username} has been removed.")

