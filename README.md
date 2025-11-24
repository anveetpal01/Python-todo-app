# Project Documentation: Todo Application

## 1. Introduction
Designed and built a full-stack, Todo application that allows multiple users to register, log in, and manage their private tasks. Unlike a simple todo list, this project implements **Authentication (Auth)** and **Database Relationships**, ensuring that User A cannot see or edit User B's tasks.

---

## 2. Technical Stack
* **Backend:** FastAPI.
* **Database:** SQLite | ORM-SQLAlchemy.
* **Security:** JWT (JSON Web Tokens) for stateless authentication & pwdlib for password hashing.
* **Frontend:** Streamlit.
* **Testing:** Pytest (Automated testing) & Postman (Manual API testing).

---

## 3. Development 

### Phase 1: Requirement Gathering & Planning
Determined that the app needed three core pillars:
1.  **Security:** Users must log in to access data.
2.  **Privacy:** Data must be segregated per user.
3.  **CRUD Operations:** Create, Read, Update (Check/Complete), and Delete tasks.

### Phase 2: Database Design
Designed a Relational Schema using **One-to-Many Relationship**:
* **User Table:** Stores credentials.
* **Task Table:** Stores task details and a `Foreign Key` linking back to the User.(Tasks for every users store in a single table)

### Phase 3: Backend Implementation
Built the API using **FastAPI**. Implemented a dependency injection system to verify tokens before allowing access to any route (`get_current_user`). This acts as a security guard for every API endpoint.

### Phase 4: Frontend Integration
Used **Streamlit** to build a functional frontend in Python. This allowed me to visualize the backend logic immediately.

### Phase 5: Testing & Quality Assurance
Didn't just write code; also verified it.
* Used **Swagger UI** and **Postman** for manual route checking.
* Wrote a **Pytest** script to automate the testing of Signup -> Login -> Create Task -> Verify Security flow.

---

## 4. Codebase Breakdown

Here is the architecture of `backend/` directory and how the files interact:

### Security & Config
* **`auth.py`**: Authentication Code.
    * **Hashing:** Hashed Passwords using pwdlib | Algorithm - **Argon2** 
    * **Token Generation:** Creates a **JWT Access Token** when a user logs in.

### Database Layer
* **`database.py`**: The Bridge between code and database(`todo.db`).
* **`models.py`**: The Blueprint. It defines the SQL tables.

### Validation & Logic
* **`schemas.py`**: The Filter (Pydantic), ensures data integrity, prevents sensitive data (like passwords) from being sent back in API responses.
* **`main.py`**: The Brain / Controller.
    * Defines API endpoints (`/signup`, `/login`, `/tasks`).
    * Uses `Depends(get_current_user)` to enforce security on routes.

### Interface & Testing
* **`streamlit_app.py`**: It provides a UI for Login, Signup, and Task Management. It talks to the backend using Python `requests`.
* **`test_main.py`**: A script that runs automated tests to ensure the system is bug-free.

---

## 5. Install and Run
run here online - https://python-todo-app.streamlit.app/ (user - tony@marvel.com | pass - 1234)  
for offline - replace API_URL with localhost url in streamlit-app.py
Run in command prompt  
git clone https://github.com/anveetpal01/Python-todo-app  
cd Python-todo-app  
pip install -r requirements.txt  
streamlit run streamlit-app.py  
cd backend  
uvicorn main:app --reload
