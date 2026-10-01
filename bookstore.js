db = db.getSiblingDB("bookstore");
// Step 3: Load authors
db.authors.drop();

doc = JSON.parse(fs.readFileSync("authors.json", "utf8"));
db.authors.insertMany(doc);


// Step 4: Load books
db.books.drop();

doc = JSON.parse(fs.readFileSync("books.json", "utf8"));
db.books.insertMany(doc);


// Step 5: List the loaded data
db.authors.find();
db.books.find();


// Step 6: Insert two new books
db.books.insertMany([
  {
    title: "The Hobbit",
    published_year: 1937,
    author_ids: ["author_004"]
  },
  {
    title: "Dune",
    published_year: 1965,
    author_ids: ["author_005"]
  }
]);


// Step 7: Add missing authors
db.authors.insertMany([
  {
    _id: "author_004",
    name: "J.R.R. Tolkien",
    nationality: "British",
    bio: {
      short: "English writer and scholar best known for his fantasy works.",
      long: "J.R.R. Tolkien was an English writer and philologist best known for creating Middle-earth and writing The Hobbit and The Lord of the Rings."
    }
  },
  {
    _id: "author_005",
    name: "Frank Herbert",
    nationality: "American",
    bio: {
      short: "American science fiction writer best known for Dune.",
      long: "Frank Herbert was an American science fiction writer whose novel Dune became one of the best-known works of science fiction."
    }
  }
]);


// Step 8: Verify the data
db.authors.find();
db.books.find();
