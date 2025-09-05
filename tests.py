from functions import get_file_content, get_files_info

def test_get_files_info():
    test_cases = ["main.py", "pkg/calculator.py", "/bin/cat", "pkg/does_not_exist.py"]
    for test_case in test_cases:
        print(f'Results for {test_case}:')
        print(get_file_content.get_file_content("calculator", test_case))
        print()
if __name__ == "__main__":
    test_get_files_info()