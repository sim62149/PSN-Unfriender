import json
import re
from urllib.parse import parse_qs, urlparse
import requests
from tqdm import tqdm
from colorama import init, Fore, Style

# Initialisation de colorama
init(autoreset=True)

def obtain_auth_code(npsso_token):
    url = "https://ca.account.sony.com/api/authz/v3/oauth/authorize"
    headers = {"Cookie": f"npsso={npsso_token}"}
    params = {
        "access_type": "offline",
        "client_id": "09515159-7237-4370-9b40-3806e67c0891",
        "scope": "psn:mobile.v2.core psn:clientapp",
        "redirect_uri": "com.scee.psxandroid.scecompcall://redirect",
        "response_type": "code",
    }
    response = requests.get(url, headers=headers, params=params, allow_redirects=False)
    response.raise_for_status()

    location_url = response.headers["location"]
    parsed_url = urlparse(location_url)
    parsed_qs = parse_qs(parsed_url.query)
    return parsed_qs['code'][0]

def obtain_auth_jwt(code):
    url = "https://ca.account.sony.com/api/authz/v3/oauth/token"
    body = {
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": "com.scee.psxandroid.scecompcall://redirect",
        "scope": "psn:mobile.v2.core psn:clientapp",
        "token_format": "jwt",
    }
    headers = {
        "Authorization": "Basic MDk1MTUxNTktNzIzNy00MzcwLTliNDAtMzgwNmU2N2MwODkxOnVjUGprYTV0bnRCMktxc1A="
    }
    response = requests.post(url, headers=headers, data=body)
    response.raise_for_status()
    return response.json()["access_token"]

def authenticate_with_npsso_token(npsso_token):
    code = obtain_auth_code(npsso_token)
    return obtain_auth_jwt(code)

def get_friend_list(jwt_token):
    url = "https://m.np.playstation.com/api/userProfile/v1/internal/users/me/friends"
    params = {"limit": 1000}
    headers = {
        "Content-Type": "application/json",
        "accept-language": "en-US",
        "user-agent": "okhttp/4.9.2",
        "Authorization": f"Bearer {jwt_token}"
    }
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()['friends']

def profile_ids_to_names_chunked(jwt_token, profile_ids, start=0):
    url = "https://m.np.playstation.com/api/userProfile/v1/internal/users/profiles"
    params = {"accountIds": ",".join(profile_ids[start:start + 100])}
    headers = {
        "Content-Type": "application/json",
        "accept-language": "en-US",
        "user-agent": "okhttp/4.9.2",
        "Authorization": f"Bearer {jwt_token}"
    }
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()['profiles']

def profile_ids_to_names(jwt_token, profile_ids):
    to_return = []
    chunk_size = 100
    num_chunks = len(profile_ids) // chunk_size
    for i in range(num_chunks + 1):
        start_index = i * chunk_size
        if profile_ids[start_index:start_index + chunk_size]:
            to_return.extend(profile_ids_to_names_chunked(jwt_token, profile_ids, start_index))
    return to_return

def remove_friend(jwt_token, profile_id):
    url = f"https://m.np.playstation.com/api/userProfile/v1/internal/users/me/friends/{profile_id}"
    headers = {
        "Content-Type": "application/json",
        "accept-language": "en-US",
        "user-agent": "okhttp/4.9.2",
        "Authorization": f"Bearer {jwt_token}"
    }
    response = requests.delete(url, headers=headers)
    if response.status_code == 429:
        print(Fore.YELLOW + f"Rate limit reached for friend ID: {profile_id}. Retrying later...")
        return False
    response.raise_for_status()
    return True

def is_name_whitelisted(patterns, name):
    return any(re.match(pattern, name) for pattern in patterns)

def display_friends(friends, title, color):
    print(color + f"\n{title} ({len(friends)}):")
    print(Style.RESET_ALL + "\n".join([f"{friend[1]}" for friend in friends]))

if __name__ == '__main__':
    # Choix de la langue
    print("Choose your language / Choisissez votre langue:")
    print("1. English")
    print("2. Français")
    language = input("Enter 1 or 2 / Entrez 1 ou 2: ")

    if language == "1":
        messages = {
            "welcome": "Welcome to PSN Unfriender!",
            "fetching_friends": "Fetching friend list...",
            "file_not_found": "Error: configuration.json file not found.",
            "auth_failed": "Authentication failed",
            "validate_output": "\nValidate the output above. Continue? (y/n) ",
            "removing_friends": "Removing {} friends..."
        }
    elif language == "2":
        messages = {
            "welcome": "Bienvenue dans PSN Unfriender !",
            "fetching_friends": "Récupération de la liste d'amis...",
            "file_not_found": "Erreur : fichier configuration.json introuvable.",
            "auth_failed": "Échec de l'authentification",
            "validate_output": "\nValidez les informations ci-dessus. Continuer ? (o/n) ",
            "removing_friends": "Suppression de {} amis..."
        }
    else:
        print(Fore.RED + "Invalid choice. Exiting.")
        exit(1)

    print(Fore.CYAN + messages["welcome"])

    try:
        with open("configuration.json", 'r') as file:
            config = json.load(file)
    except FileNotFoundError:
        print(Fore.RED + messages["file_not_found"])
        exit(1)

    try:
        auth = authenticate_with_npsso_token(config['npsso_token'])
    except Exception as e:
        print(Fore.RED + f"{messages['auth_failed']}: {e}")
        exit(1)

    print(Fore.CYAN + messages["fetching_friends"])
    friend_ids = get_friend_list(auth)

    profiles = profile_ids_to_names(auth, friend_ids)
    names = [p['onlineId'] for p in profiles]

    friends_zip = list(zip(friend_ids, names))
    to_remove = []
    to_keep = []

    for friend in friends_zip:
        if is_name_whitelisted(config['nameWhitelistPatterns'], friend[1]):
            to_keep.append(friend)
        else:
            to_remove.append(friend)

    display_friends(to_keep, "Friends to keep", Fore.GREEN)
    display_friends(to_remove, "Friends to remove", Fore.RED)

    if input(Fore.YELLOW + messages["validate_output"]).lower() not in ("y", "o"):
        exit(1)

    print(Fore.CYAN + messages["removing_friends"].format(len(to_remove)))
    for friend in tqdm(to_remove):
        friend_id = friend[0]
        success = remove_friend(auth, friend_id)
        if not success:
            break  # Stop on rate limit error
