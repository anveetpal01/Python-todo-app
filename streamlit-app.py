import streamlit as st
import requests

# 1. Backend Config
API_URL = "http://127.0.0.1:8000"

# 2. Session State Management (Yaad rakhna ki user login hai ya nahi)
if 'token' not in st.session_state:
    st.session_state.token = None

if 'user_email' not in st.session_state:
    st.session_state.user_email = None

# --- Helper Functions ---

def login_user(email, password):
    try:
        # FastAPI OAuth2 expects form data, not JSON for login
        response = requests.post(f"{API_URL}/login", data={"username": email, "password": password})
        if response.status_code == 200:
            data = response.json()
            st.session_state.token = data["access_token"]
            st.session_state.user_email = email
            st.success("Login Successful!")
            st.rerun()
        else:
            st.error("Invalid Email or Password")
    except Exception as e:
        st.error(f"Connection Error: {e}")

def signup_user(email, password):
    try:
        response = requests.post(f"{API_URL}/signup", json={"email": email, "password": password})
        if response.status_code == 200:
            st.success("Account Created! Please Login.")
        elif response.status_code == 400:
            st.warning("Email already registered.")
        else:
            st.error("Signup Failed")
    except Exception as e:
        st.error(f"Connection Error: {e}")

def create_task(title):
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    try:
        response = requests.post(f"{API_URL}/tasks", json={"title": title}, headers=headers)
        if response.status_code == 200:
            st.success("Task Added!")
            st.rerun()
        else:
            st.error("Failed to add task.")
    except Exception as e:
        st.error(f"Error: {e}")

def get_tasks():
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    try:
        response = requests.get(f"{API_URL}/tasks", headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Failed to fetch tasks.")
            return []
    except Exception as e:
        st.error(f"Error: {e}")
        return []

def logout():
    st.session_state.token = None
    st.session_state.user_email = None
    st.rerun()

def update_task_status(task_id, title, current_status):
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    
    # Logic: Agar abhi True hai to False karo, False hai to True karo
    new_status = not current_status
    
    try:
        requests.put(
            f"{API_URL}/tasks/{task_id}", 
            json={"title": title, "is_completed": new_status}, # Title bhejna padta hai schema validation ke liye
            headers=headers
        )
        # Page refresh nahi karna padega agar state use kar rahe ho, par safe side ke liye:
        # st.rerun() yahan call mat karna, callback handle karega
    except Exception as e:
        st.error(f"Error updating task: {e}")
# --- UI LAYOUT ---

st.set_page_config(page_title="Todo App", page_icon="✅")

st.title("✅ Python Todo App")

# Agar Token nahi hai -> Show Login/Signup
if st.session_state.token is None:
    tab1, tab2 = st.tabs(["Login", "Signup"])
    
    with tab1:
        st.header("Login")
        email_in = st.text_input("Email", key="login_email")
        pass_in = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            login_user(email_in, pass_in)

    with tab2:
        st.header("Create Account")
        email_up = st.text_input("Email", key="signup_email")
        pass_up = st.text_input("Password", type="password", key="signup_pass")
        if st.button("Sign Up"):
            signup_user(email_up, pass_up)

# Agar Token hai -> Show Dashboard
else:
    st.sidebar.write(f"Logged in as: **{st.session_state.user_email}**")
    if st.sidebar.button("Logout"):
        logout()

    st.subheader("My Tasks")

    # 1. Add New Task
    with st.form("task_form", clear_on_submit=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            new_task_title = st.text_input("New Task", placeholder="What needs to be done?", label_visibility="collapsed")
        with col2:
            submitted = st.form_submit_button("Add Task")
            
        if submitted and new_task_title:
            create_task(new_task_title)

    # 2. Show List of Tasks
    tasks = get_tasks()
    
    if tasks:
        for task in tasks:
            with st.container():
                c1, c2 = st.columns([0.1, 0.9])
                with c1:
                    # KEY Logic: 'on_change' use karenge
                    # Jab checkbox click hoga, ye 'update_task_status' function chalayega
                    is_checked = st.checkbox(
                        "", 
                        value=task['is_completed'], 
                        key=task['id'],
                        on_change=update_task_status,
                        args=(task['id'], task['title'], task['is_completed'])
                    )
                with c2:
                    # Agar completed hai to Strike-through (kaata hua) dikhao
                    if task['is_completed']:
                        st.markdown(f"~~{task['title']}~~")
                    else:
                        st.write(f"**{task['title']}**")
                st.divider()