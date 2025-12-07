from functions.run_python_file import run_python_file


def test() -> None:
    result = run_python_file("calculator", "main.py")
    print('Result for "calculator/main.py":\n')
    print(result)
    print("-----------------------------------------------------------------------")

    result = run_python_file("calculator", "main.py", ["3 + 5"])
    print('Result for "calculator/main.py 3 + 5": \n')
    print(result)
    print("-----------------------------------------------------------------------")

    result = run_python_file("calculator", "tests.py")
    print('Result for "calculator/test": \n')
    print(result)
    print("-----------------------------------------------------------------------")

    result = run_python_file("calculator", "../main.py")
    print('Result for "calculator/../main.py":\n')
    print(result)
    print("-----------------------------------------------------------------------")

    result = run_python_file("calculator", "nonexistent.py")
    print('Result for "calculator/nonexist.py":\n')
    print(result)
    print("-----------------------------------------------------------------------")

    result = run_python_file("calculator", "lorem.txt")
    print('Result for "calculator/lorem.txt":\n')
    print(result)
    print("-----------------------------------------------------------------------")


if __name__ == "__main__":
    test()
