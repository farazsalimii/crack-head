import sys
import hashlib
import bcrypt

def main(inMode=-1, inPwd=""):
    hashMode = 0

    print("~~~~~~~~~~~~~~~~~~~")
    print("~~~~~ CRACKER ~~~~~")
    print("~~~~~~~~~~~~~~~~~~~")

    if inMode != -1:
        print("Using mode", inMode, "...")
    
    if inPwd == "":
        pwd = input("Enter a password: ")
    else:
        pwd = inPwd
    
    while True:
        count = 0
        
        if int(inMode) > 0:
            checkMode(inMode)
            inMode = -1
        else:
            try:
                mode = int(input("Enter 0 to change password\nEnter 1 to use dictionary\nEnter 2 to ..."))
                
                if mode == 0:
                    pwd = input("Enter a new password: ")
                elif mode == 1:
                    # Add code for dictionary mode
                    pass
                elif mode == 2:
                    # Add code for mode 2
                    pass
                else:
                    print("Invalid mode. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")
            except KeyboardInterrupt:
                print("\nProgram terminated.")
                break

def checkMode(mode):
    # Add code to handle different modes
    pass

if __name__ == "__main__":
    main()
    
