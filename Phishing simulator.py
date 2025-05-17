import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import random
from datetime import datetime, timedelta
import json
import os

class EmailSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Phishing Awareness Simulator")
        self.root.geometry("1000x700")
        
        # User data
        self.score = 0
        self.total_emails = 0
        self.phishing_emails_reported = 0
        self.genuine_emails_reported = 0
        self.history = []
        self.user_name = ""
        
        # Tutorial mode
        self.tutorial_shown = False
        
        # Create data directory if not exists
        if not os.path.exists("user_data"):
            os.makedirs("user_data")
        
        self.create_widgets()
        self.show_welcome()
    
    def create_widgets(self):
        # Menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        
        # File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="New Session", command=self.new_session)
        self.file_menu.add_command(label="View History", command=self.show_history)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        
        # Help menu
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="Tutorial", command=self.show_tutorial)
        self.help_menu.add_command(label="About", command=self.show_about)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        
        # Header
        self.header = tk.Label(self.root, text="Advanced Phishing Awareness Simulator", 
                             font=("Arial", 16, "bold"))
        self.header.pack(pady=10)
        
        # User info frame
        self.user_frame = tk.Frame(self.root)
        self.user_frame.pack(pady=5)
        
        self.user_label = tk.Label(self.user_frame, text="User: ", font=("Arial", 12))
        self.user_label.pack(side=tk.LEFT)
        
        # Score display
        self.score_frame = tk.Frame(self.root)
        self.score_frame.pack(pady=5)
        
        self.score_label = tk.Label(self.score_frame, text=f"Score: {self.score}", 
                                   font=("Arial", 12))
        self.score_label.pack(side=tk.LEFT, padx=10)
        
        # Stats label
        self.stats_label = tk.Label(self.score_frame, 
                                  text="Phishing Reported: 0 | Genuine Reported: 0", 
                                  font=("Arial", 10))
        self.stats_label.pack(side=tk.LEFT, padx=20)
        
        # Email list with scrollbar
        self.list_frame = tk.Frame(self.root)
        self.list_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        self.scrollbar = tk.Scrollbar(self.list_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.email_listbox = tk.Listbox(self.list_frame, width=100, height=10, 
                                      font=("Arial", 10), yscrollcommand=self.scrollbar.set)
        self.email_listbox.pack(fill=tk.BOTH, expand=True)
        self.email_listbox.bind('<<ListboxSelect>>', self.show_email_details)
        self.email_listbox.bind('<Double-Button-1>', self.open_email_link)
        
        self.scrollbar.config(command=self.email_listbox.yview)
        
        # Buttons
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)
        
        self.report_button = tk.Button(self.button_frame, text="Report as Phishing", 
                                     command=self.report_phishing, width=15)
        self.report_button.pack(side=tk.LEFT, padx=10)
        
        self.genuine_button = tk.Button(self.button_frame, text="Mark as Genuine", 
                                      command=self.mark_genuine, width=15)
        self.genuine_button.pack(side=tk.LEFT, padx=10)
        
        self.new_emails_button = tk.Button(self.button_frame, text="Get New Emails", 
                                         command=self.generate_sample_emails, width=15)
        self.new_emails_button.pack(side=tk.LEFT, padx=10)
        
        # Email details with scrollbar
        self.details_frame = tk.Frame(self.root)
        self.details_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        self.details_scroll = tk.Scrollbar(self.details_frame)
        self.details_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.details_text = tk.Text(self.details_frame, width=115, height=20, 
                                   wrap=tk.WORD, font=("Arial", 12), 
                                   yscrollcommand=self.details_scroll.set)
        self.details_text.pack(fill=tk.BOTH, expand=True)
        
        self.details_scroll.config(command=self.details_text.yview)
        
        # Attachment frame
        self.attachment_frame = tk.Frame(self.root)
        self.attachment_frame.pack(pady=5)
        
        self.attachment_label = tk.Label(self.attachment_frame, text="Attachments: ", 
                                       font=("Arial", 10))
        self.attachment_label.pack(side=tk.LEFT)
        
        # Status bar
        self.status_bar = tk.Label(self.root, text="Ready", bd=1, relief=tk.SUNKEN, 
                                 anchor=tk.W)
        self.status_bar.pack(fill=tk.X)
    
    def show_welcome(self):
        self.user_name = simpledialog.askstring("Welcome", 
                                              "Enter your name to begin:")
        if not self.user_name:
            self.user_name = "User"
        
        self.user_label.config(text=f"User: {self.user_name}")
        self.show_tutorial()
        self.generate_sample_emails()
    
    def new_session(self):
        self.score = 0
        self.phishing_emails_reported = 0
        self.genuine_emails_reported = 0
        self.update_score()
        self.generate_sample_emails()
        self.update_status("New session started")
    
    def generate_sample_emails(self):
        self.emails = []
        self.email_listbox.delete(0, tk.END)
        
        # Generate genuine emails (more realistic templates)
        genuine_templates = [
            {
                "sender": "IT Department",
                "subject": "Scheduled System Maintenance - March 15",
                "from_email": "it.support@yourcompany.com",
                "body": """Dear Team,

We would like to inform you about the scheduled system maintenance window:

Date: March 15, 2023
Time: 10:00 PM to 2:00 AM (EST)
Impact: All systems will be unavailable during this period

Please save your work and log out before the maintenance begins. 

For more details, visit our IT portal: https://it.yourcompany.com/maintenance

Thank you for your cooperation.

Best regards,
IT Support Team
yourcompany.com""",
                "link": "https://it.yourcompany.com/maintenance",
                "attachments": []
            },
            {
                "sender": "Human Resources",
                "subject": "Important: Benefits Enrollment Period Open",
                "from_email": "hr.benefits@yourcompany.com",
                "body": """Hello Colleagues,

The annual benefits enrollment period is now open from March 1-15. 

Please review your options and make your selections by the deadline. 

To access the enrollment system:
1. Visit https://hr.yourcompany.com/benefits
2. Log in with your employee credentials
3. Complete your enrollment

If you have questions, please contact benefits@yourcompany.com

Sincerely,
HR Benefits Team""",
                "link": "https://hr.yourcompany.com/benefits",
                "attachments": ["Benefits_Guide_2023.pdf"]
            },
            {
                "sender": "Security Team",
                "subject": "Reminder: Mandatory Security Training Due",
                "from_email": "security.training@yourcompany.com",
                "body": """Dear Employee,

This is a reminder that your annual security awareness training is due by March 31st.

To complete the training:
1. Log in to the Learning Portal: https://learn.yourcompany.com
2. Select "Security Awareness 2023"
3. Complete all modules and the final quiz

Note: Failure to complete this mandatory training may result in restricted system access.

For assistance, contact the Help Desk at ext. 4357.

Regards,
Corporate Security Team""",
                "link": "https://learn.yourcompany.com",
                "attachments": []
            },
            {
                "sender": "Payroll Department",
                "subject": "Your February 2023 Payslip is Available",
                "from_email": "payroll.notices@yourcompany.com",
                "body": """Dear Employee,

Your payslip for February 2023 is now available in the employee portal.

To access your payslip:
1. Go to https://portal.yourcompany.com
2. Log in with your credentials
3. Navigate to Payroll > Payslips

Please note: We will never email you a payslip directly for security reasons.

If you have any questions, please contact payroll@yourcompany.com

Sincerely,
Payroll Department""",
                "link": "https://portal.yourcompany.com",
                "attachments": []
            },
            {
                "sender": "Facilities Management",
                "subject": "Office Reopening Guidelines",
                "from_email": "facilities@yourcompany.com",
                "body": """Hello Everyone,

As we prepare for the full office reopening on April 3rd, please review the attached guidelines document.

Key points:
- New cleaning protocols
- Updated seating arrangements
- Conference room booking procedures

The full details are in the attached document.

Welcome back!

Facilities Team""",
                "link": "",
                "attachments": ["Office_Reopening_Guidelines.pdf"]
            },
            {
        "sender": "Amazon",
        "subject": "Your Order #123-4567890-1234567 Has Shipped",
        "from_email": "shipment-tracking@amazon.com",
        "body": """Hi,

Your Amazon order #123-4567890-1234567 has been shipped and is on the way.

Track your package: https://www.amazon.com/track/1234567

Thank you for shopping with us!
Amazon Team""",
        "link": "https://www.amazon.com/track/1234567",
        "attachments": []
            },
            {
        "sender": "PayPal",
        "subject": "Payment Confirmation - $65.00 to Netflix",
        "from_email": "service@paypal.com",
        "body": """Hello,

You’ve authorized a payment of $65.00 USD to Netflix.

Transaction ID: 4T12345678901234M
Date: May 10, 2025

View details: https://www.paypal.com/myaccount/transactions

Thanks,
PayPal""",
        "link": "https://www.paypal.com/myaccount/transactions",
        "attachments": []
            },
            {
    "sender": "Slack",
    "subject": "You have unread messages in #general",
    "from_email": "notifications@slack.com",
    "body": """Hi,

You have unread messages in the #general channel.

Catch up with your team: https://yourcompany.slack.com/messages/general

Thanks,
The Slack Team""",
    "link": "https://yourcompany.slack.com/messages/general",
    "attachments": []
            },
            {
    "sender": "Zoom",
    "subject": "Meeting Invitation: Project Sync",
    "from_email": "no-reply@zoom.us",
    "body": """You have been invited to the following Zoom meeting:

Topic: Weekly Project Sync
Time: May 15, 2025 10:00 AM

Join Zoom Meeting:
https://zoom.us/j/1234567890

Zoom Support""",
    "link": "https://zoom.us/j/1234567890",
    "attachments": []
            },
            {
    "sender": "Dropbox",
    "subject": "Shared File: Q2 Strategy Plan.pdf",
    "from_email": "no-reply@dropbox.com",
    "body": """Hi,

John has shared a file with you: Q2 Strategy Plan.pdf

View the file: https://www.dropbox.com/s/q2strategyplan

Dropbox""",
    "link": "https://www.dropbox.com/s/q2strategyplan",
    "attachments": []
            },
            {
    "sender": "Outlook Calendar",
    "subject": "Upcoming Event: Client Review Meeting",
    "from_email": "calendar-notify@outlook.com",
    "body": """This is a reminder for your upcoming event:

Event: Client Review Meeting
Date: May 17, 2025
Time: 2:00 PM

Join here: https://outlook.office365.com/meeting/abc123

Microsoft Outlook Calendar""",
    "link": "https://outlook.office365.com/meeting/abc123",
    "attachments": []
            },
            {
    "sender": "Indeed",
    "subject": "New Jobs Matching: Cybersecurity Analyst",
    "from_email": "alerts@indeed.com",
    "body": """Hi,

We found new job listings that match your search: "Cybersecurity Analyst".

View jobs: https://www.indeed.com/jobs?q=cybersecurity+analyst

Good luck!
Indeed""",
    "link": "https://www.indeed.com/jobs?q=cybersecurity+analyst",
    "attachments": []
            }

        ]
        
        # Generate sophisticated phishing emails
        phishing_templates = [
            {
                "sender": "IT Security",
                "subject": "URGENT: Unusual Login Activity Detected on Your Account",
                "from_email": "security-alert@your-company-support.com",
                "body": """URGENT SECURITY NOTIFICATION,

We detected unusual login activity on your account from a new device in Germany.

If this wasn't you, please secure your account immediately:

1. Click here to verify your identity: http://your-company-support.com/verify
2. Change your password
3. Review recent activity

Failure to respond within 24 hours will result in account suspension.

Security Team
Your Company Support""",
                "link": "http://your-company-support.com/verify",
                "attachments": [],
                "red_flags": [
                    "Urgency created ('URGENT', '24 hours')",
                    "Suspicious domain (your-company-support.com)",
                    "Requests immediate action via link",
                    "Generic greeting ('Your Account')",
                    "Poor grammar and formatting"
                ]
            },
            {
                "sender": "Microsoft Office 365",
                "subject": "Your Subscription Will Be Suspended",
                "from_email": "noreply@office365-update.com",
                "body": """Dear Office 365 User,

Your subscription will be suspended due to a billing issue. To avoid service interruption:

1. Click here to update your payment details: http://office365-update.com/billing
2. Verify your account information

Important: You must complete this process within 12 hours to maintain access to your emails and files.

Microsoft Office 365 Team""",
                "link": "http://office365-update.com/billing",
                "attachments": ["Payment_Invoice_98342.pdf"],
                "red_flags": [
                    "Fake sender (not from microsoft.com)",
                    "Creates false urgency",
                    "Requests sensitive information",
                    "Attachment could be malicious",
                    "Unofficial domain (office365-update.com)"
                ]
            },
            {
                "sender": "LinkedIn Connections",
                "subject": "You have 3 new connection requests waiting",
                "from_email": "notifications@linkedin-mail.net",
                "body": """Hi there,

You have 3 new connection requests waiting for your response:

- John Smith (CEO at TechCorp)
- Sarah Johnson (Recruiter at TalentFinders)
- Michael Brown (HR Director at GlobalSoft)

View and respond to your pending requests:
http://linkedin-mail.net/connections

The LinkedIn Team""",
                "link": "http://linkedin-mail.net/connections",
                "attachments": [],
                "red_flags": [
                    "Fake LinkedIn domain (linkedin-mail.net)",
                    "Generic greeting ('Hi there')",
                    "Uses social engineering (important-sounding names)",
                    "Link goes to suspicious site"
                ]
            },
            {
                "sender": "DHL Express",
                "subject": "Package Delivery Failed - Action Required",
                "from_email": "delivery@dhl-express-tracking.com",
                "body": """Dear Customer,

We attempted to deliver your package today but were unsuccessful.

Tracking #: DHL78432905
Estimated Delivery Date: March 10, 2023
Recipient: Your Name

Please download and complete the attached delivery form and schedule a new delivery.

Download form: http://dhl-express-tracking.com/form

DHL Customer Service""",
                "link": "http://dhl-express-tracking.com/form",
                "attachments": ["Delivery_Form_DHL78432905.exe"],
                "red_flags": [
                    "Suspicious attachment (.exe file)",
                    "Fake DHL domain",
                    "Creates false urgency",
                    "Uses generic recipient ('Your Name')",
                    "Malicious executable attachment"
                ]
            },
            {
                "sender": "Your Bank",
                "subject": "Security Alert: Unusual Transaction Detected",
                "from_email": "alerts@your-bank-security.com",
                "body": """Dear Valued Customer,

We detected an unusual transaction attempt on your account:

Amount: $1,250.00
Merchant: Amazon Web Services
Location: Singapore

If you didn't authorize this transaction, please verify your account immediately:

http://your-bank-security.com/secure-login

For your security, we've temporarily restricted your account until verification is complete.

Bank Security Team""",
                "link": "http://your-bank-security.com/secure-login",
                "attachments": [],
                "red_flags": [
                    "Fake bank domain",
                    "Creates panic with false transaction",
                    "Requests login via link",
                    "Generic greeting ('Valued Customer')",
                    "Misspelled words"
                ]
            },
            {
                "sender": "Google Drive",
                "subject": "You've received a shared document",
                "from_email": "drive-share@google-docs.net",
                "body": """Hello,

You've received an important document shared via Google Drive:

Document: "Q1 Financial Report - Confidential"
Shared by: James Wilson (Finance Dept)

Click to view: http://google-docs.net/view/GFD7832

This link will expire in 24 hours.

Google Drive Team""",
                "link": "http://google-docs.net/view/GFD7832",
                "attachments": [],
                "red_flags": [
                    "Fake Google domain",
                    "Uses curiosity ('Confidential')",
                    "Creates false urgency ('expires in 24 hours')",
                    "Generic greeting",
                    "Link goes to suspicious site"
                ]
            },
            {
    "sender": "PayPal Support",
    "subject": "Your account is limited — action needed",
    "from_email": "alert@paypal-resolve.com",
    "body": """Dear User,

We've noticed unusual activity in your PayPal account.

To restore access, please verify your information:
http://paypal-resolve.com/login

PayPal Security""",
    "link": "http://paypal-resolve.com/login",
    "attachments": [],
    "red_flags": [
        "Fake PayPal domain",
        "Urgent action request",
        "Unsecured link"
    ]
            },
            {
    "sender": "Amazon Prime",
    "subject": "Your membership is expiring soon!",
    "from_email": "support@amazon-billing.com",
    "body": """Hello,

Your Amazon Prime subscription is expiring.

Renew here to continue benefits: http://amazon-billing.com/renew

Amazon Support""",
    "link": "http://amazon-billing.com/renew",
    "attachments": [],
    "red_flags": [
        "Fake billing domain",
        "Urgency",
        "Unsecured link"
    ]
            },
            {
    "sender": "Google Docs",
    "subject": "Shared confidential document: 'Budget2025'",
    "from_email": "drive@google-docs-services.com",
    "body": """Hi,

A confidential document has been shared with you.

View here: http://google-docs-services.com/shared/Budget2025

Google Drive""",
    "link": "http://google-docs-services.com/shared/Budget2025",
    "attachments": [],
    "red_flags": [
        "Fake domain",
        "Creates curiosity",
        "Unsecured external link"
    ]
            },
            {
    "sender": "Facebook Security",
    "subject": "Suspicious login attempt detected",
    "from_email": "secure@facebook-alerts.com",
    "body": """Hi,

We detected a suspicious login from Russia. If this wasn't you:

Secure your account now: http://facebook-alerts.com/security

Facebook""",
    "link": "http://facebook-alerts.com/security",
    "attachments": [],
    "red_flags": [
        "Scare tactic",
        "Impersonation of Facebook",
        "Look-alike domain"
    ]
            },
            {
    "sender": "Microsoft Support",
    "subject": "License Expired - Renew Now",
    "from_email": "admin@microsoft-renewal.com",
    "body": """Attention,

Your Microsoft Office license has expired.

Click below to renew:
http://microsoft-renewal.com/renew

Failure to act will disable access.

Microsoft""",
    "link": "http://microsoft-renewal.com/renew",
    "attachments": [],
    "red_flags": [
        "Fake renewal domain",
        "Fake urgency",
        "Unusual sender address"
    ]
            }

        ]
        
        # Select random emails (3 genuine, 3 phishing)
        selected_emails = random.sample(genuine_templates, 10) + random.sample(phishing_templates, 11)
        random.shuffle(selected_emails)
        
        for template in selected_emails:
            days_ago = random.randint(0, 9)
            date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d %H:%M")
            
            email = {
                'from': template['sender'],
                'subject': template['subject'],
                'from_email': template['from_email'],
                'date': date,
                'body': template['body'],
                'link': template['link'],
                'attachments': template.get('attachments', []),
                'is_phishing': 'red_flags' in template,
                'red_flags': template.get('red_flags', []),
                'evaluated': False  # <-- NEW FLAG
                    }

            
            self.emails.append(email)
            display_text = f"{email['from']} - {email['subject']}"
            if email['attachments']:
                display_text += " (Attachment)"
            self.email_listbox.insert(tk.END, display_text)
        
        self.total_emails = len(selected_emails)
        self.update_status(f"Loaded {self.total_emails} new emails. Review them carefully!")
    
    def show_email_details(self, event):
        selection = self.email_listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        email = self.emails[index]
        
        details = f"From: {email['from']} <{email['from_email']}>\n"
        details += f"Date: {email['date']}\n"
        details += f"Subject: {email['subject']}\n\n"
        details += email['body']
        
        self.details_text.config(state=tk.NORMAL)
        self.details_text.delete(1.0, tk.END)
        self.details_text.insert(tk.END, details)
        self.details_text.config(state=tk.DISABLED)
        
        # Update attachments display
        for widget in self.attachment_frame.winfo_children()[1:]:
            widget.destroy()
        
        if email['attachments']:
            for attachment in email['attachments']:
                btn = tk.Button(self.attachment_frame, text=attachment, 
                              command=lambda a=attachment: self.open_attachment(a, email['is_phishing']))
                btn.pack(side=tk.LEFT, padx=5)
        else:
            tk.Label(self.attachment_frame, text="No attachments").pack()
    
    def open_attachment(self, filename, is_phishing):
        if is_phishing:
            # Check for dangerous file types
            dangerous_extensions = ['.exe', '.bat', '.cmd', '.js', '.vbs', '.scr', '.jar']
            if any(filename.lower().endswith(ext) for ext in dangerous_extensions):
                messagebox.showerror("Malware Detected!", 
                                   f"WARNING: The file '{filename}' appears to be malicious!\n\n"
                                   "In a real scenario, this could have installed malware on your computer.")
            else:
                messagebox.showwarning("Suspicious Attachment", 
                                     f"Opening attachment '{filename}' from a phishing email.\n\n"
                                     "Even if this file seems safe, it could still be dangerous.")
        else:
            messagebox.showinfo("Safe Attachment", 
                              f"Opening legitimate attachment: {filename}\n\n"
                              "This is a safe document from a trusted sender.")
    
    def open_email_link(self, event):
        selection = self.email_listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        email = self.emails[index]
        
        if not email['link']:
            messagebox.showinfo("No Link", "This email doesn't contain a clickable link.")
            return
        
        if email['is_phishing']:
            messagebox.showerror("Hacked!", 
                               "You've been phished! This was a malicious link.\n\n"
                               f"Red flags you missed:\n{chr(10).join(email['red_flags'])}")
            self.score -= 15  # Penalty for clicking phishing link
            self.update_score()
        else:
            messagebox.showinfo("Safe Link", 
                              "This is a legitimate link. You would now be taken to the official website.")
            # In a real program: webbrowser.open(email['link'])
    
    def report_phishing(self):
        selection = self.email_listbox.curselection()
        if not selection:
            self.update_status("Please select an email to report")
            return
        
        index = selection[0]
        email = self.emails[index]
        
        if email.get('evaluated'):
            self.update_status("You've already evaluated this email.")
            return

        if email['is_phishing']:
            self.score += 20
            self.phishing_emails_reported += 1
            message = "Good job! This was indeed a phishing email.\n\n"
            if email['red_flags']:
                message += "Red flags you identified:\n" + "\n".join(f"• {flag}" for flag in email['red_flags'])
            messagebox.showinfo("Correct!", message)
        else:
            self.score -= 10
            messagebox.showwarning("Incorrect", 
                                 "This was actually a genuine email. "
                                 "Be careful not to report legitimate communications.")
        
        email['evaluated'] = True  # Prevent double-reporting
        self.update_score()
        self.record_action("Reported as phishing", email, email['is_phishing'])
    
    def mark_genuine(self):
        selection = self.email_listbox.curselection()
        if not selection:
            self.update_status("Please select an email to mark as genuine")
            return
        
        index = selection[0]
        email = self.emails[index]
        
        if email.get('evaluated'):
            self.update_status("You've already evaluated this email.")
            return

        if not email['is_phishing']:
            self.score += 10
            self.genuine_emails_reported += 1
            messagebox.showinfo("Correct!", "Correct! This is a genuine email.")
        else:
            self.score -= 15
            message = "This was actually a phishing email!\n\n"
            if email['red_flags']:
                message += "Red flags you missed:\n" + "\n".join(f"• {flag}" for flag in email['red_flags'])
            messagebox.showerror("Incorrect", message)
        
        email['evaluated'] = True  # Prevent double-marking
        self.update_score()
        self.record_action("Marked as genuine", email, not email['is_phishing'])
    
    def update_score(self):
        self.score_label.config(text=f"Score: {self.score}")
        self.stats_label.config(text=f"Phishing Reported: {self.phishing_emails_reported} | "
                                   f"Genuine Reported: {self.genuine_emails_reported}")
        
        # Check if all emails have been evaluated
        total_evaluated = self.phishing_emails_reported + self.genuine_emails_reported
        if total_evaluated >= self.total_emails:
            max_possible = self.total_emails * 20  # 20 points per email (10 for genuine, 20 for phishing)
            accuracy = (self.score / max_possible) * 100 if max_possible > 0 else 0
            
            # Save session to history
            session_data = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "score": self.score,
                "accuracy": accuracy,
                "phishing_caught": self.phishing_emails_reported,
                "genuine_correct": self.genuine_emails_reported,
                "total_emails": self.total_emails
            }
            self.history.append(session_data)
            self.save_history()
            
            messagebox.showinfo("Round Complete", 
                              f"Round complete!\n\n"
                              f"Final Score: {self.score}\n"
                              f"Accuracy: {accuracy:.1f}%\n\n"
                              f"Phishing emails caught: {self.phishing_emails_reported}/3\n"
                              f"Genuine emails correctly identified: {self.genuine_emails_reported}/3\n\n"
                              f"Click 'Get New Emails' for another round.")
    
    def record_action(self, action, email, was_correct):
        action_record = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "action": action,
            "email_subject": email['subject'],
            "sender": email['from'],
            "from_email": email['from_email'],
            "was_phishing": email['is_phishing'],
            "was_correct": was_correct,
            "score_impact": self.score
        }
        # Could save this to a log file for detailed analysis
    
    def save_history(self):
        try:
            with open("user_data/history.json", "w") as f:
                json.dump(self.history, f, indent=2)
        except Exception as e:
            print(f"Error saving history: {e}")
    
    def load_history(self):
        try:
            if os.path.exists("user_data/history.json"):
                with open("user_data/history.json", "r") as f:
                    self.history = json.load(f)
        except Exception as e:
            print(f"Error loading history: {e}")
    
    def show_history(self):
        self.load_history()
        
        history_window = tk.Toplevel(self.root)
        history_window.title("Your Training History")
        history_window.geometry("800x500")
        
        if not self.history:
            tk.Label(history_window, text="No history available yet.", 
                    font=("Arial", 12)).pack(pady=20)
            return
        
        # Create a text widget with scrollbar
        scrollbar = tk.Scrollbar(history_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        history_text = tk.Text(history_window, wrap=tk.WORD, yscrollcommand=scrollbar.set)
        history_text.pack(fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=history_text.yview)
        
        # Add history data
        history_text.insert(tk.END, "Your Phishing Training History\n\n")
        history_text.tag_add("header", "1.0", "1.28")
        history_text.tag_config("header", font=("Arial", 14, "bold"), justify="center")
        
        for i, session in enumerate(self.history, 1):
            history_text.insert(tk.END, 
                              f"Session {i}: {session['date']}\n"
                              f"Score: {session['score']} ({session['accuracy']:.1f}% accuracy)\n"
                              f"Phishing caught: {session['phishing_caught']}/{session['total_emails']//2}\n"
                              f"Genuine correct: {session['genuine_correct']}/{session['total_emails']//2}\n\n")
        
        history_text.config(state=tk.DISABLED)
    
    def show_tutorial(self):
        tutorial_window = tk.Toplevel(self.root)
        tutorial_window.title("Phishing Awareness Tutorial")
        tutorial_window.geometry("900x600")
        
        # Create notebook for multiple tabs
        notebook = tk.ttk.Notebook(tutorial_window)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: What is Phishing?
        tab1 = tk.Frame(notebook)
        notebook.add(tab1, text="What is Phishing?")
        
        content1 = tk.Text(tab1, wrap=tk.WORD, padx=10, pady=10)
        content1.pack(fill=tk.BOTH, expand=True)
        
        content1.insert(tk.END, "Understanding Phishing Attacks\n\n", "header")
        content1.tag_config("header", font=("Arial", 14, "bold"))
        
        content1.insert(tk.END, 
                       "Phishing is a type of cyber attack where criminals attempt to trick you into:\n"
                       "• Revealing sensitive information (passwords, credit card numbers)\n"
                       "• Downloading malicious software\n"
                       "• Sending money or valuable data\n\n"
                       "These attacks often come via email but can also arrive as:\n"
                       "• Text messages (SMiShing)\n"
                       "• Phone calls (Vishing)\n"
                       "• Fake websites\n\n"
                       "Phishing emails often pretend to be from trusted organizations like:\n"
                       "• Your bank or credit card company\n"
                       "• Popular services (Microsoft, Google, Apple)\n"
                       "• Shipping companies (FedEx, DHL, UPS)\n"
                       "• Your employer's IT department\n\n")
        
        # Tab 2: Red Flags
        tab2 = tk.Frame(notebook)
        notebook.add(tab2, text="Red Flags")
        
        content2 = tk.Text(tab2, wrap=tk.WORD, padx=10, pady=10)
        content2.pack(fill=tk.BOTH, expand=True)
        
        content2.insert(tk.END, "How to Spot Phishing Emails\n\n", "header")
        content2.tag_config("header", font=("Arial", 14, "bold"))
        
        content2.insert(tk.END, 
                       "Look for these common warning signs:\n\n"
                       "1. Suspicious Sender Address:\n"
                       "   - Check if the domain matches the organization's real domain\n"
                       "   - Watch for slight misspellings (e.g., 'amaz0n.com' instead of 'amazon.com')\n\n"
                       "2. Urgency and Threats:\n"
                       "   - 'Your account will be closed in 24 hours!'\n"
                       "   - 'Immediate action required'\n"
                       "   - 'Failure to respond will result in...'\n\n"
                       "3. Generic Greetings:\n"
                       "   - 'Dear Customer' instead of your name\n"
                       "   - 'Dear User' or 'Dear Account Holder'\n\n"
                       "4. Suspicious Links:\n"
                       "   - Hover over links to see the real destination\n"
                       "   - Watch for URLs that don't match the organization's website\n\n"
                       "5. Requests for Sensitive Information:\n"
                       "   - Legitimate companies won't ask for passwords via email\n"
                       "   - Be wary of requests for credit card numbers or personal details\n\n"
                       "6. Poor Grammar and Spelling:\n"
                       "   - Professional organizations proofread their communications\n"
                       "   - Many phishing emails originate overseas and have language errors\n\n"
                       "7. Unexpected Attachments:\n"
                       "   - Especially .exe, .zip, or other executable files\n"
                       "   - Even PDFs can contain malicious content\n")
        
        # Tab 3: Best Practices
        tab3 = tk.Frame(notebook)
        notebook.add(tab3, text="Best Practices")
        
        content3 = tk.Text(tab3, wrap=tk.WORD, padx=10, pady=10)
        content3.pack(fill=tk.BOTH, expand=True)
        
        content3.insert(tk.END, "Protecting Yourself from Phishing\n\n", "header")
        content3.tag_config("header", font=("Arial", 14, "bold"))
        
        content3.insert(tk.END, 
                       "Follow these security best practices:\n\n"
                       "1. Verify Before Clicking:\n"
                       "   - Hover over links to see the actual URL\n"
                       "   - When in doubt, go directly to the official website\n\n"
                       "2. Don't Open Unexpected Attachments:\n"
                       "   - Especially from unknown senders\n"
                       "   - Even expected attachments can be malicious if the email is compromised\n\n"
                       "3. Use Multi-Factor Authentication (MFA):\n"
                       "   - Even if your password is stolen, MFA can prevent access\n\n"
                       "4. Keep Software Updated:\n"
                       "   - Ensure your OS, browser, and security software are current\n\n"
                       "5. Report Suspicious Emails:\n"
                       "   - Forward phishing attempts to your IT security team\n"
                       "   - Use your email client's 'Report Phishing' feature\n\n"
                       "6. Educate Yourself Continuously:\n"
                       "   - Phishing tactics evolve constantly\n"
                       "   - Participate in regular security awareness training\n\n"
                       "Remember: When in doubt, throw it out! If an email seems suspicious, \n"
                       "it's better to delete it or verify through another channel.\n")
        
        for content in [content1, content2, content3]:
            content.config(state=tk.DISABLED)
        
        self.tutorial_shown = True
    
    def show_about(self):
        messagebox.showinfo("About Phishing Simulator", 
                          "Advanced Phishing Awareness Simulator\n\n"
                          "Version 2.0\n"
                          "Developed for cybersecurity education\n\n"
                          "This tool helps users recognize and resist phishing attempts "
                          "through realistic simulations and immediate feedback.")
    
    def update_status(self, message):
        self.status_bar.config(text=message)

if __name__ == "__main__":
    root = tk.Tk()
    try:
        import ttk
    except:
        import tkinter.ttk as ttk
    app = EmailSimulator(root)
    root.mainloop()