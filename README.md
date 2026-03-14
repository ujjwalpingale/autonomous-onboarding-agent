# Autonomous Developer Onboarding Agent

An AI-powered onboarding assistant that helps new software developers get started quickly by guiding them through setup, documentation, and onboarding tasks using a chat interface.

This project was built for a hackathon to automate the developer onboarding process and reduce the manual effort required from HR and engineering teams.

---

# Problem Statement

Onboarding a new developer in a company requires multiple steps:

* Getting access to repositories
* Setting up the development environment
* Reading company documentation
* Understanding internal processes
* Completing onboarding tasks

These steps usually require manual coordination from HR and senior engineers.

This project solves that problem by creating an **AI onboarding agent** that can guide developers through the entire onboarding process automatically.

---

# Key Features

## Chat-Based Onboarding Interface

A conversational interface similar to ChatGPT where new employees can interact with the onboarding assistant.

## Personalized Onboarding

The agent identifies the developer's profile and customizes the onboarding process based on:

* Role (Backend / Frontend / DevOps)
* Experience Level (Intern / Junior / Senior)
* Tech Stack (Python / Node.js / Java)

## Knowledge Base Retrieval (RAG)

The agent retrieves information from company documentation using a Retrieval-Augmented Generation approach.

Developers can ask questions like:

* How do I run the backend server?
* What are the API guidelines?
* How do I set up the development environment?

## Onboarding Checklist Tracking

The system maintains a structured checklist of tasks and tracks onboarding progress.

Example tasks:

* Install required tools
* Clone repository
* Run local server
* Review architecture documentation
* Complete starter task

## HR Completion Notification

Once onboarding is completed, the system generates a structured completion report for HR.

The report includes:

* Employee name
* Role and tech stack
* Completed tasks
* Pending tasks
* Completion timestamp

---

# System Architecture

Frontend
HTML + CSS + JavaScript chat interface

Backend
FastAPI (Python)

AI Layer
Google Gemini API

Knowledge Retrieval
LangChain + Vector Database

Document Storage
Markdown / PDF documentation

---

# Tech Stack

Frontend

* HTML
* CSS
* JavaScript

Backend

* Python
* FastAPI

AI and LLM

* Google Gemini API
* LangChain

Vector Database

* ChromaDB

Embeddings

* Sentence Transformers

Other Tools

* Git
* GitHub

---

# Project Structure

```
frontend/
  index.html
  style.css
  script.js

backend/
  main.py
  agent.py
  persona_detector.py
  checklist_manager.py
  rag_engine.py
  hr_notifier.py

docs/
  backend_setup.md
  frontend_setup.md
  company_policy.md

database/
  vectordb/

requirements.txt
README.md
```

---

# Installation

Clone the repository:

```
git clone https://github.com/ujjwalpingale/autonomous-onboarding-agent.git
```

Move into the project folder:

```
cd autonomous-onboarding-agent
```

Install dependencies:

```
pip install -r requirements.txt
```

---

# Environment Setup

Create a `.env` file inside the backend folder.

Example:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

You can generate a Gemini API key from Google AI Studio.

---

# Running the Backend

Navigate to the backend directory:

```
cd backend
```

Run the server:

```
uvicorn main:app --reload
```

The API will run on:

```
http://127.0.0.1:8000
```

API documentation:

```
http://127.0.0.1:8000/docs
```

---

# Example Workflow

User joins company and interacts with the onboarding agent:

Example message:

"Hi, I'm Riya. I joined as a Backend Intern working with Node.js."

The agent will:

1. Identify the user's role and tech stack
2. Generate a personalized onboarding checklist
3. Provide relevant documentation
4. Track task completion
5. Generate a final onboarding completion report

---

# Future Improvements

* Slack integration for welcome messages
* GitHub repository access automation
* Jira starter task assignment
* Automatic environment verification
* Knowledge base learning from FAQs

---

# Team

Hackathon Project

Team Members:

* Ujjwal Pingale
* Shauat Mulla
* Gopal Kale
* Jeet Patil

---

# License

This project is developed for educational and hackathon purposes.
