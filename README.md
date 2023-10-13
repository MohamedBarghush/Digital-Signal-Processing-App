# Digital-Signal-Processing-App
This simple python app is for the tasks of the Digital Signal Processing course in Computer Science ASU, Scientific Computing major

# Setup instructions
1- Clone the repo in the desired folder with this command
```
git clone "https://github.com/MohamedGamalBarghash/Digital-Signal-Processing-App"
```

2- Install the required libraries with this command
```
pip3 install -r .\requirements.txt
```

3- Run the app with the command
```
python3 '.\Task 1.py'
```

4- Enjoy!!!

# To deploy the app into an EXE on Mohamed Barghush's pc, run the command
```
pyinstaller --noconfirm --onefile --windowed --add-data "C:/Users/Cinos/AppData/Local/packages/PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0/localcache/local-packages/python311/site-packages/tkinterdnd2;tkinterdnd2/" ".\Task 1.py"
```