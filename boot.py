from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import time

#==================== CONFIGURATION =====================
LOCAL_FOLDER_PATH = r"............" # Change this to your local folder path
GOOGLE_DRIVE_FOLDER_ID = "..........."  # Change this to your Drive folder ID
BATCH_SIZE = 5
WAIT_TIME_SECONDS = 120  # 2 minutes




def authenticate_drive():
    """Authenticate and create a Google Drive instance."""
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("mycreds.txt")
    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
    gauth.SaveCredentialsFile("mycreds.txt")
    return GoogleDrive(gauth)


def upload_file(drive, file_path):
    """Upload a single file to Google Drive."""
    try:
        file_name = os.path.basename(file_path)
        gfile = drive.CreateFile({
            'title': file_name,
            'parents': [{'id': GOOGLE_DRIVE_FOLDER_ID}]
        })
        gfile.SetContentFile(file_path)
        gfile.Upload()
        print(f"Uploaded: {file_name}")
    except Exception as e:
        print(f"Error uploading {os.path.basename(file_path)}: {e}")


def main():
    drive = authenticate_drive()
    txt_files = [os.path.join(LOCAL_FOLDER_PATH, f) for f in os.listdir(LOCAL_FOLDER_PATH) if
                 f.lower().endswith('.txt')]
    total_files = len(txt_files)
    if total_files == 0:
        print("No .txt files found in the specified folder.")
        return

    print(f"Found {total_files} .txt files to upload.")

    for i in range(0, total_files, BATCH_SIZE):
        batch = txt_files[i:i + BATCH_SIZE]
        for idx, file_path in enumerate(batch, start=1):
            print(f"Uploading file {i + idx} of {total_files}: {os.path.basename(file_path)}")
            upload_file(drive, file_path)
        if i + BATCH_SIZE < total_files:
            print(f"Batch complete, waiting {WAIT_TIME_SECONDS} seconds...")
            time.sleep(WAIT_TIME_SECONDS)

    print("All files uploaded successfully.")


if __name__ == "__main__":
    main()
