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
    print('2 - Create a New Student Record')
    print('3 - Read a Student Record')
    print('4 - Update a Student Record')
    print('5 - Delete a Student Record')
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

# Display all the student records.
def display_all(cur):
    # Get all the students.
    cur.execute('''SELECT   Students.StudentName, Departments.DeptName, Majors.MajorName
                   FROM     Students, Departments, Majors
                   WHERE    Students.DeptID == Departments.DeptID AND
                            Students.MajorID == Majors.MajorID
                   ORDER BY StudentName''')

    # Fetch the results.
    results = cur.fetchall()

    # Display the results.
    print()
    print(f'{"Name":25}{"Department":20}{"Major":15}')
    print('------------------------------------------------------------')
    for row in results:
        print(f'{row[0]:25}{row[1]:20}{row[2]:15}')
    print()

# Create a new row in the database.
def create_row(cur):
    # Get the student's info.
    name = input('Student Name: ')
    major = get_major(cur)
    dept = get_department(cur)

    # Insert into the database.
    cur.execute('''INSERT INTO Students (StudentName, MajorID, DeptID)
                   VALUES (?, ?, ?)''', (name, major, dept))
    
    # Confirm the insertion.
    print('New student added.\n')

# Get the student's major from a list of majors.
def get_major(cur):
    major_id = -1

    # Get all the majors from the Majors table.
    cur.execute('SELECT MajorID, MajorName FROM Majors')
    
    # Fetch the results.
    results = cur.fetchall()

    if len(results) > 0:
        print(f'{"ID":3} {"Major Name":20}')
        for row in results:
            print(f'{row[0]:<3} {row[1]:20}')
        major_id = int(input("Enter the ID of the student's major: "))
        while not contains_id(results, major_id):
            major_id = int(input('Invalid ID. Enter a valid ID: '))
    else:
        print('No Majors found.\n')
    return major_id

# Get the student's department from a list of departments.
def get_department(cur):
    dept_id = -1

    # Get all the departments from the Departments table.
    cur.execute('SELECT DeptID, DeptName FROM Departments')
    
    # Fetch the results.
    results = cur.fetchall()

    if len(results) > 0:
        print(f'{"ID":3} {"Department Name":20}')
        for row in results:
            print(f'{row[0]:<3} {row[1]:20}')
        dept_id = int(input("Enter the ID of the student's department: "))
        while not contains_id(results, dept_id):
            dept_id = int(input('Invalid ID. Enter a valid ID: '))
    else:
        print('No departments found.\n')
    return dept_id

# Read a row. (Search by student name.)
def read_row(cur):
    # Get the name to search for.
    name = input('Student to search for: ')

    # Insert the % symbols before and after the name.
    name = '%' + name + '%'

    # Search for the student.
    cur.execute('''SELECT   Students.StudentName, Departments.DeptName, Majors.MajorName
                   FROM     Students, Departments, Majors
                   WHERE    Students.StudentName LIKE ? AND
                            Students.DeptID == Departments.DeptID AND
                            Students.MajorID == Majors.MajorID
                   ORDER BY StudentName''', (name,))
    
    # Fetch the results.
    results = cur.fetchall()

    if len(results) > 0:
        print()
        print(f'{"Name":25}{"Department":20}{"Major":15}')
        print('------------------------------------------------------------')
        for row in results:
            print(f'{row[0]:25}{row[1]:20}{row[2]:15}')
        print()
    else:
        print('Not found.\n')

# Update an existing row.
def update_row(cur):
    # Get the name to search for.
    name = input('Student to search for: ')

    # Insert the % symbols before and after the name.
    name = '%' + name + '%'

    # Search for a row containing the name.
    cur.execute('''SELECT   Students.StudentID, Students.StudentName, Departments.DeptName, Majors.MajorName
                   FROM     Students, Departments, Majors
                   WHERE    Students.StudentName LIKE ? AND
                            Students.DeptID == Departments.DeptID AND
                            Students.MajorID == Majors.MajorID
                   ORDER BY StudentName''', (name,))
    
    # Fetch the results.
    results = cur.fetchall()

    if len(results) > 0:
        print()
        print(f'{"ID":<3}{"Name":25}{"Department":20}{"Major":15}')
        print('---------------------------------------------------------------')
        for row in results:
            print(f'{row[0]:<3}{row[1]:25}{row[2]:20}{row[3]:15}')
        id = int(input('Enter the ID of the student you wish to update: '))
        if contains_id(results, id):
            new_name = input('Enter the new student name: ')
            new_major = get_major(cur)
            new_dept = get_department(cur)
            cur.execute('''UPDATE Students SET StudentName = ?, MajorID = ?, DeptID = ?
                           WHERE StudentID == ?''', (new_name, new_major, new_dept, id))
            print('Entry updated.\n')
        else:
            print('Not a valid ID.')
        print()
    else:
        print('Not found.\n')

# Delete an existing row.
def delete_row(cur):
    # Get the student name.
    name = input('Student to search for: ')

    # Insert the % symbols before and after the name.
    name = '%' + name + '%'

    # Search for a row containing the name.
    cur.execute('''SELECT   Students.StudentID, Students.StudentName, Departments.DeptName, Majors.MajorName
                   FROM     Students, Departments, Majors
                   WHERE    Students.StudentName LIKE ? AND
                            Students.DeptID == Departments.DeptID AND
                            Students.MajorID == Majors.MajorID
                   ORDER BY StudentName''', (name,))
    
    # Fetch the results.
    results = cur.fetchall()

    if len(results) > 0:
        print()
        print(f'{"ID":<3}{"Name":25}{"Department":20}{"Major":15}')
        print('---------------------------------------------------------------')
        for row in results:
            print(f'{row[0]:<3}{row[1]:25}{row[2]:20}{row[3]:15}')
        id = int(input('Enter the ID of the student you wish to delete: '))
        if contains_id(results, id):
            r_u_sure = input('Are you sure? (y/n): ')
            if (r_u_sure == 'y' or r_u_sure == 'Y'):
                cur.execute('DELETE FROM Students WHERE StudentID == ?', (id,))
                print('Student deleted.\n')
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