# Employee and Department Chatbot UI
A simple web-based chatbot application for managing employees and departments using Streamlit and SQLite.

**Table of Contents**
- [Project Overview](#project-overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Database Structure](#database-structure)
- [Contributing](#contributing)
- [License](#license)

**Project Overview**
This application allows users to interact with a chatbot for managing employee and department records. Users can:

-Add new departments and employees
-View employee records by department
-Delete existing employees
-Interact with a chatbot to query department and employee information

**Features**
  -Interactive Streamlit UI
  Integration with LangChain for chatbot capabilities
  Persistent data storage using SQLite
  Employee and Department CRUD operations

**Technologies Used**
Python
Streamlit
SQLite
LangChain (AI Language Model Integration)

**Installation**
1.use python -m streamlit run app.py command to run your streamlit application

**Usage**
Open the Streamlit app in your browser at the provided URL (usually http://localhost:8501).
Use the sidebar to:
Add departments and employees
Delete employees
Use the chatbot UI to query or interact with employee data.

**Database Structure**
The project uses SQLite with the following schema:

#Tables:

1.department: Stores department details.
id: Primary Key
name: Unique department name

2.employee: Stores employee details.
id: Primary Key
name: Employee name
department_id: Foreign Key to department
timestamp: Timestamp for record creation

**Limitations:**
Need billing for continuosly fetching API Key. 

**License**
This project is licensed under the MIT License.
