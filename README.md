# real-time-pump.fun-thx-recive
1. Install Required Packages
First, install the necessary Python packages using pip:

bash
코드 복사
pip install gql aiohttp python-dotenv
2. Set Up Environment Variables
To keep your API key secure, use environment variables.

a. Create a .env File
In the root directory of your project, create a file named .env and add your Bitquery API key:

env
코드 복사
BITQUERY_API_KEY=your_bitquery_api_key_here
b. Add .env to .gitignore
Ensure that the .env file is not pushed to GitHub by adding it to your .gitignore file. Create a .gitignore file in your project root (if it doesn't exist) and add the following line:

gitignore
코드 복사
# Ignore environment variables file
.env
Create the folder in your project directory:

bash
mkdir data
If you choose a different folder name, update the DATA_FOLDER variable in the script accordingly.

5. Initialize Git Repository and Push to GitHub
a. Initialize Git Repository
bash
git init
b. Add Files to Repository
bash
git add .
c. Commit Changes
bash
git commit -m "Initial commit with Bitquery subscription script"
d. Create a GitHub Repository
Go to GitHub and create a new repository.

e. Add Remote and Push
Replace yourusername and your-repo-name with your GitHub username and repository name.

bash
git remote add origin https://github.com/yourusername/your-repo-name.git
git branch -M main
git push -u origin main
