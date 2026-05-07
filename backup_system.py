# backup_system.py

import os
import json
import shutil
from datetime import datetime

APP_DATA_DIR = os.path.join(os.path.expanduser("~"), "HamzaServices")
BACKUP_DIR = os.path.join(APP_DATA_DIR, "backups")

SETTINGS_FILE = os.path.join(APP_DATA_DIR, "settings.json")
CLIENTS_FILE = os.path.join(APP_DATA_DIR, "clients.json")

os.makedirs(BACKUP_DIR, exist_ok=True)


def create_backup():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_folder = os.path.join(BACKUP_DIR, f"backup_{timestamp}")

    os.makedirs(backup_folder, exist_ok=True)

    if os.path.exists(SETTINGS_FILE):
        shutil.copy2(
            SETTINGS_FILE,
            os.path.join(backup_folder, "settings.json")
        )

    if os.path.exists(CLIENTS_FILE):
        shutil.copy2(
            CLIENTS_FILE,
            os.path.join(backup_folder, "clients.json")
        )

    return backup_folder


def list_backups():
    if not os.path.exists(BACKUP_DIR):
        return []

    backups = []

    for item in os.listdir(BACKUP_DIR):
        full_path = os.path.join(BACKUP_DIR, item)

        if os.path.isdir(full_path):
            backups.append(item)

    backups.sort(reverse=True)
    return backups


def restore_backup(backup_name):
    backup_folder = os.path.join(BACKUP_DIR, backup_name)

    if not os.path.exists(backup_folder):
        return False

    settings_backup = os.path.join(backup_folder, "settings.json")
    clients_backup = os.path.join(backup_folder, "clients.json")

    if os.path.exists(settings_backup):
        shutil.copy2(settings_backup, SETTINGS_FILE)

    if os.path.exists(clients_backup):
        shutil.copy2(clients_backup, CLIENTS_FILE)

    return True


def delete_backup(backup_name):
    backup_folder = os.path.join(BACKUP_DIR, backup_name)

    if not os.path.exists(backup_folder):
        return False

    shutil.rmtree(backup_folder)
    return True


def get_latest_backup():
    backups = list_backups()

    if not backups:
        return "لا توجد نسخ احتياطية"

    return backups[0]


if __name__ == "__main__":
    print("آخر نسخة احتياطية:")
    print(get_latest_backup())
