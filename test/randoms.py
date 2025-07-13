import os, sys, signal
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.database import LMDBDict

def main():
    """Main function to demonstrate the LMDBDict module."""
    
    # db_path = "./my-modular-db"
    
    # Using a 'with' statement automatically handles opening and closing
    # with LMDBDict(db_path) as db:
    with LMDBDict() as db:
        print("✅ Database connection opened.")
        
        # 1. Define data
        user_key = "user:456"
        user_data = {
            'username': 'casey',
            'email': 'casey@example.com',
            'login_count': 15
        }
        
        # 2. Store the data using the module's .put() method
        db.put(user_key, user_data)
        print(f"Stored data for key: '{user_key}'")
        
        # 3. Retrieve the data using the .get() method
        retrieved_data = db.get(user_key)
        print(f"Retrieved data: {retrieved_data}")
        
        # 4. Delete the data
        was_deleted = db.delete(user_key)
        print(f"Attempted to delete key '{user_key}'. Success: {was_deleted}")

        # 5. Verify it's gone
        retrieved_again = db.get(user_key)
        print(f"Data after deletion: {retrieved_again}")

    print("✅ Database connection closed.")


if __name__ == "__main__":
    main()