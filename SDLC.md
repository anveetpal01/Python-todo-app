# SDLC Documentation: Multi-User Todo Application

## Project Overview
Building a secure, full-stack Todo application where users can manage their own tasks individually. The system ensures data privacy so users cannot see each other's tasks.

---

## Phase 1: Requirement Gathering
**Goal:** A user specific todo application where each user can read, write, update delete the tasks by sign up and login in to their account.

### Functional Requirements
1.  **Authentication Module:**
    * User Sign Up (Email, Password, Name).
    * User Login (Secure authentication).
    * Logout functionality.
2.  **Task Management (CRUD):**
    * **Create:** Add a new task with a title and status.
    * **Read:** View a list of tasks created *only* by the logged-in user.
    * **Update:** Edit task details or mark as "Completed".
    * **Delete:** Remove a task permanently.
3.  **Views/UI:**
    * **Dashboard:** Shows all active/pending tasks.
    * **Completed List:** A separate view/filter for finished tasks.

---

## Phase 2: Planning & Feasibility
**Goal:** Decide tools and timeline.

### Technology Stack (Recommended)
* **Frontend:** React.js or HTML/CSS/JS (for UI).
* **Backend:** Python (FastAPI/Django) or Node.js (for Logic).
* **Database:** SQL Database (PostgreSQL or SQLite) - *Required for relational data.*
* **Authentication:** JWT (JSON Web Tokens) for secure session handling.

### Architecture Decision
* **Client-Server Model:** The Frontend will send API requests (JSON) to the Backend. The Backend will talk to the Database.

---

## Phase 3: Design (The Blueprint)
**Goal:** Structure the data and logical flow.

### 1. Database Schema (ER Diagram Logic)
We need a **One-to-Many Relationship** (One User -> Many Tasks).

**Table: Users**
| Column | Type | Constraints |
| :--- | :--- | :--- |
| `id` | Integer | Primary Key, Auto Increment |
| `email` | String | Unique, Not Null |
| `password` | String | Hashed (Never store plain text!) |

**Table: Tasks**
| Column | Type | Constraints |
| :--- | :--- | :--- |
| `id` | Integer | Primary Key |
| `title` | String | Not Null |
| `is_completed` | Boolean | Default: False |
| `user_id` | Integer | **Foreign Key (Links to Users.id)** |

### 2. API Endpoints Design
* `POST /auth/signup` - Register new user.
* `POST /auth/login` - Returns Access Token.
* `GET /tasks` - Get tasks *only* for the requester (reads Token).
* `POST /tasks` - Create new task (assigns current `user_id`).
* `PUT /tasks/{id}` - Update status.
* `DELETE /tasks/{id}` - Delete task.

---

## Phase 4: Implementation (Coding)
**Goal:** Write the actual code.

### Step-by-Step Development Order:
1.  **Setup:** Initialize Git repository, set up Virtual Environment.
2.  **Backend - Models:** Create the Database Tables (`Users`, `Tasks`) using code.
3.  **Backend - Auth:** Write logic for Hashing passwords and generating Tokens.
4.  **Backend - CRUD:** Write API logic. *Crucial: Ensure every query filters by `user_id`.*
5.  **Frontend - Auth:** Create Login/Signup forms. Store the received Token in LocalStorage/Cookies.
6.  **Frontend - Dashboard:** Fetch data from API using the Token and display tasks.

---

## Phase 5: Testing
**Goal:** Find bugs before launch.

### Test Cases
1.  **Unit Testing:**
    * Does password hashing work?
    * Does the database reject a duplicate email?
2.  **Integration/Security Testing (Most Important):**
    * **The "Data Leak" Test:** Create User A and User B. Add tasks for User A. Login as User B. **Verify User B sees an empty list**, NOT User A's tasks.
    * **Access Control:** Try to delete a task without logging in. The system must say "401 Unauthorized".
3.  **UI Testing:**
    * Does the "Completed" filter correctly hide pending tasks?

---

## Phase 6: Deployment
**Goal:** Make the app live.

1.  **Database:** Set up a cloud database (e.g., Supabase, Neon, or AWS RDS).
2.  **Backend:** Deploy API to a cloud provider (e.g., Render, Railway, or AWS EC2).
3.  **Frontend:** Deploy UI to a static host (e.g., Vercel or Netlify).
4.  **Configuration:** Set Environment Variables (Database URL, Secret Keys) on the server.

---

## Phase 7: Maintenance
**Goal:** Updates and fixes after launch.

* **Monitor:** Check logs for failed login attempts or server errors.
* **Updates:** * *Feature Idea:* Add "Forgot Password" via email.
    * *Feature Idea:* Add specific "Due Dates" for tasks.