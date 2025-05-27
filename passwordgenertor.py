import random

# Define all the characters we can use for passwords
lowercase_letters = "abcdefghijklmnopqrstuvwxyz"
uppercase_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
numbers = "0123456789"
special_characters = "!@#$%^&*"

def ask_user_for_password_length():
    """Ask the user how long they want their password to be"""
    print("Welcome to the Password Generator!")
    print("-" * 35)
    
    while True:
        try:
            length = int(input("How many characters do you want in your password? "))
            if length <= 0:
                print("Please enter a number greater than 0")
            else:
                return length
        except ValueError:
            print("Please enter a valid number")

def ask_user_what_to_include():
    """Ask the user what types of characters to include"""
    print("\nWhat do you want to include in your password?")
    print("1. Only lowercase letters (like: abc)")
    print("2. Only uppercase letters (like: ABC)")
    print("3. Only numbers (like: 123)")
    print("4. Mix of letters and numbers")
    print("5. Everything (letters, numbers, and symbols) - Most Secure!")
    
    while True:
        choice = input("\nEnter your choice (1-5): ")
        if choice in ["1", "2", "3", "4", "5"]:
            return choice
        else:
            print("Please choose a number between 1 and 5")

def get_characters_to_use(user_choice):
    """Based on what the user chose, decide which characters we can use"""
    if user_choice == "1":
        # Only lowercase letters
        return lowercase_letters
    
    elif user_choice == "2":
        # Only uppercase letters
        return uppercase_letters
    
    elif user_choice == "3":
        # Only numbers
        return numbers
    
    elif user_choice == "4":
        # Mix of letters and numbers
        return lowercase_letters + uppercase_letters + numbers
    
    elif user_choice == "5":
        # Everything - most secure option
        return lowercase_letters + uppercase_letters + numbers + special_characters

def create_password(length, available_characters):
    """Create a random password using the available characters"""
    password = ""
    
    # Pick random characters one by one until we reach the desired length
    for i in range(length):
        random_character = random.choice(available_characters)
        password = password + random_character
    
    return password

def show_password_info(password):
    """Display the password and some information about it"""
    print("\n" + "=" * 50)
    print("YOUR NEW PASSWORD IS READY!")
    print("=" * 50)
    print(f"Password: {password}")
    print(f"Length: {len(password)} characters")
    
    # Give the user some tips about their password
    if len(password) < 8:
        print("💡 Tip: Passwords with 8 or more characters are more secure!")
    
    if any(char in special_characters for char in password):
        print("✅ Great! Your password includes special characters - very secure!")
    
    if any(char.isupper() for char in password) and any(char.islower() for char in password):
        print("✅ Good! Your password has both uppercase and lowercase letters!")
    
    print("=" * 50)

def ask_to_generate_another():
    """Ask if the user wants to create another password"""
    while True:
        answer = input("\nDo you want to generate another password? (yes/no): ").lower()
        if answer in ["yes", "y"]:
            return True
        elif answer in ["no", "n"]:
            return False
        else:
            print("Please answer 'yes' or 'no'")

def main():
    """This is the main function that runs our password generator"""
    
    # Keep generating passwords until the user wants to stop
    while True:
        # Step 1: Ask how long the password should be
        password_length = ask_user_for_password_length()
        
        # Step 2: Ask what types of characters to include
        user_choice = ask_user_what_to_include()
        
        # Step 3: Get the characters we can use based on their choice
        characters_we_can_use = get_characters_to_use(user_choice)
        
        # Step 4: Create the actual password
        new_password = create_password(password_length, characters_we_can_use)
        
        # Step 5: Show the password to the user
        show_password_info(new_password)
        
        # Step 6: Ask if they want another password
        if not ask_to_generate_another():
            print("\nThanks for using the Password Generator! Stay secure! 🔒")
            break

# This is where our program starts running
if __name__ == "__main__":
    main()