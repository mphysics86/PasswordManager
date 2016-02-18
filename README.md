# PasswordManager
This project is a simple password manager written in Python. It was inspired by the password manager code written by [Charles Leifer](http://charlesleifer.com/blog/creating-a-personal-password-manager/). The basic functionality has been established, but it is still a work in progress.

## How to Use it
The password manager includes the following user functions:

- `add_service(service, username, dbname)` - Adds a new service to the database. Stores the information necessary to reconstruct a password.
- `remove_service(service, dbname)` - Remove a service from the database.
- `password(service,dbname,show=False)` - Generate a password for a service. User will be prompted for a master password to generate the correct password. Saves the password to the clipboard. If the `show` parameter is set to True, the password will be printed. Default behavior does not print the password.
- `username(service,dbname)` - Retrieve the username for the service. Prints the username and saves to the clipboard.
- `peek(dbname,service = None)` - Default behavior lists the accounts stored in the database. Information for a specific service will be displayed if the `service` parameter is set to a service name.

Some notes about the function parameters:
- `dbname` - The database name that stores the account information. By default, account information will be saved to a database named `accounts.db`. Unless the user wishes to create a new database or change the database name, *the dbname parameter does not need to be set by the user*.
- `service` - This is the name of the service or account as a string.

