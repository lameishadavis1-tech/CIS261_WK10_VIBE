"""Student Grade Calculator."""

FILE_NAME = "student_grades.txt"


class ExitProgram(Exception):
	"""Raised when the user presses Escape or chooses to exit."""


def calculate_average(test1, test2, test3):
	"""Return the average of three test scores."""
	return (test1 + test2 + test3) / 3


def calculate_grade(average):
	"""Return a letter grade for an average score."""
	if average >= 90:
		return "A"
	if average >= 80:
		return "B"
	if average >= 70:
		return "C"
	if average >= 60:
		return "D"
	return "F"


def get_input(prompt):
	"""Read input and allow Escape to exit from any prompt."""
	try:
		value = input(prompt)
	except (EOFError, KeyboardInterrupt):
		raise ExitProgram
	if value == "\x1b":
		raise ExitProgram
	return value.strip()


def get_score(prompt):
	"""Prompt for a test score between 0 and 100."""
	while True:
		value = get_input(prompt)
		try:
			score = float(value)
			if 0 <= score <= 100:
				return score
			print("Please enter a score from 0 to 100.")
		except ValueError:
			print("Please enter a valid number.")


def add_student(students):
	"""Prompt for and add one student record."""
	print("\nAdd Student (press ESC at any prompt to exit)")
	name = get_input("Student name: ")
	while not name:
		print("Student name cannot be blank.")
		name = get_input("Student name: ")

	student_id = get_input("Student ID: ")
	while not student_id:
		print("Student ID cannot be blank.")
		student_id = get_input("Student ID: ")

	test1 = get_score("Test 1 score: ")
	test2 = get_score("Test 2 score: ")
	test3 = get_score("Test 3 score: ")
	average = calculate_average(test1, test2, test3)
	students.append({
		"name": name,
		"id": student_id,
		"test1": test1,
		"test2": test2,
		"test3": test3,
		"average": average,
		"grade": calculate_grade(average),
	})
	print(f"{name} was added with an average of {average:.2f} ({calculate_grade(average)}).")


def display_students(students):
	"""Display all student records in a formatted table."""
	if not students:
		print("\nNo student records to display.")
		return

	print("\nStudent Records")
	header = (
		f"{'Name':<20} {'ID':<14} {'Test 1':>8} {'Test 2':>8} "
		f"{'Test 3':>8} {'Average':>9} {'Grade':>6}"
	)
	print(header)
	print("-" * len(header))
	for student in students:
		print(
			f"{student['name'][:20]:<20} {student['id'][:14]:<14} "
			f"{student['test1']:>8.2f} {student['test2']:>8.2f} "
			f"{student['test3']:>8.2f} {student['average']:>9.2f} "
			f"{student['grade']:>6}"
		)


def display_statistics(students):
	"""Display highest, lowest, and class average scores."""
	if not students:
		print("\nNo student records available for statistics.")
		return

	averages = [student["average"] for student in students]
	highest = max(averages)
	lowest = min(averages)
	class_average = sum(averages) / len(averages)
	print("\nClass Statistics")
	print(f"Highest average: {highest:.2f}")
	print(f"Lowest average:  {lowest:.2f}")
	print(f"Class average:   {class_average:.2f}")


def search_student(students):
	"""Search for and display students by name, ignoring case."""
	search_name = get_input("\nEnter a student name to search: ").lower()
	matches = [student for student in students if search_name in student["name"].lower()]
	if matches:
		display_students(matches)
	else:
		print("No students found with that name.")


def save_students(students, filename=FILE_NAME):
	"""Save student records in the required pipe-delimited format."""
	try:
		with open(filename, "w", encoding="utf-8") as file:
			for student in students:
				file.write(
					f"{student['name']}|{student['id']}|{student['test1']:.2f}|"
					f"{student['test2']:.2f}|{student['test3']:.2f}|"
					f"{student['average']:.2f}|{student['grade']}\n"
				)
		return True
	except OSError as error:
		print(f"Unable to save student records: {error}")
		return False


def load_students(filename=FILE_NAME):
	"""Load student records, skipping malformed lines with a clear message."""
	students = []
	try:
		with open(filename, "r", encoding="utf-8") as file:
			for line_number, line in enumerate(file, start=1):
				fields = line.rstrip("\n").split("|")
				if len(fields) != 7:
					print(f"Skipping invalid record on line {line_number}.")
					continue
				try:
					test1, test2, test3 = (float(fields[index]) for index in (2, 3, 4))
					average = calculate_average(test1, test2, test3)
					students.append({
						"name": fields[0],
						"id": fields[1],
						"test1": test1,
						"test2": test2,
						"test3": test3,
						"average": average,
						"grade": calculate_grade(average),
					})
				except ValueError:
					print(f"Skipping invalid scores on line {line_number}.")
	except FileNotFoundError:
		return students
	except OSError as error:
		print(f"Unable to load student records: {error}")
	return students


def display_menu():
	"""Display the main menu."""
	print("\nStudent Grade Calculator")
	print("1. Add a student")
	print("2. Display all students")
	print("3. Display class statistics")
	print("4. Search for a student")
	print("5. Save records")
	print("E. Exit (or press ESC)")


def main():
	"""Run the Student Grade Calculator menu."""
	students = load_students()
	if students:
		print(f"Loaded {len(students)} student record(s).")
	else:
		print("No saved student records found.")

	try:
		while True:
			display_menu()
			choice = get_input("Choose an option: ").lower()
			if choice == "1":
				add_student(students)
				save_students(students)
			elif choice == "2":
				display_students(students)
			elif choice == "3":
				display_statistics(students)
			elif choice == "4":
				search_student(students)
			elif choice == "5":
				if save_students(students):
					print("Student records saved successfully.")
			elif choice in ("e", "exit"):
				raise ExitProgram
			else:
				print("Invalid choice. Please select an option from the menu.")
	except ExitProgram:
		save_students(students)
		print("\nStudent records saved. Goodbye!")


if __name__ == "__main__":
	main()