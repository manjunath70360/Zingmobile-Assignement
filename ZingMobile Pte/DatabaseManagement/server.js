const express = require('express');
const sqlite3 = require('sqlite3').verbose();

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(express.json());

// Connect to SQLite database
const db = new sqlite3.Database('./database.db', (err) => {
  if (err) {
    console.error('Error connecting to database:', err.message);
  } else {
    console.log('Connected to the SQLite database.');
    createTables(); // Create tables when connected to the database
  }
});

// Create tables if not exist
function createTables() {
  db.run(`
    CREATE TABLE IF NOT EXISTS colleges (
      id INTEGER PRIMARY KEY,
      name TEXT NOT NULL,
      state TEXT NOT NULL,
      city TEXT NOT NULL,
      campus TEXT NOT NULL,
      section TEXT NOT NULL
    )
  `);
  db.run(`
    CREATE TABLE IF NOT EXISTS students (
      id INTEGER PRIMARY KEY,
      name TEXT NOT NULL,
      section TEXT NOT NULL,
      college_id INTEGER NOT NULL,
      FOREIGN KEY (college_id) REFERENCES colleges(id)
    )
  `);
}

// Middleware function to check user's role
const checkRole = (requiredRole) => (req, res, next) => {
  const { role } = req.query; // Assuming role is provided in query parameter for simplicity
  if (!role || role !== requiredRole) {
    return res.status(403).json({ message: 'Unauthorized' });
  }
  next(); // Proceed to the next middleware or route handler
};

// Routes for colleges (only Super Admin and Admin have access)
app.get('/api/colleges', checkRole('Super Admin'), (req, res) => {
  db.all('SELECT * FROM colleges', (err, rows) => {
    if (err) {
      console.error('Error fetching colleges:', err);
      res.status(500).json({ message: 'Internal server error' });
    } else {
      res.json(rows);
    }
  });
});

app.post('/api/colleges', checkRole('Admin'), (req, res) => {
  const { name, state, city, campus, section } = req.body;
  db.run('INSERT INTO colleges (name, state, city, campus, section) VALUES (?, ?, ?, ?, ?)',
    [name, state, city, campus, section], (err) => {
      if (err) {
        console.error('Error creating college:', err);
        res.status(500).json({ message: 'Internal server error' });
      } else {
        res.json({ message: 'College created successfully' });
      }
    });
});

// Routes for students (Teacher and Student have access)
app.get('/api/students', checkRole('Teacher'), (req, res) => {
  const { section } = req.query;
  if (!section) {
    return res.status(400).json({ message: 'Section parameter is required' });
  }
  db.all('SELECT * FROM students WHERE section = ?', [section], (err, rows) => {
    if (err) {
      console.error('Error fetching students:', err);
      res.status(500).json({ message: 'Internal server error' });
    } else {
      res.json(rows);
    }
  });
});

app.get('/api/students/:id', checkRole('Student'), (req, res) => {
  const { id } = req.params;
  const { studentId } = req.query;
  if (!studentId || studentId !== id) {
    return res.status(403).json({ message: 'Unauthorized' });
  }
  db.get('SELECT * FROM students WHERE id = ?', [id], (err, row) => {
    if (err) {
      console.error('Error fetching student:', err);
      res.status(500).json({ message: 'Internal server error' });
    } else if (!row) {
      res.status(404).json({ message: 'Student not found' });
    } else {
      res.json(row);
    }
  });
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
