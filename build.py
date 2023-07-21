import os
import zipfile


def make_zip(file_name):
    with zipfile.ZipFile(
        os.path.join(path := os.path.abspath("dist/"), file_name), "w"
    ) as zip_file:
        zip_file.write("dist/main.exe", "main.exe")
        for root, _, files in os.walk("assets\\"):
            for file in files:
                zip_file.write(os.path.join(root, file))


os.system("black .")
os.system("isort .")

os.system("python311 -m nuitka --onefile --output-dir=dist main.py")
make_zip("win_x64.zip")

os.system("python38 -m nuitka --onefile --output-dir=dist --remove-output main.py")
make_zip("win_x86_[COMPATIBILITY-VERSION].zip")

os.remove("dist/main.exe")
