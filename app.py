import os
import time
import json
import pickle
import hashlib
import getpass
import pyperclip

from pathlib import Path

from rich import print
from rich.console import Console
from dt_security import generate_password

from contributors import *
from app_constants import *

from dt_security import (
    encrypt_text,
    decrypt_text,
    validate_password_strength,
)

__version__ = "1.5"


def get_now(format: str = DATE_TIME_FORMAT) -> str:
    """Get now"""

    now: str = time.strftime(format)
    return now


def sort_items_by_name_and_update_ids() -> None:
    """Sort items by name and update IDs"""

    items.sort(key=lambda item: item[KEY_NAME_NAME])
    for index, item in enumerate(iterable=items, start=1):
        item[KEY_NAME_ID] = index


def clear_screen() -> None:
    """Clear screen"""

    os.system(command="cls" if os.name == "nt" else "clear")


def display(title: str, display_line: bool = False) -> None:
    """Display title"""

    console.print(title, style=STYLE_COLUMN_HEADER)

    if display_line:
        console.print("-" * len(title), style=STYLE_COLUMN_HEADER)


def clear_screen_and_display(title: str) -> None:
    """Clear screen and display title"""

    clear_screen()

    display(
        title=title,
        display_line=True,
    )


def display_menu_and_get_user_prompt(menu_items: list[str]) -> str:
    """Display menu and get user prompt"""

    for menu_item in menu_items:
        console.print(menu_item, style=STYLE_MENU_ITEM)

    console.print("\nEnter your choice:", end=" ", style=STYLE_MESSAGE_WAITING)
    choice: str = input().strip()
    return choice


def goodbye() -> None:
    """Encrypt and save data before exit."""
    encrypt_and_save_data(password=master_password)

    console.print("\nGoodbye!\n", style=STYLE_MESSAGE_SUCCESS)
    exit()


def display_label(label: str, width: int, inline: bool = True) -> None:
    """Display label"""

    end: str = "\n"
    if inline:
        end = " "

    label = label.ljust(width, " ") + ":"
    console.print(label, end=end, style=STYLE_LABEL)


def fix_special_field_value(value: str) -> str:
    """Fix special field value"""

    value = value.replace(" ", "")
    return value


def press_enter_to_continue() -> None:
    """Press [ENTER] to continue"""

    message: str = "\nPress [ENTER] to continue..."
    console.print(message, end="", style=STYLE_MESSAGE_WAITING)
    input()


def add_new_item() -> None:
    """Add new item"""

    default_password_label: str = f"Default {LABEL_PASSWORD}"
    max_width: int = len(default_password_label)

    while True:
        clear_screen_and_display(title="Add New Item")

        display_label(label=f"Default {LABEL_EMAIL}", width=max_width)
        print(DEFAULT_EMAIL)

        display_label(label=f"Default {LABEL_MOBILE}", width=max_width)
        print(DEFAULT_MOBILE)

        display_label(label=f"Default {LABEL_USERNAME}", width=max_width)
        print(DEFAULT_USERNAME)

        display_label(label=default_password_label, width=max_width)
        print("System will generate a strong password!")

        print()

        label_name: str = f"{LABEL_NAME} (required)"
        display_label(label=label_name, width=max_width)
        name: str = input().strip()
        if name != "":
            break

    display_label(label=LABEL_EMAIL, width=max_width)
    email: str = fix_special_field_value(value=input().lower())
    if email == "":
        email = DEFAULT_EMAIL

    display_label(label=LABEL_MOBILE, width=max_width)
    mobile: str = fix_special_field_value(value=input().lower())
    if mobile == "":
        mobile = DEFAULT_MOBILE

    display_label(label=LABEL_USERNAME, width=max_width)
    username: str = fix_special_field_value(value=input().lower())
    if username == "":
        username = DEFAULT_USERNAME

    display_label(label=LABEL_PASSWORD, width=max_width)
    password: str = fix_special_field_value(value=input())
    if password == "":
        password = generate_password(
            length=GENERATED_PASSWORD_LENGTH,
        )

    display_label(label=LABEL_DESCRIPTION, width=max_width)
    description: str = input().strip()

    now: str = get_now()

    item: dict = {
        KEY_NAME_NAME: name,
        KEY_NAME_EMAIL: email,
        KEY_NAME_MOBILE: mobile,
        KEY_NAME_PASSWORD: password,
        KEY_NAME_USERNAME: username,
        KEY_NAME_DESCRIPTION: description,
        #
        KEY_NAME_INSERT_TIME: now,
        KEY_NAME_UPDATE_TIME: now,
    }

    items.append(item)

    sort_items_by_name_and_update_ids()

    display_success_message(message="Item added successfully!")
    press_enter_to_continue()


def edit_item(item: dict) -> None:
    """Edit item"""

    clear_screen_and_display(title="Edit Item")

    label_password: str = f"{LABEL_PASSWORD} (NEW)"
    max_width: int = len(label_password)

    display_label(label=LABEL_ID, width=max_width)
    print(item.get(KEY_NAME_ID, MESSAGE_NOT_SET))

    display_label(label=LABEL_NAME, width=max_width)
    print(item.get(KEY_NAME_NAME, MESSAGE_NOT_SET))

    display_label(label=LABEL_EMAIL, width=max_width)
    print(item.get(KEY_NAME_NAME, MESSAGE_NOT_SET))

    display_label(label=LABEL_MOBILE, width=max_width)
    print(item.get(KEY_NAME_MOBILE, MESSAGE_NOT_SET))

    display_label(label=LABEL_USERNAME, width=max_width)
    print(item.get(KEY_NAME_USERNAME, MESSAGE_NOT_SET))

    display_label(label=LABEL_PASSWORD, width=max_width)
    print(item.get(KEY_NAME_PASSWORD, MESSAGE_NOT_SET))

    display_label(label=LABEL_DESCRIPTION, width=max_width)
    print(item.get(KEY_NAME_DESCRIPTION, MESSAGE_NOT_SET))

    print()

    updated: bool = False

    display_label(label=LABEL_NAME, width=max_width)
    name: str = input().strip()
    if name == "":
        name = item[KEY_NAME_NAME]
    else:
        updated = True

    display_label(label=LABEL_EMAIL, width=max_width)
    email: str = fix_special_field_value(value=input().lower())
    if email == "":
        email = item[KEY_NAME_EMAIL]
    else:
        updated = True

    display_label(label=LABEL_MOBILE, width=max_width)
    mobile: str = fix_special_field_value(value=input().lower())
    if mobile == "":
        mobile = item[KEY_NAME_MOBILE]
    else:
        updated = True

    display_label(label=LABEL_USERNAME, width=max_width)
    username: str = fix_special_field_value(value=input().lower())
    if username == "":
        username = item[KEY_NAME_USERNAME]
    else:
        updated = True

    display_label(label=label_password, width=max_width)
    password: str = fix_special_field_value(value=input())
    if password == "":
        password = item[KEY_NAME_PASSWORD]
    elif password.upper() == "NEW":
        updated = True
        password = generate_password(
            length=GENERATED_PASSWORD_LENGTH,
        )
    else:
        updated = True

    display_label(label=LABEL_DESCRIPTION, width=max_width)
    description: str = input().strip()
    if description == "":
        description = item[KEY_NAME_DESCRIPTION]
    else:
        updated = True

    if updated:
        now: str = get_now()

        item.update(
            {
                KEY_NAME_NAME: name,
                KEY_NAME_EMAIL: email,
                KEY_NAME_MOBILE: mobile,
                KEY_NAME_PASSWORD: password,
                KEY_NAME_USERNAME: username,
                KEY_NAME_DESCRIPTION: description,
                #
                KEY_NAME_UPDATE_TIME: now,
            }
        )

        sort_items_by_name_and_update_ids()

        display_success_message(message="Item updated successfully.")
        press_enter_to_continue()


def display_error_message(message: str) -> None:
    """Display error message"""

    console.print(f"[-] {message}", style=STYLE_MESSAGE_ERROR)


def display_success_message(message: str) -> None:
    """Display success message"""

    console.print(f"\n[+] {message}", style=STYLE_MESSAGE_SUCCESS)


def display_items(display_password: bool = False) -> None:
    """Display items"""

    while True:
        clear_screen()

        if not items:
            display_error_message(message="No data found!")
            press_enter_to_continue()
            break

        display_table_header()
        for item in items:
            display_item_in_table_row(
                item=item,
                display_password=display_password,
            )
        display_table_footer()

        message: str = (
            "Type 'ID' and then press [ENTER] to display item details or just press [ENTER] to go back:"
        )
        console.print(message, end=" ", style=STYLE_MESSAGE_WAITING)
        choise: str = input().strip()

        if not choise:
            break

        try:
            choise_int: int = int(choise)
            display_item_details(item=items[choise_int - 1])
        except:
            pass


def get_duplicate_item(item: dict) -> dict:
    """Duplicate item"""

    now: str = get_now()

    new_item: dict = {
        KEY_NAME_INSERT_TIME: now,
        KEY_NAME_UPDATE_TIME: now,
        #
        KEY_NAME_NAME: item[KEY_NAME_NAME],
        KEY_NAME_EMAIL: item[KEY_NAME_EMAIL],
        KEY_NAME_MOBILE: item[KEY_NAME_MOBILE],
        KEY_NAME_USERNAME: item[KEY_NAME_USERNAME],
        KEY_NAME_PASSWORD: item[KEY_NAME_PASSWORD],
        KEY_NAME_DESCRIPTION: item[KEY_NAME_DESCRIPTION],
    }

    return new_item


def display_item_details(item: dict) -> None:
    """Display item details"""

    while True:
        clear_screen_and_display(title="Display Item Details")

        id: int = item.get(KEY_NAME_ID, MESSAGE_NOT_SET)
        name: str = item.get(KEY_NAME_NAME, MESSAGE_NOT_SET)
        email: str = item.get(KEY_NAME_EMAIL, MESSAGE_NOT_SET)
        mobile: str = item.get(KEY_NAME_MOBILE, MESSAGE_NOT_SET)
        username: str = item.get(KEY_NAME_USERNAME, MESSAGE_NOT_SET)
        password: str = item.get(KEY_NAME_PASSWORD, MESSAGE_NOT_SET)
        description: str = item.get(KEY_NAME_DESCRIPTION, MESSAGE_NOT_SET)
        insert_time: str = item.get(KEY_NAME_INSERT_TIME, MESSAGE_NOT_SET)
        update_time: str = item.get(KEY_NAME_UPDATE_TIME, MESSAGE_NOT_SET)

        max_width: int = len(LABEL_DESCRIPTION)

        display_label(label=LABEL_ID, width=max_width)
        print(id)

        display_label(label=LABEL_NAME, width=max_width)
        print(name)

        display_label(label=LABEL_EMAIL, width=max_width)
        print(email)

        display_label(label=LABEL_MOBILE, width=max_width)
        print(mobile, f"0{mobile}", f"+98{mobile}")

        display_label(label=LABEL_USERNAME, width=max_width)
        print(username)

        display_label(label=LABEL_PASSWORD, width=max_width)
        print(password)

        display_label(label=LABEL_INSERT_TIME, width=max_width)
        print(insert_time)

        display_label(label=LABEL_UPDATE_TIME, width=max_width)
        print(update_time)

        display_label(label=LABEL_DESCRIPTION, width=max_width)
        print(description)

        console.print()

        menu_items: list[str] = [
            "1. Edit",
            "2. Duplicate",
            "3. Copy password in clipboard",
            "Just Press [ENTER] to go back",
            "Just Type 'DELETE' (uppercase) to delete!",
        ]

        choice: str = display_menu_and_get_user_prompt(
            menu_items=menu_items,
        )

        match choice:
            case "1":
                edit_item(item=item)
            case "2":
                new_item: dict = get_duplicate_item(item=item)
                items.append(new_item)
                sort_items_by_name_and_update_ids()
                break
            case "3":
                pyperclip.copy(text=password)
                break
            case "DELETE":
                items.pop(id - 1)
                sort_items_by_name_and_update_ids()
                break
            case _:
                break


def get_total_width() -> int:
    """Get total width"""

    total_width: int = (
        8  # Pipe Count: ('|')
        + COLUMN_WIDTH_ID
        + COLUMN_WIDTH_NAME
        + COLUMN_WIDTH_EMAIL
        + COLUMN_WIDTH_MOBILE
        + COLUMN_WIDTH_USERNAME
        + COLUMN_WIDTH_PASSWORD
        + COLUMN_WIDTH_UPDATE_TIME
    )

    return total_width


def display_table_header() -> None:
    """Display table header"""

    id: str = LABEL_ID
    name: str = "Name: URL / Application / Device"
    email: str = "Email Address"
    mobile: str = LABEL_MOBILE
    username: str = LABEL_USERNAME
    password: str = LABEL_PASSWORD
    update_time: str = "Update"

    id = id.ljust(COLUMN_WIDTH_ID, " ")
    name = name.ljust(COLUMN_WIDTH_NAME, " ")
    email = email.ljust(COLUMN_WIDTH_EMAIL, " ")
    mobile = mobile.ljust(COLUMN_WIDTH_MOBILE, " ")
    username = username.ljust(COLUMN_WIDTH_USERNAME, " ")
    password = password.ljust(COLUMN_WIDTH_PASSWORD, " ")
    update_time = update_time.ljust(COLUMN_WIDTH_UPDATE_TIME, " ")

    header: str = f"|{id}|{name}|{email}|{mobile}|{username}|{password}|{update_time}|"

    total_width: int = get_total_width()

    console.print("-" * total_width, style=STYLE_LABEL)
    console.print(header, style=STYLE_LABEL)
    console.print("-" * total_width, style=STYLE_LABEL)


def display_item_in_table_row(item: dict, display_password: bool = False) -> None:
    """Display item"""

    id: str = item.get(KEY_NAME_ID, MESSAGE_NOT_SET)
    name: str = item.get(KEY_NAME_NAME, MESSAGE_NOT_SET)
    email: str = item.get(KEY_NAME_EMAIL, MESSAGE_NOT_SET)
    mobile: str = item.get(KEY_NAME_MOBILE, MESSAGE_NOT_SET)
    username: str = item.get(KEY_NAME_USERNAME, MESSAGE_NOT_SET)
    password: str = item.get(KEY_NAME_PASSWORD, MESSAGE_NOT_SET)
    update_time: str = item.get(KEY_NAME_UPDATE_TIME, MESSAGE_NOT_SET)

    id = str(id).rjust(COLUMN_WIDTH_ID, " ")

    name = name.ljust(COLUMN_WIDTH_NAME, " ")
    email = email.ljust(COLUMN_WIDTH_EMAIL, " ")
    mobile = mobile.ljust(COLUMN_WIDTH_MOBILE, " ")
    username = username.ljust(COLUMN_WIDTH_USERNAME, " ")
    update_time = update_time.ljust(COLUMN_WIDTH_UPDATE_TIME, " ")

    update_time = update_time[0:10]

    if not display_password:
        password = "**********"
    password = password.ljust(COLUMN_WIDTH_PASSWORD, " ")

    console.print("|", style=STYLE_LABEL, end="")
    console.print(
        f"{id}|{name}|{email}|{mobile}|{username}|{password}|{update_time}", end=""
    )
    console.print("|", style=STYLE_LABEL)


def display_table_footer() -> None:
    """Display table footer"""

    total_width: int = get_total_width()
    console.print("-" * total_width, style=STYLE_LABEL)


def change_master_password() -> None:
    """Change master password"""

    global master_password

    clear_screen_and_display(title="Change Master Password")
    console.print(
        "\nEnter Previous Master Password:",
        end=" ",
        style=STYLE_MESSAGE_WAITING,
    )
    password: str = getpass.getpass(prompt="")

    if password == master_password:
        master_password = set_master_password(is_change_password=True)
    else:
        display_error_message(message="Previous Master Password is incorrect.")
        press_enter_to_continue()


def display_about() -> None:
    """Display About"""

    # About Dariush Tasdighi
    clear_screen_and_display(title="About DT Password Manager Developers")

    max_width: int = len(TELEGRAM_CHANNEL_1_LABEL)

    display_label(label=f"__Version__", width=len(__version__))
    print(__version__)

    print()
    for name, details in CONTRIBUTORS.items():
        display(title=f"★ {name}")
        for label, value in details.items():
            display_label(label=f" • {label}", width=max_width)
            print(value)

        print()

    press_enter_to_continue()


def display_main_menu() -> None:
    """Display main menu"""

    while True:
        title: str = f"Welcome to DT Password Manager - Version: {__version__}"
        clear_screen_and_display(title=title)

        menu_items: list[str] = [
            "1. Add New",
            "2. List with Password",
            "3. List without Password",
            "4. Change Master Password" "",
            "",
            "5. About",
            "",
            "Type '0' | bye | end | exit | quit | 'q' for save and exit...",
        ]

        choice: str = display_menu_and_get_user_prompt(
            menu_items=menu_items,
        )

        match choice.lower():
            case "1":
                add_new_item()
            case "2":
                display_items(display_password=True)
            case "3":
                display_items(display_password=False)
            case "4":
                change_master_password()
            case "5":
                display_about()
            case "0" | "bye" | "end" | "exit" | "quit" | "q":
                goodbye()


def is_master_password_set() -> bool:
    """Check if the master password file exists and is non-empty."""

    # Check if file exists and is non-empty
    return DATA_FILE_PATH.is_file() and DATA_FILE_PATH.stat().st_size > 0


def set_master_password(is_change_password: bool = False) -> str:
    """Get master password and save it globally."""

    # Choose title and prompt based on is_change_password
    if is_change_password:
        title: str = "Change Master Password"
        prompt_message = "\nEnter New Master Password:"

    else:
        title: str = "Set up your Master Password"
        prompt_message = "\nEnter Master Password:"

    while True:
        clear_screen_and_display(title=title)

        console.print(prompt_message, end=" ", style=STYLE_MESSAGE_WAITING)
        password: str = getpass.getpass(prompt="")

        message: str
        is_valid: bool

        is_valid, message = validate_password_strength(password=password)

        if not is_valid:
            display_error_message(message=message)
            press_enter_to_continue()
            continue

        # Confirm password
        console.print("Confirm Master Password:", end=" ", style=STYLE_MESSAGE_WAITING)
        confirm_password: str = getpass.getpass(prompt="")

        if password != confirm_password:
            message: str = "Passwords do not match. Please try again."
            display_error_message(message=message)
            press_enter_to_continue()
            continue

        # Succuss
        display_success_message(message=message)
        # NOTE: This line Ensures the password is preserved even if the user exits with Ctrl+C rather than 'bye' or 'end'.
        encrypt_and_save_data(password=password)
        return password


def hash_data(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()


def handle_backup_if_changed(password: str, new_json_string: str) -> None:

    new_data_hash: str = hash_data(new_json_string)

    with open(DATA_FILE_PATH, "rb") as f:
        existing_encrypted = pickle.load(file=f)

    _, existing_json_string = decrypt_text(
        encrypted_data=existing_encrypted, password=password
    )

    existing_hash = hash_data(data=existing_json_string)

    if existing_hash != new_data_hash:
        now: str = get_now(BACKUP_FILE_FORMAT)

        backup_file_path: Path = DATA_FILE_PATH.with_name(
            f"{DATA_FILE_PATH.stem}_{now}{DATA_FILE_PATH.suffix}"
        )
        DATA_FILE_PATH.rename(target=backup_file_path)


def encrypt_and_save_data(password: str) -> None:
    """Encrypt items list using AES-256-GCM (Quantum-resistant symmetric encryption)"""

    # 1. Serialize new data
    new_json_string: str = json.dumps(obj=items)

    # Backup last file if there is change in data

    if DATA_FILE_PATH.is_file():
        handle_backup_if_changed(password=password, new_json_string=new_json_string)

    encrypted_data: dict = encrypt_text(plaintext=new_json_string, password=password)

    with open(file=DATA_FILE_PATH, mode="wb") as f:
        pickle.dump(obj=encrypted_data, file=f)


def load_and_decrypt_data() -> str:
    """Decrypt items list using AES-256-GCM (Quantum-resistant symmetric encryption)"""
    while True:
        title: str = f"Master Password Authentication"
        clear_screen_and_display(title=title)

        console.print("\nEnter Master Password:", end=" ", style=STYLE_MESSAGE_WAITING)
        password: str = getpass.getpass(prompt="")

        with open(file=DATA_FILE_PATH, mode="rb") as f:
            encrypted_data: dict = pickle.load(file=f)

        plaintext: str
        is_decrypted: bool

        is_decrypted, plaintext = decrypt_text(
            encrypted_data=encrypted_data, password=password
        )

        if not is_decrypted:
            display_error_message(message=plaintext)
            press_enter_to_continue()
            continue

        if is_decrypted:
            items.clear()
            items.extend(json.loads(plaintext))

            display_success_message(message=plaintext)
            return password


def main() -> None:
    """The main of program"""

    display_main_menu()


if __name__ == "__main__":
    try:
        console = Console()

        items: list[dict] = []
        master_password: str = ""

        if not is_master_password_set():
            master_password = set_master_password()
        else:
            master_password = load_and_decrypt_data()

        main()

    except KeyboardInterrupt:
        print()

    except Exception as error:
        print(f"\n[-] {error}!")

    print()
