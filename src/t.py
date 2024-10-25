import os


# ruff: noqa: E501


def main():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        text = input("text: ")
        os.system("cls" if os.name == "nt" else "clear")
        # print(text.replace('COMMONLY_', '').replace("_", " ").title().replace(" ", "_"))
        print(text.upper().replace(" ", "_"))
        # print(text.lower().replace(" ", "_"))
        input()


if __name__ == "__main__":
    try:
        os.system("cls" if os.name == "nt" else "clear")
        main()

    except KeyboardInterrupt:
        exit()
