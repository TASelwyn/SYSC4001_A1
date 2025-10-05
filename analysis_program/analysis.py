import os

folder_path = "../testcases"

if __name__ == "__main__":
    print("Analysis")

    for file in os.listdir(folder_path):
        print(file)


