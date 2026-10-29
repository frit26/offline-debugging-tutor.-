[app]
title = Offline Debugging Tutor
package.name = offlinedebugtutor
package.domain = org.studentproject
source.dir = .
source.include_exts = py,txt,json,md
version = 0.1.0
requirements = python3,kivy
orientation = portrait
fullscreen = 0

# Keep permissions empty: this MVP requires no network or device permissions.
android.permissions =
android.api = 35
android.minapi = 23
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
