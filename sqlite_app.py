import streamlit as st
import sqlite3
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

# Initialize the conversation chain
import os
#from langchain.chat_models import ChatOpenAI
from langchain_community.chat_models import ChatOpenAI



# Fetch API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(api_key=api_key)
memory = ConversationBufferMemory()
conversation = ConversationChain(llm=llm, memory=memory)

# Initialize SQLite database
conn = sqlite3.connect('company.db')
c = conn.cursor()

# Create employee and department tables
c.execute('''
CREATE TABLE IF NOT EXISTS department (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
)
''')
c.execute('''
CREATE TABLE IF NOT EXISTS employee (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    department_id INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (department_id) REFERENCES department (id)
)
''')
conn.commit()

# Function to save department
def save_department(department_name):
    c.execute('''
    INSERT OR IGNORE INTO department (name)
    VALUES (?)
    ''', (department_name,))
    conn.commit()
    department_id = c.execute('SELECT id FROM department WHERE name = ?', (department_name,)).fetchone()[0]
    return department_id

# Function to save employee
def save_employee(name, department_id):
    c.execute('''
    INSERT INTO employee (name, department_id)
    VALUES (?, ?)
    ''', (name, department_id))
    conn.commit()

# Function to delete an employee
def delete_employee(employee_id):
    c.execute('DELETE FROM employee WHERE id = ?', (employee_id,))
    conn.commit()

# Streamlit UI setup
st.set_page_config(page_title="Employee and Department Chatbot", layout="wide")
st.title("Employee and Department Chatbot UI")

# Sidebar for department and employee management
st.sidebar.header("Management")

# Add a new department
new_department = st.sidebar.text_input("New Department Name")
if st.sidebar.button("Add Department"):
    if new_department:
        save_department(new_department)
        st.sidebar.success(f"Department '{new_department}' added successfully!")

# Add a new employee
new_employee_name = st.sidebar.text_input("New Employee Name")
selected_department = st.sidebar.selectbox("Select Department", [row[0] for row in c.execute('SELECT name FROM department').fetchall()])
if st.sidebar.button("Add Employee"):
    if new_employee_name and selected_department:
        department_id = c.execute('SELECT id FROM department WHERE name = ?', (selected_department,)).fetchone()[0]
        save_employee(new_employee_name, department_id)
        st.sidebar.success(f"Employee '{new_employee_name}' added to '{selected_department}' successfully!")

# Delete an employee
employee_to_delete = st.sidebar.selectbox("Select Employee to Delete", [None] + [f"{row[0]} ({row[1]})" for row in c.execute('''
SELECT e.name, d.name FROM employee e 
LEFT JOIN department d ON e.department_id = d.id
''').fetchall()])
if st.sidebar.button("Delete Selected Employee"):
    if employee_to_delete:
        employee_name = employee_to_delete.split(" (")[0]
        employee_id = c.execute('SELECT id FROM employee WHERE name = ?', (employee_name,)).fetchone()[0]
        delete_employee(employee_id)
        st.sidebar.success(f"Employee '{employee_name}' deleted successfully!")

# Main chat area
st.header("Employee and Department Interaction")
if 'messages' not in st.session_state:
    st.session_state.messages = []

user_input = st.text_input("You: ", key="input")

if st.button("Send"):
    if user_input:
        bot_response = conversation.predict(input=user_input)
        st.session_state.messages.append(("User", user_input))
        st.session_state.messages.append(("Bot", bot_response))
        user_input = ""

# Display the chat history
st.header("Conversation")
for sender, message in st.session_state.messages:
    st.write(f"**{sender}:** {message}")
    st.write("---")
