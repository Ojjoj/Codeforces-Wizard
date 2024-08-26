import requests
from random import randint
import os
from typing import List
from rich import print


# helper functions

def api_request(api_url: str, params):
    try:
        response = requests.get(api_url, params=params)

        if response.status_code != 200:
            return f"Error: Failed to retrieve data from {api_url}. Status code: {response.status_code}"

        data = response.json()
        if data['status'] != 'OK':
            return f"Error: API response status not OK. Message: {data.get('comment', 'No additional information')}"

        return data['result']
    except Exception:
        return f"Error: Internet connection problem !"


def get_names(filename='.usernames.csv'):
    if not os.path.exists(filename):
        return "Error: Username file does not exist."
    with open(filename, 'r') as file:
        names = file.read().strip()
    if not names:
        return "Error: No usernames found in the file."
    usernames = [name.strip() for name in names.split(',')]
    return usernames


def get_users_info(usernames: List[str]):
    api_url = "https://codeforces.com/api/user.info"
    params = {"handles": ";".join(usernames)}
    return api_request(api_url, params)


def get_user_solved_problems(username: str):
    api_url = "https://codeforces.com/api/user.status"
    params = {"handle": username}
    result = api_request(api_url, params)

    if isinstance(result, str):
        return result

    submissions = result
    solved_problems = set()

    for submission in submissions:
        if submission['verdict'] == 'OK':
            problem = submission['problem']
            problem_id = f"{problem.get('contestId', randint(0, 10_000_000))}-{problem.get('index', '')}"
            solved_problems.add(problem_id)

    return len(solved_problems)


def search_algorithm(names: List[str], query: str, max_distance: int = 2) -> List[str]:
    if query in names:
        return [query]

    results = []

    prefix_matches = [name for name in names if name.lower().startswith(query.lower())]
    results.extend(prefix_matches)

    for name in names:
        if levenshtein(name, query) <= max_distance:
            if name not in results:
                results.append(name)

    return list(set(results))


def levenshtein(s1: str, s2: str) -> int:
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    # Fill the dp table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1

    return dp[m][n]


def get_input(prompt_string: str = "Enter a username"):
    prompt = f"{prompt_string} (0 - Exit): "
    text = input(prompt)
    if text == "0":
        return -1
    return text


def print_message(message: str):
    message_parts = message.split(":")
    message_type, message_text = message_parts[0].strip(), message_parts[1].strip()
    print()
    if message_type == "Error":
        print_error(message_text)
    elif message_type == "Note":
        print_note(message_text)
    elif message_type == "Success":
        print_success(message_text)
    print()


def print_error(message: str):
    print(f"[red]{'-' * (len(message) + 7)}[/red]")
    print(f'[red]Error: {message}[/red]')
    print(f"[red]{'-' * (len(message) + 7)}[/red]")


def print_success(message: str):
    print(f"[green]{'-' * (len(message) + 9)}[/green]")
    print(f'[green]Success: {message}[/green]')
    print(f"[green]{'-' * (len(message) + 9)}[/green]")


def print_note(message: str):
    print(f"[cyan]{'-' * (len(message) + 6)}[/cyan]")
    print(f'[cyan]Note: {message}[/cyan]')
    print(f"[cyan]{'-' * (len(message) + 6)}[/cyan]")

