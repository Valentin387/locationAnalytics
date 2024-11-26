# locationAnalytics
Simple python project to fetch and study data from a mongo db database. Generate informs to get insights

# Project Setup

## Setting Up the Project

### Step 1: Create a `.env` File

It is recommended to use a virtual environment to manage the project's dependencies. To create and activate a virtual environment, follow these steps:

1. **Create the virtual environment:**

   On Windows:
   ```bash
   python -m venv venv

That will create a `.env` file in the root of the project. Then, add the following content:

```env
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_SERVER=your_cluster_url
DB_NAME=your_database_name
```

Make sure to replace the placeholders with your actual MongoDB credentials. Also, ensure the .env file is not committed by adding it to your .gitignore:

### Step 2: Install Dependencies
To install the required dependencies, run:

```
pip install -r requirements.txt
```

