import sys
import hashlib
import subprocess

# run pip install bcrypt in terminal
try:
    import bcrypt
except ImportError:
    print("bcrypt not found. Attempting to install...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'bcrypt'])
        import bcrypt  # Now that bcrypt is installed, import it
    except subprocess.CalledProcessError:
        print("Error installing bcrypt. Please install it manually using 'pip install bcrypt'")
        sys.exit(1)

run = True 

def print_header():
    print("-------------------------------------\n"\
          "--- crackhead cracker crack crack ---\n"\
          "---------------------------------------")

def get_password():
    return input("Enter a password: ")

def get_mode_choice():
    try:
        return int(input("\n---------Options---------\n"
                          "Enter 0 to change password\n"\
                          "Enter 1 to use dictionary\n"\
                          "Enter 2 to brute force\n"\
                          "Enter 3 to convert to MD5\n"\
                          "Enter 4 to convert to SHA256\n"\
                          "Enter 5 to convert to BCrypt\n"\
                          "Enter 6 to quit\n"))
    except ValueError:
        print("Please enter a valid mode!")

def dictionary_crack(pwd, h_mode):
    pass_list = open("passList.txt", "r").read()
    word_list = pass_list.splitlines()
    
    for guess in word_list:
        if h_mode == 5 and bcrypt.checkpw(guess.encode(), pwd):
            print("\nCracked password:", guess)
            return
        
        hashed_guess = to_hash(guess, h_mode) if h_mode > 2 else guess
        
        if h_mode != 5 and hashed_guess == pwd:
            print("\nCracked password:", guess)
            return
    
    print("\nDictionary failed :( \nMaybe try brute forcing?")

def brute_crack(pwd, size, h_mode, guess=""):
    global count
    global found
    
    if size == 0:
        count += 1
        if h_mode == 5 and bcrypt.checkpw(guess.encode(), pwd):
            found = True
            print("\nCracked password:", guess)
            return
        
        hashed_guess = to_hash(guess, h_mode) if h_mode > 2 else guess
        
        if h_mode != 5 and hashed_guess == pwd:
            found = True
            print("\nCracked password:", guess)
            return
        
        if h_mode > 2 and count % 3000000 == 0 or count % 7500000 == 0:
            print("Cracking...")
    else:
        for char in range(32, 127):
            if found:
                return
            new_guess = guess + chr(char)
            brute_crack(pwd, size - 1, h_mode, new_guess)

def to_hash(pwd, mode):
    if mode == 3:
        return hashlib.md5(pwd.encode()).hexdigest()
    elif mode == 4:
        return hashlib.sha256(pwd.encode()).hexdigest()
    elif mode == 5:
        return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt())

def check_mode(mode, h_mode=0):
    global pwd
    global hash_mode
    if mode == 0:
        hash_mode = 0
        pwd = get_password()
    elif mode == 1:
        dictionary_crack(pwd, h_mode)
    elif mode == 2:
        global found
        found = False
        for x in range(1, 21):
            brute_crack(pwd, x, h_mode)
    elif mode == 6:
        global run
        run = False
    elif 2 < mode < 6:
        hash_mode = mode
        pwd = to_hash(pwd, mode)
        print("\nHashed password:", pwd)
        if mode == 5:
            print("Warning: BCrypt cracking is VERY slow.")
    else:
        print("Please enter a valid mode!")

def main(in_mode=-1, in_pwd=""):
    global count
    global pwd
    global hash_mode
    hash_mode = 0

    print_header()
    
    if in_mode != -1:
        print("Using mode " + str(in_mode) + "...")
    if in_pwd == "":
        pwd = get_password()
    else:
        pwd = in_pwd

    while run:
        count = 0
        if int(in_mode) > 0:
            check_mode(in_mode)
            in_mode = -1
        else:
            mode = get_mode_choice()
            check_mode(mode, hash_mode)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        main()
    elif len(sys.argv) == 2:
        try:
            if 0 < int(sys.argv[1]) < 6:
                main(int(sys.argv[1]))
            else:
                print("Please enter a valid mode!")
        except ValueError:
            print("Please enter a valid mode!")
    elif len(sys.argv) == 3:
        try:
            if 0 < int(sys.argv[1]) < 6:
                main(int(sys.argv[1]), sys.argv[2])
            else:
                print("Please enter a valid mode!")
        except ValueError:
            print("Please enter a valid mode!")
    elif len(sys.argv) > 2:
        print("Please enter only one mode and a password!")
