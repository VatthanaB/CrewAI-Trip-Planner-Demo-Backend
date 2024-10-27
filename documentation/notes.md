poetry env list : to get list of install dependencies

poetry shell : to start environnement python

---

### Step 1: Install Poetry

If you haven’t installed Poetry yet, use the following command in your terminal to do so:

**For Mac/Linux:**

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

**For Windows:**

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

To verify that Poetry was installed successfully, run:

```bash
poetry --version
```

This should display the installed version of Poetry.

---

### Step 2: Navigate to Your Project Directory

Open your terminal and navigate to the directory where your project is located. Use the `cd` command:

```bash
cd /path/to/your/project
```

Replace `/path/to/your/project` with the actual path to your project directory.

---

### Step 3: Start a Poetry Shell

Once you're in your project directory, start a Poetry shell to activate the virtual environment:

```bash
poetry shell
```

This activates a virtual environment specific to your project. You’ll see your terminal prompt change to reflect the activated environment.

---

### Step 4: Install Dependencies

If your project has a `pyproject.toml` file that lists dependencies, you can install them with the following command:

```bash
poetry install
```

This command will install all the dependencies specified in your project.

---

### Step 5: Update Python Interpreter in Visual Studio Code

To run and debug your project properly, you need to ensure that VS Code is using the correct Python interpreter (the one created by Poetry). Here’s how to update the interpreter:

1. **Open Visual Studio Code:**

   - Launch Visual Studio Code and open your project directory.

2. **Open the Command Palette:**

   - Press `Cmd + Shift + P` on Mac (or `Ctrl + Shift + P` on Windows/Linux).
   - In the Command Palette, type `Python: Select Interpreter` and choose it from the dropdown menu.

3. **Select Your Poetry Interpreter:**

   - VS Code will show a list of available Python interpreters.
   - Look for the interpreter located inside your `.venv` or `poetry` environment. It should look like this: `.venv/bin/python` or something similar (Poetry creates a virtual environment for your project).

4. **Manually Add the Interpreter (If Not Listed):**
   - If you can’t find the interpreter in the list, you can manually add it:
     - Open the Command Palette (`Cmd + Shift + P` or `Ctrl + Shift + P`).
     - Type `Python: Select Interpreter` again and select it.
     - Click on **Enter interpreter path**.
     - Choose **Find** and navigate to the `python` executable inside your virtual environment (created by Poetry), usually found at `.venv/bin/python` (Mac/Linux) or `.venv/Scripts/python.exe` (Windows).

---

### Step 6: Run Your Project

Now that your environment and interpreter are set up, you can run your project directly within Visual Studio Code:

1. **Open the Integrated Terminal in VS Code:**
   - Go to the terminal menu and select **Terminal > New Terminal**.
2. **Run Your Project:**
   - In the terminal, run your project’s main file:
     ```bash
     python main.py
     ```

Make sure that your `main.py` file contains the entry point for your project (or specify the correct file to run if it’s named differently).

---

### Summary:

1. Install Poetry.
2. Navigate to your project directory.
3. Start a Poetry shell to activate the virtual environment.
4. Install dependencies with `poetry install`.
5. Update the Python interpreter in Visual Studio Code.
6. Run your project using `python main.py` in VS Code's terminal.

This setup will ensure you're using Poetry’s virtual environment correctly and that Visual Studio Code is aligned with your project’s interpreter settings.
