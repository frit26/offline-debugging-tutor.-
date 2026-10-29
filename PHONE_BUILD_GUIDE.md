# Build the Offline Debugging Tutor APK using only an Android phone

This project is an early offline MVP. It uses Kivy and rule-based diagnostics. It does not yet include a local AI model and does not execute submitted code.

## What you need
- Android phone with a browser
- GitHub account
- Internet connection for uploading source and building the APK in GitHub Actions

## A. Download and inspect the source
1. Download `offline_debugging_tutor_phone_build.zip` from this chat and extract it with your phone's Files app or a ZIP utility.
2. Keep the folder structure intact, especially `.github/workflows/build-android.yml`.

## B. Create a GitHub repository from your phone
1. Open https://github.com/new in your phone browser and sign in.
2. Create a repository named `offline-debugging-tutor`. For easiest setup, choose Public only if you are comfortable making the source public; otherwise choose Private.
3. Open the empty repository and use **Add file → Upload files** in the browser. If the mobile layout does not show this, enable **Desktop site** in your browser.
4. Upload the project files and folders from the extracted ZIP. Make sure `.github/workflows/build-android.yml` is included. GitHub's browser uploader can be awkward for nested folders on mobile; if it cannot upload the folder structure correctly, use GitHub's web editor to create the workflow file and add the other files, or use a cloud development environment.
5. Commit the uploaded files to the `main` branch.

## C. Run the cloud APK build
1. In your repository, open the **Actions** tab.
2. Select **Build Android APK**.
3. Tap **Run workflow** if it has not started automatically after the commit.
4. Open the running workflow and wait for it to finish. The first build may take several minutes and can fail if a dependency or Android build tool changes.
5. If successful, scroll to **Artifacts** and download `offline-debugging-tutor-debug-apk`.
6. Extract the downloaded artifact ZIP. It should contain the `.apk` file.

## D. Install and test
1. Tap the APK on your phone to install it. Android may ask you to allow installation from the browser or file manager; only proceed if you trust the file you built.
2. Open the app and test the sample code.
3. Turn on Airplane mode and repeat the test to confirm core diagnostics work offline.

## Troubleshooting
- If Actions fails, open the failed step and copy the last 30–50 lines of its log; use those lines to troubleshoot.
- Do not share GitHub passwords or access tokens.
- The APK from this workflow is a debug build for testing, not a Play Store release.
- GitHub Actions usage limits apply. Private repositories have account-dependent limits.
- Before distributing publicly, review the code, test on real devices, update `package.domain` in `buildozer.spec` to a namespace you control, and consider signing/release requirements.
