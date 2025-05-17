const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const bcrypt = require('bcrypt');
const sanitizeHtml = require('sanitize-html');
const app = express();
const port = 3000;

app.use(express.json());

// Database setup
const db = new sqlite3.Database('database.db', (err) => {
    if (err) {
        console.error('Database connection error:', err.message);
        return;
    }
    console.log('Database connected.');

    // Create tables sequentially
    db.serialize(() => {
        // Create users table
        db.run(`CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )`, (err) => {
            if (err) console.error('Error creating users table:', err.message);
        });

        // Create quizzes table
        db.run(`CREATE TABLE IF NOT EXISTS quizzes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            part TEXT,
            question TEXT NOT NULL,
            options TEXT,
            correct_answer TEXT,
            type TEXT
        )`, (err) => {
            if (err) console.error('Error creating quizzes table:', err.message);
        });

        // Create answers table
        db.run(`CREATE TABLE IF NOT EXISTS answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            quiz_id INTEGER,
            user_answer TEXT,
            points INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (quiz_id) REFERENCES quizzes(id)
        )`, (err) => {
            if (err) console.error('Error creating answers table:', err.message);
        });

        // Create leaderboard table
        db.run(`CREATE TABLE IF NOT EXISTS leaderboard (
            user_id INTEGER PRIMARY KEY,
            total_points INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )`, (err) => {
            if (err) console.error('Error creating leaderboard table:', err.message);
            else {
                console.log('All tables created successfully.');

                // Insert quiz data
                const quizData = [
                    // Part 1: Background and Context
                    { part: 'Part 1', question: 'What do phishing, spear phishing, vishing, scareware, watering hole attacks and their ilk have in common?', options: JSON.stringify(['They are all "social engineering" attacks...', 'They are all funny-sounding terms...', 'They are today\'s common examples...', 'All of the above are correct.']), correct_answer: '3', type: 'multiple-choice' },
                    { part: 'Part 1', question: 'Who are the targets of modern day hackers?', options: JSON.stringify(['Banks and finance companies...', 'Any organization or individual...', 'Companies which hold a lot of proprietary information.', 'Companies which hold credit card numbers...']), correct_answer: '1', type: 'multiple-choice' },
                    { part: 'Part 1', question: 'True or False: To protect personal information and other sensitive data, you need only worry about outsider threats such as hackers, phishing scams and ransomware.', options: JSON.stringify(['True', 'False']), correct_answer: '1', type: 'true-false' },
                    { part: 'Part 1', question: 'True or False: If you install software from the internet there is a possibility that viruses or malware could infect your computer and access PII or sensitive data.', options: JSON.stringify(['True', 'False']), correct_answer: '0', type: 'true-false' },
                    { part: 'Part 1', question: 'An email claiming that you won the lottery and requesting that you fill out the corresponding information, is an example of what type of cyber-attack?', options: JSON.stringify(['Baiting', 'Phishing', 'Scareware', 'Vishing']), correct_answer: '1', type: 'multiple-choice' },
                    { part: 'Part 1', question: 'Which of the following is/are example(s) of a phishing attack?', options: JSON.stringify(['Sending someone an email that contains a malicious link...', 'Creating a fake website that looks nearly identical...', 'Sending someone a text message that contains a malicious link...', 'All of the above are correct.']), correct_answer: '3', type: 'multiple-choice' },
                    { part: 'Part 1', question: 'True or false: Scareware is malicious software that tricks computer users into visiting malware-infested websites by displaying a fake pop-up warning on the screen.', options: JSON.stringify(['True', 'False']), correct_answer: '0', type: 'true-false' },
                    { part: 'Part 1', question: 'In a "watering hole" attack, the attacker compromises a site likely to be visited by a particular target group, rather than attacking the target group directly. True or False?', options: JSON.stringify(['True', 'False']), correct_answer: '0', type: 'true-false' },
                    { part: 'Part 1', question: '"Vishing" is a cybercrime that uses the phone to steal personal confidential information from victims. True or False?', options: JSON.stringify(['True', 'False']), correct_answer: '0', type: 'true-false' },
                    { part: 'Part 1', question: 'True or false: You can trust that an email from your client really comes from that client if it uses the client\'s logo and contains at least one fact about the client that you know to be true.', options: JSON.stringify(['True', 'False']), correct_answer: '1', type: 'true-false' },
                    { part: 'Part 1', question: 'Cyber security protection of an organization is the responsibility of:', options: JSON.stringify(['Everyone in the organization.', 'The CIO or CISO executive.', 'A specialized cybersecurity defense team.', 'The board of directors.']), correct_answer: '0', type: 'multiple-choice' },

                    // Part 2: Cyber-Attacks in Action
                    { part: 'Part 2', question: 'What are some of the ways to distinguish a legitimate email from a phishing email?', options: JSON.stringify(['Bad spelling, poor syntax and grammar...', 'Look at the email headers to see where it really came from.', 'Poorly replicated logos.', 'Contact the sender on some other medium besides email to verify...']), correct_answer: '3', type: 'multiple-choice' },
                    { part: 'Part 2', question: 'A new window pops up on your screen telling you that a virus has been found on your computer... How can you tell this is Scareware?', options: JSON.stringify(['Hovering over any of the links will direct you out to third party websites...', 'Windows Firewall will not direct you out to third party websites...', 'Seeks to make you click on buttons for "Enable Protection"...', 'The entire pop-up window may be hyperlinked...', 'All of the above are correct.']), correct_answer: '4', type: 'multiple-choice' },
                    { part: 'Part 2', question: 'The window then presents you a button for you to click offering to resolve the issue. Your best course of action is to:', options: JSON.stringify(['Click on the button to remove the virus.', 'Place your cursor over the button and check the link\'s website address...', 'Close both the original browser window and the new "pop-up" window...', 'Hit the back button and see if it goes away.']), correct_answer: '2', type: 'multiple-choice' },
                    { part: 'Part 2', question: 'Unexpectedly, you get an email from a colleague who asks you to urgently click on an email link... What should you do?', options: JSON.stringify(['The link is from a known person therefore it\'s safe to open.', 'If the link was malicious the organization\'s firewall would have flagged...', 'Reply to the sender to double-check if the link is safe...', 'Do not click the link. Telephone or email or text the sender for verification...']), correct_answer: '3', type: 'multiple-choice' },
                    { part: 'Part 2', question: 'A colleague calls you telling you she has an urgent deadline to meet... What should you do to help?', options: JSON.stringify(['Go to a computer terminal and log the user in...', 'Suggest to your colleague that they call your IT helpdesk...', 'Give them your login credentials temporarily...', 'Put your login credentials on an encrypted USB memory stick...']), correct_answer: '1', type: 'multiple-choice' },
                    { part: 'Part 2', question: 'You receive an email from your bank warning you that suspicious activity has been detected... Which of these actions should you not do?', options: JSON.stringify(['Login immediately and change your password...', 'Login to your bank account immediately and check your balance.', 'Check the headers in the email and then login.', 'Contact your bank by telephone or email using the contact information...', 'You should not do any of these things.']), correct_answer: '4', type: 'multiple-choice' },
                    { part: 'Part 2', question: 'You get a call from your support helpdesk saying they are performing an urgent server upgrade... What should you do?', options: JSON.stringify(['Get the caller\'s name and give him your login and password.', 'Get the caller\'s email address and email him your login and password.', 'Give the support representative your password, but not your login.', 'Refuse and contact your manager or technology director.']), correct_answer: '3', type: 'multiple-choice' },
                    { part: 'Part 2', question: 'True or false: If you\'re working on a project with a colleague or a vendor, you can click on any links as long as you have a spam blocker and anti-virus protection.', options: JSON.stringify(['True', 'False']), correct_answer: '1', type: 'true-false' },
                    { part: 'Part 2', question: 'You get an email from your Operations Director asking you to provide personal information right away. True or false: You should check it out first to verify...', options: JSON.stringify(['True, but ...', 'False']), correct_answer: '0', type: 'true-false' },
                    { part: 'Part 2', question: 'You receive an email from your boss or manager or the company CFO... You should reply right away. True or False?', options: JSON.stringify(['True', 'False']), correct_answer: '1', type: 'true-false' },
                    { part: 'Part 2', question: 'How can you check whether the request is valid?', options: JSON.stringify(['Check the sender\'s email address for discrepancies...', 'Follow normal procedures for payments and wires...', 'Pay attention to unusual circumstances in the request...', 'All of the above are correct.']), correct_answer: '3', type: 'multiple-choice' },
                    { part: 'Part 2', question: 'You receive this "Receipt for your Payment to mum PayPal"...', options: JSON.stringify(['Both A and B are correct.']), correct_answer: '0', type: 'multiple-choice' },
                    { part: 'Part 2', question: 'You get a text from a vendor asking you to click on a link to renew your password... You should:', options: JSON.stringify(['Reply to the text to confirm that you really need to renew...', 'Pick up the phone and call the vendor, using a phone number you know...', 'Click on the link. If it takes you to the vendor\'s website...']), correct_answer: '1', type: 'multiple-choice' },
                    { part: 'Part 2', question: 'Which of these may indicate that these emails are trouble?', options: JSON.stringify(['The email is unsolicited or from an unknown source.', 'The email address uses a strange "to" field...', 'A vague or ambiguous subject line.', 'No salutation addressing you.', 'Poor grammar/spelling', 'A sense of urgency in the requested response', 'All of the above are correct.']), correct_answer: '6', type: 'multiple-choice' },
                    { part: 'Part 2', question: 'What is one to do to protect oneself against these sorts of attacks via malicious attachments?', options: JSON.stringify(['Don\'t click on attachments. Period.', 'If the email has passed the "tests" above, but you\'re still unsure...']), correct_answer: '1', type: 'multiple-choice' },

                    // Part 3: Preventing Successful Cyber-Attacks
                    { part: 'Part 3', question: 'Which of the following are signs that you may have a virus?', options: JSON.stringify(['Mass emails sent to your contact list...', 'Slow performance', 'Unusual pop-ups prompting you to download...', 'Password changes without your authority', 'Hard drive making continual noise', 'Files missing', 'A change to your website homepage', 'Error messages', 'Computer freezes or crashes', 'Unfamiliar programs start up...', 'All of the above.']), correct_answer: '10', type: 'multiple-choice' },
                    { part: 'Part 3', question: 'Which of these are things you should not do if you detect a virus?', options: JSON.stringify(['Quit any application or software that seems to be affected.', 'Stop shopping, banking, and doing other things online...', 'Continue using the same passwords as previously.', 'Check to see if you have security software on your device...', 'For Windows-based devices, run a virus scan...', 'Make sure your software is up to date...']), correct_answer: '2', type: 'multiple-choice' },
                    { part: 'Part 3', question: 'Turning on your firewall is sufficient to prevent malware attacks, true or false?', options: JSON.stringify(['True', 'False']), correct_answer: '1', type: 'true-false' },
                    { part: 'Part 3', question: 'Does private browsing prevent malware attacks?', options: JSON.stringify(['Yes', 'No']), correct_answer: '1', type: 'true-false' },
                    { part: 'Part 3', question: 'Can internet service providers see the online activities of their subscribers when those subscribers are using private browsing?', options: JSON.stringify(['Yes', 'No']), correct_answer: '0', type: 'true-false' },
                    { part: 'Part 3', question: 'If a Scareware window pops up on your computer... is it ok to simply click the "X," "cancel," or "close" button on the pop-up window?', options: JSON.stringify(['No', 'Yes']), correct_answer: '0', type: 'true-false' },
                    { part: 'Part 3', question: 'If you fall for a phishing scam, what should you do to limit the damage?', options: JSON.stringify(['Delete the phishing email.', 'Unplug the computer. This will get rid of any malware.', 'Change any compromised passwords.']), correct_answer: '2', type: 'multiple-choice' },
                    { part: 'Part 3', question: 'What are steps you can take to minimize the risk of a malware or phishing or ransomware attack?', options: JSON.stringify(['Ensure that anti-virus tools are running and up to date', 'All of these answers are correct.', 'Keep your computer software up to date', 'Ensure that you are backing up your critical files']), correct_answer: '1', type: 'multiple-choice' },
                    { part: 'Part 3', question: 'You\'ve inadvertently opened a link or download... What course of action should you take next?', options: JSON.stringify(['The purpose of a firewall and security software is to block...', 'Update and run your anti-virus software.', 'Contact your IT help desk or Information Security team.', 'Keep an eye on the performance of your computer.']), correct_answer: '2', type: 'multiple-choice' },
                    { part: 'Part 3', question: 'What does the "https://" at the beginning of a URL denote...?', options: JSON.stringify(['The site has special high definition.', 'Information that you exchange with that website travels via a secure connection.', 'The site is not accessible to certain computers.', 'None of the above']), correct_answer: '1', type: 'multiple-choice' },
                    { part: 'Part 3', question: 'If a public Wi-Fi network (such as in an airport or coffee shop) requires a password to access... is it generally safe to use that network for sensitive activities such as online banking?', options: JSON.stringify(['Yes, it is safe.', 'No, it is not safe.']), correct_answer: '1', type: 'true-false' },
                    { part: 'Part 3', question: 'How can you identify an unsecure Wi-Fi network?', options: JSON.stringify(['The Wi-Fi is available for free in public places', 'Does not require a username and password to connect.', 'Not sure']), correct_answer: '1', type: 'multiple-choice' },
                    { part: 'Part 3', question: 'What actions can you take today to secure your devices, your password-enabled accounts and your personal information...?', options: JSON.stringify(['Self-Assessment Checklist (of Information Security and Data Privacy Actions)']), correct_answer: '0', type: 'multiple-choice' },
                ];

                // Insert quiz data
                quizData.forEach(q => {
                    db.run(`INSERT OR IGNORE INTO quizzes (part, question, options, correct_answer, type) VALUES (?, ?, ?, ?, ?)`, [q.part, q.question, q.options, q.correct_answer, q.type], (err) => {
                        if (err) console.error('Error inserting quiz:', err.message);
                        else console.log(`Inserted quiz: ${q.question}`);
                    });
                });
            }
        });
    });
});

// Middleware for authentication
const authenticate = (req, res, next) => {
    // Support email in both body (for POST) and query (for GET), but prioritize body for compatibility with provided commands
    const email = req.body.email || req.query.email;
    if (!email) return res.status(401).json({ error: 'Authentication required' });
    db.get(`SELECT id FROM users WHERE email = ?`, [sanitizeHtml(email)], (err, user) => {
        if (err) {
            console.error('Database error in authenticate:', err.message);
            return res.status(500).json({ error: 'Database error' });
        }
        if (!user) return res.status(401).json({ error: 'User not found' });
        req.user = user;
        next();
    });
};

// API Endpoints

// User Registration
app.post('/api/register', (req, res) => {
    const { email, password } = req.body;
    if (!email || !password) return res.status(400).json({ error: 'Email and password are required' });
    const sanitizedEmail = sanitizeHtml(email);
    const hashedPassword = bcrypt.hashSync(password, 10);
    db.run(`INSERT INTO users (email, password) VALUES (?, ?)`, [sanitizedEmail, hashedPassword], (err) => {
        if (err) return res.status(400).json({ error: 'Email already exists' });
        res.json({ message: 'User registered successfully' });
    });
});

// User Login
app.post('/api/login', (req, res) => {
    const { email, password } = req.body;
    if (!email || !password) return res.status(400).json({ error: 'Email and password are required' });
    db.get(`SELECT * FROM users WHERE email = ?`, [sanitizeHtml(email)], (err, user) => {
        if (err) return res.status(500).json({ error: 'Database error' });
        if (!user || !bcrypt.compareSync(password, user.password)) {
            return res.status(401).json({ error: 'Invalid credentials' });
        }
        res.json({ message: 'Login successful', userId: user.id });
    });
});

// Logout
app.post('/api/logout', authenticate, (req, res) => {
    res.json({ message: 'Logout successful' });
});

// Get Quizzes
app.get('/api/quizzes', authenticate, (req, res) => {
    db.all(`SELECT * FROM quizzes`, [], (err, rows) => {
        if (err) return res.status(500).json({ error: 'Failed to fetch quizzes' });
        res.json(rows);
    });
});

// Submit Quiz Answer
app.post('/api/quiz/submit', authenticate, (req, res) => {
    const { quizId, answer } = req.body;
    if (!quizId || !answer) return res.status(400).json({ error: 'Quiz ID and answer are required' });
    db.get(`SELECT correct_answer FROM quizzes WHERE id = ?`, [quizId], (err, quiz) => {
        if (err) return res.status(500).json({ error: 'Database error' });
        if (!quiz) return res.status(404).json({ error: 'Quiz not found' });
        const isCorrect = answer === quiz.correct_answer;
        const points = isCorrect ? 10 : 0;
        db.run(`INSERT INTO answers (user_id, quiz_id, user_answer, points) VALUES (?, ?, ?, ?)`, [req.user.id, quizId, answer, points], (err) => {
            if (err) return res.status(500).json({ error: 'Failed to submit answer' });
            // Update leaderboard
            db.get(`SELECT SUM(points) as total FROM answers WHERE user_id = ?`, [req.user.id], (err, result) => {
                if (err) return res.status(500).json({ error: 'Database error' });
                const totalPoints = result.total || 0;
                db.run(`INSERT OR REPLACE INTO leaderboard (user_id, total_points) VALUES (?, ?)`, [req.user.id, totalPoints], (err) => {
                    if (err) return res.status(500).json({ error: 'Database error' });
                    res.json({ correct: isCorrect, pointsEarned: points, totalPoints });
                });
            });
        });
    });
});

// Get User Progress
app.get('/api/progress', authenticate, (req, res) => {
    db.all(`SELECT COUNT(*) as total FROM quizzes`, [], (err, total) => {
        if (err) return res.status(500).json({ error: 'Database error' });
        db.all(`SELECT COUNT(*) as completed FROM answers WHERE user_id = ?`, [req.user.id], (err, completed) => {
            if (err) return res.status(500).json({ error: 'Database error' });
            db.get(`SELECT total_points FROM leaderboard WHERE user_id = ?`, [req.user.id], (err, points) => {
                if (err) return res.status(500).json({ error: 'Database error' });
                res.json({
                    totalPoints: points ? points.total_points : 0,
                    totalQuizzes: total[0].total,
                    completedQuizzes: completed[0].completed,
                    remainingQuizzes: total[0].total - completed[0].completed,
                });
            });
        });
    });
});

// Get Leaderboard
app.get('/api/leaderboard', authenticate, (req, res) => {
    db.all(`SELECT u.email, l.total_points FROM leaderboard l JOIN users u ON l.user_id = u.id ORDER BY l.total_points DESC LIMIT 5`, [], (err, rows) => {
        if (err) return res.status(500).json({ error: 'Failed to fetch leaderboard' });
        res.json(rows);
    });
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});