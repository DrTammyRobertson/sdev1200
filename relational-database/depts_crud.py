import sqlite3

# Globals for the minimum and maximum menu items
MIN_MENU_ITEM = 1
MAX_MENU_ITEM = 6

# Main function
def main():
    # Menu choice
    choice = 0

    # Connect to the database.
    conn = sqlite3.connect('student_info.db')

    # Get a database cursor.
    cur = conn.cursor()

    # Enable Foreign Key Enforcement.
    cur.execute('PRAGMA foreign_keys=ON')

    # Get the user's menu choice.
    while choice != MAX_MENU_ITEM:
        choice = get_menu_choice()
        execute_choice(choice, cur)
    
    # Commit the changes
    conn.commit()

    # Close the connection.
    conn.close()

# The display_menu function displays a menu.
def display_menu():
    print('                          MENU')
    print('--------------------------------------------------------')
    print('1 - Display All')
    print('2 - Create a New Department')
    print('3 - Read a Department')
    print('4 - Update a Department')
    print('5 - Delete a Department')
    print('6 - EXIT')

# The get_menu_choice function displays the menu and gets the user's choice.
def get_menu_choice():
    display_menu()
    choice = int(input('Enter your choice: '))
    # Validate the choice.
    while choice < MIN_MENU_ITEM or choice > MAX_MENU_ITEM:
        choice = int(input('Enter a valid choice: '))
    return choice

# Perform the action that the user selected.
def execute_choice(choice, cur):
    if choice == 1:
        display_all(cur)
    elif choice == 2:
        create_row(cur)
    elif choice == 3:
        read_row(cur)
    elif choice == 4:
        update_row(cur)
    elif choice == 5:
        delete_row(cur)

# Display all the database rows.
def display_all(cur):
    # Get all the majors.
    cur.execute('SELECT DeptName FROM Departments ORDER BY DeptName')

    # Fetch the results.
    results = cur.fetchall()

    # Display the results.
    print()
    for row in results:
        print(f'{row[0]}')
    print()

# Create a new row in the database.
def create_row(cur):
    # Get the name of the new department.
    name = input('Name of Department: ')

    # Insert into the database.
    cur.execute('''INSERT INTO Departments (DeptName)
                   VALUES (?)''', (name,))
    
    # Confirm the insertion.
    print('New department added.\n')

# Read a row. (Search by department name.)
def read_row(cur):
    # Get the name to search for.
    name = input('Department to search for: ')

    # Insert the % symbols before and after the name.
    name = '%' + name + '%'

    # Search for a row containing the name.
    cur.execute('''SELECT DeptName FROM Departments
                   WHERE DeptName LIKE ?''', (name,))
    
    # Fetch the results.
    results = cur.fetchall()

    if len(results) > 0:
        for row in results:
            print(f'{row[0]}')
        print()
    else:
        print('Not found.\n')

# Update an existing row.
def update_row(cur):
    # Get the existing name of the department.
    name = input('Department to search for: ')

    # Insert the % symbols before and after the name.
    name = '%' + name + '%'

    # Search for a row containing the name.
    cur.execute('''SELECT DeptID, DeptName FROM Departments
                   WHERE DeptName LIKE ?''', (name,))
    
    # Fetch the results.
    results = cur.fetchall()

    if len(results) > 0:
        print(f'{"ID":3} {"Name":20}')
        for row in results:
            print(f'{row[0]:<3} {row[1]:20}')
        id = int(input('Enter the ID of the department you wish to update: '))
        if contains_id(results, id):
            new_name = input('Enter the new department name: ')
            cur.execute('''UPDATE Departments SET DeptName = ?
                           WHERE DeptID == ?''', (new_name, id))
            print('Entry updated.\n')
        else:
            print('Not a valid ID.')
        print()
    else:
        print('Not found.\n')

# Delete an existing row.
def delete_row(cur):
    # Get the department name.
    name = input('Department to search for: ')

    # Insert the % symbols before and after the name.
    name = '%' + name + '%'

    # Search for a row containing the department name.
    cur.execute('''SELECT DeptID, DeptName FROM Departments
                   WHERE DeptName LIKE ?''', (name,))
    
    # Fetch the results.
    results = cur.fetchall()

    if len(results) > 0:
        print(f'{"ID":3} {"Name":20}')
        for row in results:
            print(f'{row[0]:<3} {row[1]:20}')
        id = int(input('Enter the ID of the department you wish to delete: '))
        if contains_id(results, id):
            r_u_sure = input('Are you sure? (y/n): ')
            if (r_u_sure == 'y' or r_u_sure == 'Y'):
                cur.execute('DELETE FROM Departments WHERE DeptID == ?', (id,))
                print('Department deleted.\n')
        else:
            print('Not a valid ID.')
        print()
    else:
        print('Not found.\n')

# The contains_id function returns True if the id is in the results list.
def contains_id(results, id):
    status = False
    for row in results:
        if row[0] == id:
            status = True
    return status

# Execute the main function.
if __name__ == '__main__':
    main()