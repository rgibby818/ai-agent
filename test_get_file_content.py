from functions.get_file_content import get_file_content


def test() -> None:

    result = get_file_content("calculator", "lorem.txt")
    print("Running test_get_file_content:\n")
    print('Result for "calculator/lorem.txt":')
    if len(result) == 10000 + len('[...File "{file_path}" truncated at 10000 characters]'):
        print("Passed 10,000 char test")
    print("-----------------------------------------------------------------------")

    result = get_file_content("calculator", "main.py")
    print('Result for "calculator/main.py":\n')
    print(result)
    print("-----------------------------------------------------------------------")

    result = get_file_content("calculator", "pkg/calculator.py")
    print('Result for "pkg/calculator":\n')
    print(result)
    print("-----------------------------------------------------------------------")

    result = get_file_content("calculator", "/bin/cat")
    print('Result for "calculator/bin/cat":\n')
    print(result)
    print("-----------------------------------------------------------------------")

    result = get_file_content("calculator", "pkg/does_not_exist.py")
    print('Result for "calculator/pkg/does_not_exist":\n')
    print(result)
    print("-----------------------------------------------------------------------")


if __name__ == "__main__":
    test()
