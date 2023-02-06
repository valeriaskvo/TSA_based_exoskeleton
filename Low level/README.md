# ESP32 How to connect and upload your code

## Upload your code

**Step 1:** Install the rshell to you computer

```shell
pip3 install rshell
```

**Step 2:** Connect to ESP32

1. Usually the ESP32 board has the port `/dev/ttyUSB0`
2. Check the board port:

```shell
ls /dev/ttyUSB*
```

3. Connect to the board

```shell
rshell -p /dev/ttyUSB0 -b 115200
```

* If the process stopped into the step `Trying to connect to REPL ...`, try to push the button `reset` on a board, or
  try the command with `sudo`

**Step 3:** Upload the script(s) with `rshell`

* If you need upload only file `main.py`

```shell
cp path/to/main.py /pyboard/main.py
```

* If you need to upload many files

```shell
cp -r path/to/*.py /pyboard/
```

* If you need to upload many files with folder

```shell
mkdir /pyboard/<folder_name>
```

```shell
cp -r path/to/<folder_name>/*.py /pyboard/<folder_name>/
```

**Step 4:** Close the rshell

## Run your code

**Step 1:** Install **picocom**

```shell
sudo apt-get install picocom
```

**Step 2:** Open shell

```shell
sudo picocom /dev/ttyUSB0 -b 115200
```

**Step 3:** Run script
1. Run script: **ctrl+d**
2. Stop script: **ctrl+c**
3. Exit from shell: **ctrl+a** + **ctrl+q**