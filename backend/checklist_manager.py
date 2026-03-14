from hr_notifier import send_hr_email

# In memory checklist DB mapping session_id -> list of tasks
checklist_db = {}

def generate_checklist_for_persona(session_id: str, role: str, experience: str, tech_stack: str) -> list:
    """Generates a contextual checklist based on the user's detected persona."""
    
    # Base mandatory tasks
    tasks = [
        {"id": 1, "name": "Review Company Policy", "completed": False},
        {"id": 2, "name": "Setup Local Environment", "completed": False}
    ]
    
    # Contextual tasks
    role_lower = role.lower()
    if "backend" in role_lower:
        tasks.append({"id": 3, "name": "Clone backend repository", "completed": False})
        tasks.append({"id": 4, "name": f"Install {tech_stack} dependencies", "completed": False})
        tasks.append({"id": 5, "name": "Run local API server", "completed": False})
        tasks.append({"id": 6, "name": "Read backend architecture docs", "completed": False})
    elif "frontend" in role_lower:
        tasks.append({"id": 3, "name": "Clone frontend repository", "completed": False})
        tasks.append({"id": 4, "name": "Review CompanyUI Style Guide", "completed": False})
        tasks.append({"id": 5, "name": "Run local React server", "completed": False})
    
    if "intern" in experience.lower() or "junior" in experience.lower():
        tasks.append({"id": 7, "name": "Complete starter bug fix", "completed": False})
    elif "senior" in experience.lower():
        tasks.append({"id": 7, "name": "Schedule architecture review with team lead", "completed": False})
        
    checklist_db[session_id] = tasks
    return tasks

def get_checklist(session_id: str):
    return checklist_db.get(session_id, [])

def mark_task_completed(session_id: str, task_id: int, persona_data):
    """Marks a task as complete. If all complete, triggers HR email."""
    tasks = checklist_db.get(session_id, [])
    
    task_found = False
    for task in tasks:
        if task["id"] == task_id or (isinstance(task_id, str) and task["name"].lower() == task_id.lower()):
            task["completed"] = True
            task_found = True
            break
            
    if not task_found:
        return "Error: Task not found in your checklist."
        
    # Check if we are done with all tasks
    all_done = all(t["completed"] for t in tasks)
    msg = "Marked task as completed."
    
    if all_done:
        email_status = send_hr_email(persona_data, tasks)
        msg += f" \n🎉 CONGRATULATIONS! You have finished all onboarding tasks! \n{email_status}"
        
    return msg
