# Lab 05: NoSQL with MongoDB

The goal of this lab is to get you comfortable with NoSQL document databases using MongoDB. You will use the `mongosh` shell to create collections, insert and query documents, and then use PyMongo to build a small Python application that talks to MongoDB Atlas. Follow the steps below to complete two case studies that show how flexible, schema-free data stores power modern applications.

> **Note:** Review and adhere to the [coding best practices](https://github.com/ksiller/DS2022/blob/main/best-practices.md) where applicable when developing your scripts. Case Study 2 should follow the same scripting and Python practices you used in [Lab 03](https://github.com/ksiller/lab-03-scripting) and [Lab 04](https://github.com/ksiller/lab-04-sql): a shebang, environment variables for credentials, functions with docstrings, comments, logging, and an `if __name__ == "__main__":` block.

## Setup

### 1. MongoDB Atlas and `mongosh`

Before you begin, set up MongoDB Atlas and connect from your environment. Follow the [MongoDB Atlas setup instructions](https://github.com/ksiller/DS2022/blob/main/setup/mongodb.md): sign up for Atlas, add the required IP access list entries, get your connection string, and save `MONGODB_ATLAS_URL`, `MONGODB_ATLAS_USER`, and `MONGODB_ATLAS_PWD` in your `~/.bashrc` (or `~/.zshrc`). Install `mongosh` as described in the [mongosh install section](https://github.com/ksiller/DS2022/blob/main/setup/mongodb.md#install-the-mongosh-client-on-your-computer).

### 2. Fork and clone this repository

Fork this repository on GitHub (keep the default name): [https://github.com/ksiller/lab-05-nosql](https://github.com/ksiller/lab-05-nosql). Clone **your fork** to your own computer. Recommended location: `~/ds2022-fall-2026/lab-05-nosql`.

```bash
git clone https://github.com/YOUR_USERNAME/lab-05-nosql.git ~/ds2022-fall-2026/lab-05-nosql
cd ~/ds2022-fall-2026/lab-05-nosql
```

Do all of your work in that clone. Commit and push deliverables to your fork, then submit the URL of the fork (see [Submit your work](#submit-your-work)).

### 3. Python environment with `uv`

Case Study 2 uses a `uv` project, as in Lab 03 and Lab 04. Confirm that `uv` is installed (`uv --version`). If that command fails, install it by following [Installing uv](https://docs.astral.sh/uv/getting-started/installation/).

From the top-level directory of your clone, create the project and add PyMongo:

```bash
cd ~/ds2022-fall-2026/lab-05-nosql
uv init --name "nosql_lab" --description "NoSQL work for DS2022"
uv add pymongo
```

- `uv init` creates `pyproject.toml`, `.python-version`, and a package directory `src/nosql_lab/` (with `__init__.py`).
- `uv add pymongo` records `pymongo` in `pyproject.toml`, writes `uv.lock` with exact versions, and installs the package into `.venv/`. Do not edit `uv.lock` by hand.

This repository already includes a `.gitignore` that excludes `.venv/`, `.vscode/`, and secret files such as `.env`. Review that file, and leave those lines in place. **Do not commit `.venv/`**. On another computer, `uv sync` recreates the environment, including `.venv`, from `pyproject.toml` and `uv.lock`.

---

## Case Study 1: The Bookstore’s New Inventory System (mongosh)

A local bookstore owner has been struggling to track authors and books on spreadsheets. They’ve heard that document databases are great for semi-structured data and want to try MongoDB. They’ve recruited you to design a small “authors” collection and show them how to query it from the shell. No rigid tables—just documents that can grow over time.

You’ll use `mongosh` to create a database, add author documents with nested “bio” fields, run updates, and capture your commands in a script they can reuse.

### Create, query, and save the collection

1. Connect to MongoDB Atlas using `mongosh` and your Atlas credentials (see [Get Connection String](https://github.com/ksiller/DS2022/blob/main/setup/mongodb.md#3-get-connection-string-url) in the setup instructions).

2. Create a new database named `bookstore`. In MongoDB, you switch to (or create) a database with `use <dbname>`.

3. Insert the following document into the `authors` collection. Note the nested `bio` object with `short` and `long` fields. This is the kind of flexible structure document databases handle well.

```javascript
db.authors.insertOne({
  "name": "Jane Austen",
  "nationality": "British",
  "bio": {
    "short": "English novelist known for novels about the British landed gentry.",
    "long": "Jane Austen was an English novelist whose works critique and comment upon the British landed gentry at the end of the 18th century. Her most famous novels include Pride and Prejudice, Sense and Sensibility, and Emma, celebrated for their wit, social commentary, and masterful character development."
  }
})
```

4. Update that document to add a `birthday` field with an appropriate value (for example, `"1775-12-16"` or a date type). Use `updateOne` with a filter and `$set`.

5. Add four more author documents of your choice, using the same structure: `name`, `nationality`, `bio` (with nested `short` and `long`), and `birthday`. Vary nationalities so you can practice filtering. You can do this sequentially with `insertOne` or in bulk with `insertMany`.

6. Run a query that returns the total number of documents in `authors` (for example, `countDocuments()`).

7. Run a query that returns all documents where `nationality` is `"British"`, sorted by `name` in ascending order. Check your spelling (for example, `"British"`, not `"Bristish"`) so the filter matches.

8. In the `mongosh` shell, run `history()` to view your recent commands. Copy the commands from steps 2–7 above into one file so the bookstore owner can rerun them: switch to the database, insert the first author, update that document, insert four more authors, count the documents, and find British authors sorted by name.

   Create a file named `bookstore.js` in the top-level directory of your cloned repository with this structure:

```javascript
// Step 2: use database
// paste your use bookstore command here

// Step 3: insert first author
// paste your insertOne command here

// Step 4: update to add birthday
// paste your updateOne command here

// Step 5: insert four more authors
// paste your insertMany or insertOne commands here

// Step 6: total count
// paste your countDocuments() command here

// Step 7: British authors, sorted by name
// paste your find and sort command here
```

   Use comments so each section is clearly labeled. The owner does not need to run `history()`. They can run the pasted commands in order from `bookstore.js`.

**Success:** You’ve designed a small document model and used the MongoDB shell to create, update, query, and sort documents. Next, you’ll do the same kind of work from Python.

---

## Case Study 2: Bookstore Inventory from Python (PyMongo)

The bookstore owner is impressed by the shell demo. Now they want a simple Python script that connects to the same Atlas cluster, reads from the `bookstore` database, and prints a short report (for example, how many authors, and a list of names and nationalities). This way they can eventually hook scripts into their workflow or a small dashboard.

**Your task:** Write a Python script that uses PyMongo to connect to MongoDB Atlas, targets the `bookstore` database and `authors` collection from Case Study 1, and produces a small, readable report. Follow the scripting and Python best practices from Lab 03 and Lab 04.

### Step 1: Environment and dependencies

The `uv` project and `pymongo` dependency were created in [Setup](#3-python-environment-with-uv). If `import pymongo` fails, re-run `uv add pymongo` from the repository root.

Confirm `MONGODB_ATLAS_URL`, `MONGODB_ATLAS_USER`, and `MONGODB_ATLAS_PWD` are set in the shell you will use. If you just added them to `~/.bashrc` or `~/.zshrc`, load that file (`source ~/.bashrc` or `source ~/.zshrc`) before you run the script.

### Step 2: Write the script

Create `src/nosql_lab/bookstore_report.py` in the package directory created by `uv init --name "nosql_lab"`. The script should:

- Start with the shebang `#!/usr/bin/env python3`.
- Read `MONGODB_ATLAS_URL`, `MONGODB_ATLAS_USER`, and `MONGODB_ATLAS_PWD` with `os.getenv()`, as module-level variables below the imports (outside `main`), the same way Lab 03 reads `GITHUB_USER`. Do not hardcode credentials.
- Give every function a docstring, and add comments in the code.
- Use `logging` to report status (connection success and errors). `print` is fine inside `main` for the report itself.
- Wrap the code that opens, uses, and closes the MongoDB client in a `try`/`except` block, and close the client when you are done.
- Define a `main` function that:
  - Connects to MongoDB Atlas with `pymongo.MongoClient`, passing the connection URL and the username and password from the environment variables.
  - Selects the `bookstore` database and the `authors` collection.
  - Prints a short report that includes the total number of author documents and, for each author, at least the `name` and `nationality` (optionally `birthday` or `bio.short`). Format the output so it is easy to read: one line per author, or a few lines per author.
- Call `main()` from an `if __name__ == "__main__":` block so it runs only when the file is executed directly. See [class/03-scripting](https://github.com/ksiller/DS2022/blob/main/class/03-scripting/README.md) for how that guard works.

Run the script from the repository root with `uv run`, so Python uses the project environment. Confirm that it connects to Atlas and prints the report from the documents you added in Case Study 1:

```bash
uv run python src/nosql_lab/bookstore_report.py
```

**Hint:** Use `collection.count_documents({})` for the total count and `collection.find({})` (with an optional projection) to iterate over authors.

**Success:** You’ve connected to the same MongoDB data from Python and produced a simple report. That’s the same pattern used in larger systems: shell for ad hoc operations, Python (or another driver) for automation and applications.

---

## Learning Outcomes

By completing this lab, you have:

- Used the MongoDB shell (`mongosh`) to create a database and collection and to insert, update, and query documents.
- Practiced filtering and sorting documents and capturing shell commands in a script file.
- Created a reproducible Python environment with `uv` and installed PyMongo into it.
- Connected to MongoDB Atlas from Python with PyMongo and environment variables.
- Written a script that follows scripting best practices (shebang, docstrings, comments, logging, and an entry-point guard) and produces a report from a document collection.

These skills translate directly to real-world use: document stores like MongoDB are common in data pipelines, APIs, and applications where schema flexibility and nested data are useful.

---

## Submit your work

Your repository should look roughly like this (other `uv init` files are fine too):

```text
lab-05-nosql/
├── .gitignore
├── README.md
├── bookstore.js
├── pyproject.toml
├── uv.lock
└── src/
    └── nosql_lab/
        ├── __init__.py
        └── bookstore_report.py
```

**Submission steps**

Confirm that `.venv` and `.vscode` are listed in `.gitignore`, then run `git status` and verify that `.venv/` and `.vscode/` are **not** staged for commit.

Add all project files (gitignored paths stay out automatically):

```bash
git add .
```

Commit your work:

```bash
git commit -m "Complete Lab 05: NoSQL with MongoDB"
```

Push to your repository:

```bash
git push origin main
```

Submit the URL of your forked repository in the Canvas assignment. The URL should look like: `https://github.com/YOUR_USERNAME/lab-05-nosql`
