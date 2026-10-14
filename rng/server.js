const express = require('express');
const session = require('express-session');
const path = require('path');
const app = express();

// Middleware
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));
app.use(session({
    secret: '2f1e3E5sd2Fcsd321',
    resave: false,
    saveUninitialized: true,
    cookie: { secure: false }
}));

// Generate a random 6-character secret
function generateSecret() {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let secret = '';
    for (let i = 0; i < 6; i++) {
        secret += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return secret;
}

// Route to generate secret
app.post('/api/generate', (req, res) => {
    req.session.secret = generateSecret();
    res.json({ message: 'Secret generated successfully' });
});

// Route to verify guess
app.post('/api/verify', (req, res) => {
    const { guess } = req.body;
    const sessionSecret = req.session.secret;

    if (!sessionSecret) {
        return res.json({ type: 'error', message: 'No secret generated' });
    }

    if (guess === sessionSecret) {
        res.json({ type: 'success', message: 'Guess verified successfully' });
    } else {
        res.json({ type: 'error', message: 'Invalid guess' });
    }
});

// Serve the frontend
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});



// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});