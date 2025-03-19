# Privacy Manager App  

## Overview  
The Privacy Manager app is a tool designed to simplify and streamline the process of privatizing files in Google Drive. By automating multi-step workflows and reducing cognitive load, the app helps users manage their file-sharing settings more efficiently, saving time and improving privacy practices.  

## Features  
- **Time Efficiency**: Reduces the time required to privatize files by an average of 5.75 times compared to the default Google Drive UI.  
- **User-Friendly Design**: Simplifies complex sharing settings into intuitive, single-click actions.  
- **Consistent Performance**: Delivers reliable results across all users, with tightly clustered task completion times.  

## How It Works  
1. **Authentication**: Users authenticate with their Google account to grant the app access to their Google Drive.  
2. **File Selection**: The app lists files owned by the user and identifies those with sharing enabled.  
3. **Privatization**: Users can disable link sharing or modify permissions with a single click.  

## Installation  
1. Clone the repository:  
   ```bash  
   git clone https://github.com/tcamou/privacy-nudger.git 
   ```  
2. Install dependencies:  
   ```bash  
   pip install Flask==2.3.2
    google-api-python-client==2.86.0
    google-auth==2.17.3
    google-auth-oauthlib==1.0.0
    google-auth-httplib2==0.1.0
   ```  
3. Set up Google API credentials:  
   - Enable the Google Drive API in the Google Cloud Console.  
   - Download the `credentials.json` file and place it in the project directory.  

## Usage  
1. Run the app:  
   ```bash  
   python app.py  
   ```  
2. Open your browser and navigate to `http://localhost:5000`.  
3. Authenticate with your Google account and follow the on-screen instructions to privatize files.  

## Future Work  
- Handle edge cases, such as shared folders and external file ownership.  
- Optimize for bulk operations and team-level permissions.  
- Expand functionality to include auditing and permission management features.  

## License  
This project is licensed under the GNU License. See the `LICENSE` file for details.  

## Contact  
For questions or feedback, please contact [tcamou@pdx.edu] or [adrian6@pdx.edu].  

---  
Thank you for using the Privacy Manager App!
