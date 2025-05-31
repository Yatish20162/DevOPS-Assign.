const express = require('express');
const axios = require('axios');
const bodyParser = require('body-parser');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;
const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:5001';

// Middleware
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, 'public')));

// Set EJS as template engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Routes
app.get('/', (req, res) => {
    res.render('index', { result: null, error: null });
});

app.post('/submit', async (req, res) => {
    try {
        const formData = {
            name: req.body.name,
            email: req.body.email,
            age: req.body.age,
            city: req.body.city,
            hobby: req.body.hobby
        };

        // Send data to Flask backend
        const response = await axios.post(`${BACKEND_URL}/process`, formData, {
            headers: {
                'Content-Type': 'application/json'
            }
        });

        console.log(response)

        res.render('index', { 
            result: response.data, 
            error: null 
        });

    } catch (error) {
        console.error('Error:', error.message);
        res.render('index', { 
            result: null, 
            error: 'Failed to process form data. Please try again.' 
        });
    }
});

app.listen(PORT, '0.0.0.0', () => {
    console.log(`Frontend server running on port ${PORT}`);
});