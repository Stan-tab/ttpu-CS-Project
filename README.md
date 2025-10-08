## 📚 Setup and Running the Bot

This guide will walk you through the necessary steps to set up and run the bot using **PostgreSQL** and **Python 3.10**.

---

## 💻 Prerequisites

Before starting, ensure you have the following installed on your system:

1.  **PostgreSQL**: You'll need an active PostgreSQL server to connect to.
2.  **Python 3.10** (or a compatible version): The project is built for this version.

---

## 🛠️ Installation and Configuration

Follow these steps to get the project ready:

### 1. Repository Access

First, you need to obtain the bot's repository. Assuming you have access to the repository, copy or clone it to your local machine.

### 2. Environment File

Create a file named **`.env`** in the root directory of the project. This file will store sensitive configuration details. It must contain the following two lines:

#### DATABASE = your_postgres_connection_string\
#### API_TOKEN = your_bot_token_here


* Replace `your_postgres_connection_string` with the connection string for your PostgreSQL database (e.g., `postgresql://user:password@host:port/database_name`).
* Replace `your_bot_token_here` with the actual token for your bot.

### 3. Virtual Environment Setup

It's highly recommended to use a **virtual environment** to manage dependencies.

1.  **Create the environment**: Run the following command in your terminal from the project's root directory:
    ```bash
    python -m venv venv
    ```
    This command creates a folder named `venv` containing a isolated Python interpreter and necessary tools.

2.  **Activate the environment**:
    * **On Linux/macOS**:
        ```bash
        source venv/bin/activate
        ```
    * **On Windows (Command Prompt)**:
        ```bash
        venv\Scripts\activate.bat
        ```
    * **On Windows (PowerShell)**:
        ```bash
        venv\Scripts\Activate.ps1
        ```

3.  **Install dependencies**: Once the virtual environment is active, you'll need to install the required Python packages (often listed in a `requirements.txt` file):
    ```bash
    pip install -r requirements.txt
    ```

---

## ▶️ Running the Bot

With all preparations complete, you can now start the bot.

1.  Ensure your virtual environment is **active** (as per Step 3 above).
2.  Only for first run use:
    ```bash
    python dbPeewee/schema.py
    ```
3.  Execute the main application file:
    ```bash
    python main.py
    ```

The bot should now start running and connect to your PostgreSQL database.
