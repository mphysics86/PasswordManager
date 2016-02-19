
#=====Password Manager=======

import sqlite3
import json
import pyperclip
import getpass
from hashlib import sha256

_DB_NAME = "c:/users/lenovo/documents/accounts.db"
_ALPHABET = ('abcdefghijklmnopqrstuvwxyz'
            'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            '0123456789')

#===== User functions ==============
def add_service(service,username,dbname=_DB_NAME,
                length=10, alphabet=_ALPHABET, symbols=False):
    """Add a new service to the database."""
    dyct = _make_service_info_dict(service,username,length,alphabet,symbols)
    _save_service_info(dyct,dbname)
    print "New service: '{}' has been saved to {}.".format(service,dbname)

def remove_service(service,dbname=_DB_NAME):
    """Remove service info from database. Ask user to confirm before removing."""
    print "\nAccount info for '{}' service will be permanently removed.\n".format(service) 
    confirmation = raw_input("Delete this service? (y/n): ")
    if confirmation is 'n':
        print "\nInfo for '{}' service has NOT been removed.".format(service)
        return
    con = sqlite3.connect(dbname)
    con.execute('DELETE FROM Accounts WHERE service_name = ?',(service,))
    con.commit()
    con.close()
    print "Info for '{}' service has been removed.".format(service)

def password(service,dbname =_DB_NAME,show=False):
    """Get the password for the service. Place it on the clipboard."""
    master_pw = getpass.getpass("Password: ")
    dyct = _load_service_info(service,dbname)
    new_password = _make_password(dyct,master_pw)
    pyperclip.copy(new_password)
    print "\nYour password has been copied to the clipboard."
    if show:
        print new_password
    
def username(service,dbname=_DB_NAME):
    """Get the username for the service. Place it on the clipboard."""
    dyct = _load_service_info(service,dbname)
    username = _get_service_info(dyct,'username')
    pyperclip.copy(username)
    print "\nYour username has been copied to the clipboard.\n"
    return username

def peek(dbname = _DB_NAME,service=None):
    """Show which services are stored in the database.
    'service' can be set to a particular service name 
    to print info for that service."""
    if service:
        try:
            dyct = _load_service_info(service,dbname)
            print "\nAccount info for '{}' service:\n".format(service)
            for key in dyct:
                print "{}: {}".format(key,dyct[key])
        except:
            raise KeyError("'{}' service is not in the database.".format(service))
    else:
        service_list = _get_service_list(dbname)
        print "List of services in {}:".format(dbname)
        for item in service_list:
            print item

#===== Helper functions for generating a password=========

def _get_hexdigest(salt, password):
    """Return a hashing of salt+password."""
    return sha256(salt+password).hexdigest()

def _make_password(dyct,password):
    """Constructs a password from the service info."""
    service, username, length, alphabet = _get_service_info(dyct)    
    raw_hexdigest = _make_password_helper(service, username, password)

    # Convert the hexdigest into decimal
    num = int(raw_hexdigest, 16)

    # What base will we convert `num` into?
    num_chars = len(alphabet)

    # Build up the new password one "digit" at a time,
    # up to a certain length    
    chars = []
    while len(chars) < length:
        num, idx = divmod(num, num_chars)
        chars.append(alphabet[idx])
    return ''.join(chars)

def _make_password_helper(service, username, password):
    """Helper function for make_password().
    Returns a raw hexdigest hashing of inputs."""
    salt = _get_hexdigest(username, service)[:20]
    hsh = _get_hexdigest(salt, password)
    return ''.join((salt, hsh))

def _make_service_info_dict(service,username,length,alphabet=_ALPHABET,symbols=False):
    """Create a dictionary to hold service info for the service."""
    dyct = {"service":service, 
            "username":username, 
            "length":length,
            "alphabet":alphabet
           }
    if symbols:
        dyct['alphabet'] += '!@#$%^&*()-_'
    return dyct

#========== Helper functions for accessing service data =================
def _get_service_info(dyct,key=None):
    """Return service info from the dictionary. If a key is passed,
    Retrive only that key"""
    if key:
        return dyct.get(key,False)
    else:
        return dyct['service'],dyct['username'],dyct['length'],dyct['alphabet']
    
def _get_service_list(dbname):
    """Return a list of services in the database."""
    con = sqlite3.connect(dbname)
    lyst = []
    for name in con.execute("SELECT service_name FROM Accounts"):
        lyst.append(name[0])
    con.close()
    return lyst

def _save_service_info(dyct,dbname):
    """Saves account info to a sqlite3 database."""
    con = sqlite3.connect(dbname)
    con.execute("CREATE TABLE IF NOT EXISTS Accounts(service_name TEXT PRIMARY KEY                NOT NULL, data TEXT NOT NULL)")
    con.commit()
    con.execute("INSERT OR REPLACE INTO Accounts(service_name,data)        VALUES(?,?);", (dyct['service'],json.dumps(dyct)))
    con.commit()
    con.close()

def _load_service_info(service,dbname):
    """Returns service information as a dicitonary."""
    con = sqlite3.connect(dbname)
    for data in con.execute("SELECT data FROM Accounts WHERE service_name = ?",(service,)):
        dyct = json.loads(data[0])
    con.close()
    return dyct
    

