from pydantic import BaseModel, Field
import json

class DeveloperPersona(BaseModel):
    name: str = Field(default="", description="The name of the new developer")
    role: str = Field(default="", description="The developer's role (e.g., Backend, Frontend, DevOps)")
    experience: str = Field(default="", description="The developer's experience level (e.g., Intern, Junior, Senior)")
    tech_stack: str = Field(default="", description="The primary technology stack (e.g., Node.js, Python, React, Java)")

    def is_complete(self):
        return bool(self.name and self.role and self.experience and self.tech_stack)

# Simple in-memory storage mapping session_id -> DeveloperPersona
personas_db = {}

def get_persona(session_id: str) -> DeveloperPersona:
    if session_id not in personas_db:
        personas_db[session_id] = DeveloperPersona()
    return personas_db[session_id]

def update_persona(session_id: str, new_data: dict) -> DeveloperPersona:
    persona = get_persona(session_id)
    # Update only fields that have values
    if new_data.get("name"): persona.name = new_data["name"]
    if new_data.get("role"): persona.role = new_data["role"]
    if new_data.get("experience"): persona.experience = new_data["experience"]
    if new_data.get("tech_stack"): persona.tech_stack = new_data["tech_stack"]
    
    personas_db[session_id] = persona
    return persona
