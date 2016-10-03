
"""
Settings for the staticguru tool
"""

import os
import pwd

BACKGROUND_SLEEP_MINUTES = 10

# Set the path
REPOSITORY_PATH = "/{path_to_commitguru_code_analyser}/ingester/CASRepos/git"


DATABASE_SETTINGS = {
    "DATABASE_HOST": "hostname",
    "DATABASE_NAME": "database_name",
    "DATABASE_USERNAME": "database_username",
    "DATABASE_PASSWORD": "database_password"
}

# If a commit guru repo id is provided
# REPO_TO_ANALYSE = "42e73e16-e20a-4b17-99a3-4dd7b35a6155"
REPO_TO_ANALYSE = None

# If TOIF is not configured in session
TOIF_EXECUTABLE = "/{path to toif binary}/toif"

ADAPTOR_OUTPUT_DIR = "target/toif_run"
KDM_FILE = "assimilated.kdm"

REPROCESS_FAILURES_HOURS = 1


def get_local_settings():

    username = __get_username__()

    if "DATABASE_HOST" in DATABASE_SETTINGS:
        return DATABASE_SETTINGS
    else:
        print("Database settings need to be defined")


def __get_username__():
    return pwd.getpwuid(os.getuid()).pw_name


if __name__ == "__main__":
    # Helps you find out your username
    print("Your username is: '%s'" % __get_username__())




