from flask import Flask, redirect, request, session, url_for, render_template, jsonify
from googleapiclient import discovery
from oauth2client import file, client, tools
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Google OAuth settings
SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly", "https://www.googleapis.com/auth/drive"]
CLIENT_SECRETS_FILE = "credentials.json"
CREDENTIALS_STORE = "storage.json"

def get_credentials():
    """Retrieve credentials using oauth2client."""
    store = file.Storage(CREDENTIALS_STORE)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRETS_FILE, SCOPES)
        credentials = tools.run_flow(flow, store)
    return credentials

@app.route("/")
def index():
    if not os.path.exists(CREDENTIALS_STORE):
        return redirect("/authorize")
    credentials = get_credentials()
    if not credentials:
        return redirect("/authorize")
    
    drive_service = discovery.build("drive", "v3", credentials=credentials)

    # Get the authenticated user's email address
    about = drive_service.about().get(fields="user(emailAddress)").execute()
    user_email = about.get("user", {}).get("emailAddress")

    # List files
    files = drive_service.files().list(
        pageSize=100,
        fields="files(id, name, shared, permissions, owners(emailAddress))"
    ).execute().get("files", [])

    # Prepare file data for the template
    file_data = []
    for file in files:
        # Check if the authenticated user is the owner
        is_owner = any(owner.get("emailAddress") == user_email for owner in file.get("owners", []))
        if not is_owner:
            continue  # Skip files where the user is not the owner

        file_name = file.get("name")
        file_id = file.get("id")
        is_shared = file.get("shared", False)
        is_public = any(perm.get("role") == "reader" and perm.get("type") == "anyone" for perm in file.get("permissions", []))

        file_data.append({
            "name": file_name,
            "id": file_id,
            "shared": is_shared,
            "public": is_public
        })

    return render_template("index.html", files=file_data)

    # return """
    #     <h1>Google Drive Sharing Feedback</h1>
    #     <a href="/check-sharing">Check File Sharing Settings</a>
    # """

@app.route("/authorize")
def authorize():
    flow = client.flow_from_clientsecrets(CLIENT_SECRETS_FILE, SCOPES, redirect_uri="http://localhost:5000/callback")
    auth_url = flow.step1_get_authorize_url()
    return redirect(auth_url)

@app.route("/callback")
def callback():
    flow = client.flow_from_clientsecrets(CLIENT_SECRETS_FILE, SCOPES, redirect_uri="http://localhost:5000/callback")
    credentials = flow.step2_exchange(request.args.get("code"))
    store = file.Storage(CREDENTIALS_STORE)
    store.put(credentials)
    return redirect("/")

@app.route("/check-sharing")
def check_sharing():
    credentials = get_credentials()
    if not credentials:
        return redirect("/authorize")

    drive_service = discovery.build("drive", "v3", credentials=credentials)

    # Get the authenticated user's email address
    about = drive_service.about().get(fields="user(emailAddress)").execute()
    user_email = about.get("user", {}).get("emailAddress")

    # List files
    files = drive_service.files().list(
        pageSize=100,
        fields="files(id, name, shared, permissions, owners(emailAddress))"
    ).execute().get("files", [])

    # Filter files where the authenticated user is the owner
    feedback = []
    for file in files:
        # Check if the authenticated user is the owner
        is_owner = any(owner.get("emailAddress") == user_email for owner in file.get("owners", []))
        if not is_owner:
            continue  # Skip files where the user is not the owner

        file_name = file.get("name")
        is_shared = file.get("shared", False)
        permissions = file.get("permissions", [])

        if is_shared:
            feedback.append(f"File '{file_name}' is shared.")
            for perm in permissions:
                if perm.get("role") == "reader" and perm.get("type") == "anyone":
                    feedback.append(f"  - Publicly accessible via link.")
        else:
            feedback.append(f"File '{file_name}' is not shared.")

    return "<br>".join(feedback)

@app.route("/remove-access")
def remove_access():
    file_id = request.args.get("fileId")
    permission_id = request.args.get("permissionId")
    credentials = get_credentials()
    drive_service = discovery.build("drive", "v3", credentials=credentials)
    drive_service.permissions().delete(fileId=file_id, permissionId=permission_id).execute()
    return jsonify({"status": "success"})

@app.route("/disable-link-sharing", methods=["POST"])
def disable_link_sharing():
    file_id = request.args.get("fileId")
    if not file_id:
        return jsonify({"status": "error", "message": "fileId is required"}), 400

    credentials = get_credentials()
    print(credentials)
    if not credentials:
        return jsonify({"status": "error", "message": "Authentication required"}), 401

    drive_service = discovery.build("drive", "v3", credentials=credentials)
    try:
        # Remove "anyoneWithLink" permission
        drive_service.permissions().delete(fileId=file_id, permissionId="anyoneWithLink").execute()
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # For testing only
    app.run(port=5000, debug=True)