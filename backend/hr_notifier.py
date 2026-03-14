import datetime
import os

def send_hr_email(persona, tasks):
    """
    Simulates sending an HR notification when onboarding is complete.
    Writes the email to a file and prints it to the console.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    completed_tasks = [t["name"] for t in tasks if t["completed"]]
    pending_tasks = [t["name"] for t in tasks if not t["completed"]]
    
    email_body = f"""
==================================================
SUBJECT: Developer Onboarding Completed
DATE: {timestamp}
==================================================

Employee Name: {persona.name}
Role: {persona.experience} {persona.role}
Tech Stack: {persona.tech_stack}

Status: ONBOARDING COMPLETE 🎉

Completed Tasks:
"""
    for task in completed_tasks:
        email_body += f" * [X] {task}\n"
        
    email_body += "\nPending Tasks:\n"
    if not pending_tasks:
        email_body += " None! All done.\n"
    else:
        for task in pending_tasks:
            email_body += f" * [ ] {task}\n"
            
    email_body += "==================================================\n"
    
    print("\n\n🤖 Triggering HR Notification...")
    print(email_body)
    
    # Save to file
    if not os.path.exists("../database"):
        os.makedirs("../database")
        
    filename = f"../database/HR_Report_{persona.name.replace(' ', '_')}.txt"
    with open(filename, "w", encoding='utf-8') as f:
        f.write(email_body)
        
    return f"HR Notification successfully sent and saved to {filename}."
