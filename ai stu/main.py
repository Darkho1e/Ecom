# Ex 1: Print numbers from 12 to 24
for i in range(12, 25):
    print(i)

# Ex 2: Print odd numbers from 7 to 31
for i in range(7, 32, 2):
    print(i)

# Ex 3: Print even numbers from 10 to -20
for i in range(10, -21, -2):
    print(i)

# Ex 4: FizzBuzz
for i in range(1, 46):
    if i % 3 == 0 and i % 5 == 0:
        print("FizzBuzz")
    elif i % 3 == 0:
        print("Fizz")
    elif i % 5 == 0:
        print("Buzz")
    else:
        print(i)

# Ex 5: Sum of an array without sum()
def sum_array(arr):
    total = 0
    for num in arr:
        total += num
    return total

numbers = [1, 13, 22, 123, 49, 34, 5, 24, 57, 45]
print(sum_array(numbers))

# Ex 6: Student object manipulations
students = [
    {"id": 1, "first_name": "Aviv", "last_name": "Cohen", "age": 31, "country": "Israel", "city": "Tel Aviv"},
    {"id": 2, "first_name": "Yael", "last_name": "Levi", "age": 30, "country": "Israel", "city": "Jerusalem"}
]

def remove_property(students, prop):
    for student in students:
        if prop in student:
            del student[prop]

def print_students(students):
    for student in students:
        print(student)

def sort_by_age(students):
    return sorted(students, key=lambda x: x['age'], reverse=True)

print_students(students)
remove_property(students, 'city')
print_students(students)
print(sort_by_age(students))

# Ex 7: Pets array
# Ex 7: Pets array
our_pets = [
    {"animal_type": "cat", "names": ["Mitzi", "Shemesh", "Pitsi"]},
    {"animal_type": "dog", "names": ["Rexi", "Bobi", "Jack"]}
]

def print_cats(pets):
    for pet in pets:
        if pet['animal_type'] == 'cat':
            print(pet)

def print_animal_names(pets, animal_type):
    for pet in pets:
        if pet['animal_type'] == animal_type:
            print(pet['names'])

def add_name_to_all(pets, name):
    for pet in pets:
        if name not in pet['names']:
            pet['names'].append(name)

print_cats(our_pets)
print_animal_names(our_pets, "dog")
add_name_to_all(our_pets, "Lucky")
print(our_pets)

# Ex 8: Student object manipulations
student = {'name': 'Noam', 'age': 22, 'hobbies': ['reading', 'games', 'coding']}

def print_student_data(student):
    for key, value in student.items():
        print(f"{key}: {value}")

def add_hobby(student, hobby):
    if hobby not in student['hobbies']:
        student['hobbies'].append(hobby)

def remove_hobby(student, hobby):
    if hobby in student['hobbies']:
        student['hobbies'].remove(hobby)

student['family_name'] = 'Doe'
print_student_data(student)

# Ex 9: Print 2D array
matrix = [
    [1, 2],
    [3, 4],
    [5, 6]
]
def print_matrix(matrix):
    for row in matrix:
        for num in row:
            print(num, end=' ')
    print()

print_matrix(matrix)

# Ex 10: Count zeros in 2D matrix
matrix_zeros = [
    [0,1,1],
    [0,1,0],
    [1,0,0]
]
def zero_count(matrix):
    count = 0
    for row in matrix:
        for num in row:
            if num == 0:
                count += 1
    return count

print(zero_count(matrix_zeros))

# Ex 11: Find duplicates in array
def find_dup(arr):
    seen = set()
    duplicates = set()
    for num in arr:
        if num in seen:
            duplicates.add(num)
        seen.add(num)
    return list(duplicates)

print(find_dup([4,2,34,4,1,12,1,4]))

# Ex 12: Reverse array without reverse()
def reverse_array(arr):
    rev_arr = []
    for i in range(len(arr) - 1, -1, -1):
        rev_arr.append(arr[i])
    return rev_arr

print(reverse_array([43, "what", 9, True, "cannot", False, "be", 3, True]))

# Ex 13: Sum of two arrays
def sum_arrays(arr1, arr2):
    return [arr1[i] + arr2[i] for i in range(len(arr1))]

print(sum_arrays([4, 6, 7], [8, 1, 9]))

# Ex 14: Palindrome check
def is_palindrome(string):
    return string.replace(" ", "").lower() == string.replace(" ", "").lower()[::-1]

print(is_palindrome("racecar"))
print(is_palindrome("Java"))

# Ex 15: While loop doubling counter
counter = 1
while counter < 100:
    print(counter)
    counter *= 2

# Ex 16: While loop halving counter
counter = 900000
while counter > 50:
    print(counter)
    counter //= 2

# Ex 17: Find duplicates using while loop

def find_string_duplicates(arr):
    seen = set()
    duplicates = []
    i = 0
    while i < len(arr):
        if arr[i] in seen and arr[i] not in duplicates:
            duplicates.append(arr[i])
        seen.add(arr[i])
        i += 1
    return duplicates
names = ["Aviv", "Yossef", "Chani", "Aviv", "David", "Yossef"]
print(find_string_duplicates(names))

# Ex 18: Remove duplicates using while loop
def remove_duplicates(arr):
    seen = set()
    unique = []
    i = 0
    while i < len(arr):
        if arr[i] not in seen:
            seen.add(arr[i])
            unique.append(arr[i])
        i += 1
    return unique
print(remove_duplicates(names))

# Ex 19: Remove duplicates while skipping 'Pete'
def remove_duplicates_skip_pete(arr):
    seen = set()
    unique = []
    i = 0
    while i < len(arr):
        if arr[i] != 'Pete' and arr[i] not in seen:
            seen.add(arr[i])
            unique.append(arr[i])
        i += 1
    return unique
names_with_pete = ["Noam", "David", "Pete", "Daniel", "David", "Pete", "Daniel", "Avi"]
print(remove_duplicates_skip_pete(names_with_pete))

# Ex 20: Find first duplicate index in boolean array
def find_boolean_duplicate(arr):
    i = 1
    while i < len(arr):
        if arr[i] == arr[i - 1]:
            return i
        i += 1
    return -1
print(find_boolean_duplicate([True, False, False, True, True, False]))
print(find_boolean_duplicate([True, False, True, False, True, True]))
print(find_boolean_duplicate([True, False, True, False, True, False]))

# Ex 21: User input validation
def get_valid_input():
    while True:
        name = input("Enter full name: ")
        if len(name.split()) == 2:
            break
        print("Invalid name. Please enter first and last name.")

    while True:
        try:
            age = int(input("Enter age: "))
            if 1 <= age <= 130:
                break
        except ValueError:
            pass
        print("Invalid age. Please enter a number between 1-130.")

    while True:
        email = input("Enter email: ")
        if "@" in email:
            break
        print("Invalid email. Must contain '@'.")

    print("Valid input received.")

get_valid_input()