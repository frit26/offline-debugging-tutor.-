# Offline Debugging Tutor — Android MVP

A beginner-friendly Kivy application for Android. The current MVP includes a code editor, offline static diagnostics, a small explanation library, and progressive hints. It deliberately **does not execute submitted code**. It has no network permissions and no AI model bundled yet.

## Included files

- `main.py` — Kivy mobile UI
- `diagnostics.py` — offline rule-based diagnostic engine
- `tests/test_diagnostics.py` — basic unit tests
- `buildozer.spec` — Android build configuration

## 1. Test the diagnostic engine on Windows

Install Python 3.11 or another supported Python 3 version from https://www.python.org/downloads/windows/ . During installation, select **Add Python to PATH**.

Open PowerShell in this folder and run:

```powershell
py -m unittest discover -s tests -v
```

To preview the UI on Windows, install Kivy in a virtual environment:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install kivy
python main.py
```

## 2. Build an APK from Windows using WSL2 + Ubuntu

Buildozer's Android packaging workflow runs on Linux/macOS; on Windows use WSL2 with Ubuntu. Official docs: https://kivy.org/doc/stable/guide/packaging-android.html and https://buildozer.readthedocs.io/en/latest/installation/ .

1. Install WSL2 and Ubuntu from Microsoft's instructions: https://learn.microsoft.com/windows/wsl/install . Restart if requested.
2. Open the **Ubuntu** app, then install build dependencies:

```bash
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip python3-venv \
  autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev \
  libtinfo6 cmake libffi-dev libssl-dev automake autopoint gettext
```

3. Keep the project in the Linux filesystem (not `/mnt/c`) for the build. One simple method is to copy the extracted project folder into Ubuntu's home directory using File Explorer at `\\wsl$\Ubuntu\home\YOUR_LINUX_USERNAME\`.
4. In Ubuntu, enter the project folder and set up a virtual environment:

```bash
cd ~/offline_debugging_tutor
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install buildozer
```

5. Build the debug APK:

```bash
buildozer -v android debug
```

The first build downloads Android build tools and may take a while. When it succeeds, look for the APK in the project's `bin/` folder.

## 3. Install on your Android phone

- Copy the generated `.apk` from `bin/` to your phone (USB cable or another file transfer method).
- Open the APK on the phone and permit installation from that source if Android asks.
- Install and test in airplane mode to verify offline operation.

If using ADB, enable Developer options and USB debugging on the phone, install Android Platform Tools on Windows, then run `adb devices` and `adb install path-to-apk.apk` from PowerShell.

## Important limitations and research notes

- This is a starting MVP, not a validated final research instrument.
- Syntax checks are exact for parse errors; name/type/index checks are limited heuristics and can produce false positives or miss errors.
- The application does not execute user code. This is intentional for safety and simplicity; adding safe execution on Android requires a separate design and testing.
- The optional local AI model is not integrated in this first build. Integrate it only after measuring app size, RAM use, inference speed, and output reliability on the target phone. Do not claim AI features are implemented until tested.
- “Verified explanations” currently means predefined explanations are returned from the local rule library. For the thesis, document how the explanations and each diagnostic test case were reviewed.
- Change `package.domain` to a namespace you control before distribution. APK signing and store publication are separate steps.
