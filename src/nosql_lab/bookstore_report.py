```python
#!/usr/bin/env python3

"""Generate a report of books written by selected authors."""

import logging
import os

import certifi
import pymongo


# Read MongoDB credentials from environment variables.
MONGODB_ATLAS_URL = os.environ.get("MONGODB_ATLAS_URL")
MONGODB_ATLAS_USER = os.environ.get("MONGODB_ATLAS_USER")
MONGODB_ATLAS_PWD = os.environ.get("MONGODB_ATLAS_PWD")


# Configure logging for connection status and errors.
logging.basicConfig(level=logging.INFO)


def main():
    """Connect to MongoDB and print books linked to selected authors."""

    # Choose authors from the starter data and the new data.
    author_ids = [
        "author_002",  # Neil Gaiman
        "author_003",  # Terry Pratchett
        "author_004",  # Author added in Step 7
    ]

    client = None

    try:
        # Connect to MongoDB Atlas using environment variables.
        client = pymongo.MongoClient(
            MONGODB_ATLAS_URL,
            username=MONGODB_ATLAS_USER,
            password=MONGODB_ATLAS_PWD,
            tlsCAFile=certifi.where(),
        )

        # Confirm that the connection works.
        client.admin.command("ping")
        logging.info("Successfully connected to MongoDB Atlas.")

        # Select the bookstore database and collections.
        db = client["bookstore"]
        authors = db["authors"]
        books = db["books"]

        # Count the authors in the selected list.
        author_count = authors.count_documents(
            {"_id": {"$in": author_ids}}
        )

        print(f"Authors: {author_count}")
        print()

        # Find each author and then find books linked to that author's _id.
        for author_id in author_ids:
            author = authors.find_one({"_id": author_id})

            if author is None:
                logging.warning("Author %s was not found.", author_id)
                continue

            print(author["name"])

            # Find every book whose author_ids contains this author.
            author_books = books.find(
                {"author_ids": author["_id"]}
            )

            for book in author_books:
                print(
                    f"  {book['title']} "
                    f"({book['published_year']})"
                )

            print()

    except Exception as error:
        logging.error("MongoDB error: %s", error)

    finally:
        # Close the client when the report is finished.
        if client is not None:
            client.close()
            logging.info("MongoDB connection closed.")


if __name__ == "__main__":
    main()
```
