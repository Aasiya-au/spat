import mysql.connector
from datetime import datetime, timedelta, date, time
import traceback
import hashlib
import random
import requests
import os

def log_user_action(user_id, action, target_entity, target_id, timestamp, conn, cursor):
    print("Logging user action...")
    query = """
        SELECT id FROM target_entities WHERE entity_name = %s LIMIT 1
    """
    values = (target_entity.lower(), )
    cursor.execute(query, values)
    target_entity_id = cursor.fetchone().get('id')

    query = """
        SELECT id FROM actions WHERE action_name = %s LIMIT 1
    """
    values = (action.lower(), )
    cursor.execute(query, values)
    action_id = cursor.fetchone().get('id')

    print("log_user_action: ", user_id, action_id, target_entity_id, target_id, timestamp)

    query = """
        INSERT INTO action_logs 
        (user_id, action_id, target_entity_id, target_id, timestamp)
        VALUES (%s, %s, %s, %s, %s)
    """
    values = (user_id, action_id, target_entity_id, target_id, timestamp)

    cursor.execute(query, values)
    conn.commit()
    print(cursor.rowcount, "record(s) inserted.")

def log_error(message):
    # Automatically extract location from traceback if not given
    tb = traceback.extract_stack(limit = 3)[-2]
    full_path = tb.filename
    project_root = os.getcwd()  # Get the current working directory
    relative_path = os.path.relpath(full_path, project_root)
    location = f"{relative_path}:{tb.name}:{tb.lineno}"

    conn, cursor = connect()
    cursor.execute(
        "INSERT INTO error_logs (timestamp, location, message) VALUES (%s, %s, %s)",
        (datetime.now(), location, message)
    )
    conn.commit()
    close(conn, cursor)

def get_error_logs():   
    conn, cursor = connect()
    cursor.execute("SELECT * FROM error_logs ORDER BY timestamp DESC")
    error_logs = cursor.fetchall()
    close(conn, cursor)
    return error_logs

def get_action_logs():
    conn, cursor = connect()
    query = """
        SELECT * FROM action_log_view
    """
    cursor.execute(query)
    user_action_logs = cursor.fetchall()
    close(conn, cursor)
    return user_action_logs

def get_user_action_logs(identifier):
    conn, cursor = connect()
    try:
        try:
            user_id = int(identifier)  # Try to convert to integer for user_id
            query = """
                SELECT * FROM action_log_view
                WHERE user_id = %s
            """
            cursor.execute(query, (user_id,))
        except ValueError:
            # If not an integer, treat as username
            query = """
                SELECT * FROM action_log_view
                WHERE username = %s
            """
            cursor.execute(query, (identifier,))
        
        user_action_logs = cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        user_action_logs = []  # Return empty list on error
    finally:
        close(conn, cursor)
    return user_action_logs

def get_api_logs():
    conn, cursor = connect()
    cursor.execute("SELECT * FROM api_logs ORDER BY timestamp DESC")
    api_logs = cursor.fetchall()
    close(conn, cursor)
    return api_logs

def connect():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="spat"
    )
    cursor = conn.cursor(dictionary=True, buffered=True)
    return conn, cursor

def close(conn, cursor):
    cursor.close()
    conn.close()

def signup(username, email, password):
    conn, cursor = connect()
    try:
        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()
        if user:
            return "Email already exists"
        
        query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        if user:
            return "Username already exists"
        
        if len(password) < 8:
            return "Password must be at least 8 characters long"
        
        else:
            password = hashlib.sha256(password.encode()).hexdigest()
            query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s);"
            cursor.execute(query, (username, email, password))
            conn.commit()

            query = "SELECT * FROM users WHERE email = %s;"
            cursor.execute(query, (email,))
            user = cursor.fetchone()
            return user

    except Exception as e:
        log_error(str(e))
        return e

    finally:
        if conn and cursor:
            close(conn, cursor)

def login(username, password):
    conn, cursor = connect()

    try:
        password = hashlib.sha256(password.encode()).hexdigest() 
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password,))
        user = cursor.fetchone()

        if user:
            return user
        else:
            return "Invalid username or password"
    except Exception as e:
        log_error(str(e))
        return e
    finally:
        if conn and cursor:
            close(conn, cursor)

def get_user(identifier):
    conn, cursor = connect()

    try:
        if isinstance(identifier, int):
            query = "SELECT * FROM users WHERE id = %s"
        elif isinstance(identifier, str):
            query = "SELECT * FROM users WHERE username = %s"
        else:
            return None
        
        cursor.execute(query, (identifier,))
        user = cursor.fetchone()
        if user:
            return user
        else:
            return "Invalid username or password"
    except Exception as e:
        log_error(str(e))
        return e
    finally:
        if conn and cursor:
            close(conn, cursor)
        
def get_all_users():
    conn, cursor = connect()
    
    try:
        query = "SELECT username, total_study_points, RANK() OVER (ORDER BY total_study_points DESC) AS rank FROM users"
        cursor.execute(query)
        users = cursor.fetchall()
        return users
    except Exception as e:
        log_error(str(e))
        return e
    finally:
        if conn and cursor:
            close(conn, cursor)

def get_subjects(user_id):
    conn, cursor = connect()

    try:
        query = "SELECT * FROM subjects WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        subjects = cursor.fetchall()
        return subjects
    except Exception as e:
        log_error(str(e))
        return e
    finally:
        if conn and cursor:
            close(conn, cursor)

def add_subject(user_id, name):
    conn, cursor = connect()

    try:
        query = "INSERT INTO subjects (user_id, name) VALUES (%s, %s)"
        cursor.execute(query, (user_id, name,))
        conn.commit()
        query = "SELECT * FROM subjects WHERE user_id = %s AND name = %s ORDER BY id DESC LIMIT 1"
        cursor.execute(query, (user_id, name,))
        subjects = cursor.fetchall()
        #log_user_action(user_id, 'add', 'subjects', subjects['id'], datetime.now(), conn, cursor)
        return subjects
    except Exception as e:
        log_error(str(e))
        return e
    finally:
        if conn and cursor:
            close(conn, cursor)
    
def delete_subject(user_id, subject_id):
    conn, cursor = connect()

    try:
        query = "DELETE FROM subjects WHERE user_id = %s AND id = %s"
        cursor.execute(query, (user_id, subject_id,))
        conn.commit()
        query = "SELECT * FROM tasks WHERE user_id = %s AND subject_id = %s"
        cursor.execute(query, (user_id, subject_id,))
        tasks = cursor.fetchall()
        if tasks:
            query = "DELETE FROM tasks WHERE user_id = %s AND subject_id = %s"
            cursor.execute(query, (user_id, subject_id,))
            conn.commit()
        query = "SELECT * FROM topics WHERE user_id = %s AND subject_id = %s"
        cursor.execute(query, (user_id, subject_id,))
        topics = cursor.fetchall()
        if topics:
            query = "DELETE FROM topics WHERE user_id = %s AND subject_id = %s"
            cursor.execute(query, (user_id, subject_id,))
            conn.commit()
        query = "SELECT * FROM subjects WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        subjects = cursor.fetchall()
        #log_user_action(user_id, 'delete', 'subjects', subject_id, datetime.now(), conn, cursor)
        return subjects
    except Exception as e:
        log_error(str(e))
        return e
    finally:
        if conn and cursor:
            close(conn, cursor)
    
def complete_subject(user_id, subject_id):
    conn, cursor = connect()

    try:
        query = "UPDATE subjects SET status = 'Completed' WHERE user_id = %s AND id = %s"
        cursor.execute(query, (user_id, subject_id,))
        conn.commit()
        query = "SELECT * FROM subjects WHERE user_id = %s AND id = %s"
        cursor.execute(query, (user_id, subject_id,))
        subjects = cursor.fetchall()
        #log_user_action(user_id, 'update', 'subjects', subject_id, datetime.now(), conn, cursor)
        return subjects
    except Exception as e:
        log_error(str(e))
        return e
    finally:
        if conn and cursor:
            close(conn, cursor)
    
def update_subject(user_id, subject_id, name):
    conn, cursor = connect()

    try:
        query = "UPDATE subjects SET name = %s WHERE user_id = %s AND id = %s"
        cursor.execute(query, (name, user_id, subject_id,))
        conn.commit()
        query = "SELECT * FROM subjects WHERE user_id = %s AND id = %s"
        cursor.execute(query, (user_id, subject_id,))
        subject = cursor.fetchall()
        #log_user_action(user_id, 'update', 'subjects', subject_id, datetime.now(), conn, cursor)
        return subject
    except Exception as e:
        log_error(str(e))
        return e
    finally:
        if conn and cursor:
            close(conn, cursor)
    
def get_topics(user_id, subject_id):
    conn, cursor = connect()

    try:
        query = "SELECT * FROM topics WHERE user_id = %s AND subject_id = %s"
        cursor.execute(query, (user_id, subject_id,))
        topics = cursor.fetchall()
        return topics
    except Exception as e:
        #log_error(str(e))
        return False
    finally:
        if conn and cursor:
            close(conn, cursor)
    
def add_topic(user_id, subject_id, name, due_date):
    conn, cursor = connect()

    try:
        query = "INSERT INTO topics (user_id, subject_id, name, due_date) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (user_id, subject_id, name, due_date,))
        conn.commit()
        query = "SELECT * FROM topics WHERE user_id = %s AND subject_id = %s AND name = %s AND due_date = %s ORDER BY id DESC LIMIT 1"
        cursor.execute(query, (user_id, subject_id, name, due_date,))
        topic = cursor.fetchall()
        #log_user_action(user_id, 'add', 'topics', topic['id'], datetime.now(), conn, cursor)
        return topic
    except Exception as e:
        log_error(str(e))
        return e
    finally:
        if conn and cursor:
            close(conn, cursor)
    
def delete_topic(user_id, subject_id, topic_id):
    conn, cursor = connect()

    try:
        if topic_id is not None:
        # First delete all tasks associated with this topic
            query = "DELETE FROM tasks WHERE user_id = %s AND subject_id = %s AND topic_id = %s"
            cursor.execute(query, (user_id, subject_id, topic_id,))
            conn.commit()
            
            # Then delete the topic
            query = "DELETE FROM topics WHERE user_id = %s AND subject_id = %s AND id = %s"
            cursor.execute(query, (user_id, subject_id, topic_id,))
            conn.commit()
            
            query = "SELECT * FROM topics WHERE user_id = %s AND subject_id = %s"
            cursor.execute(query, (user_id, subject_id,))
            topics = cursor.fetchall()
            #log_user_action(user_id, 'delete', 'topics', topic_id, datetime.now(), conn, cursor)
        return topics
    except Exception as e:
        log_error(str(e))
        return e
    finally:
        if conn and cursor:
            close(conn, cursor)
    
def update_topic(user_id, subject_id, topic_id, name, due_date):
    conn, cursor = connect()

    try:
        query = "UPDATE topics SET name = %s, due_date = %s, subject_id = %s WHERE user_id = %s AND id = %s"
        cursor.execute(query, (name, due_date, subject_id, user_id, topic_id,))
        conn.commit()
        query = "SELECT * FROM topics WHERE user_id = %s AND subject_id = %s"
        cursor.execute(query, (user_id, subject_id,))
        topics = cursor.fetchall()
        #log_user_action(user_id, 'update', 'topics', topic_id, datetime.now(), conn, cursor)
        return topics
    except Exception as e:
        log_error(str(e))
        return e
    finally:
        if conn and cursor:
            close(conn, cursor)
    
def complete_topic(user_id, subject_id, topic_id):
    conn, cursor = connect()

    try:
        query = "UPDATE topics SET status = 'Completed' WHERE user_id = %s AND subject_id = %s AND id = %s"
        cursor.execute(query, (user_id, subject_id, topic_id,))
        query = "UPDATE users SET total_topics_completed = total_topics_completed + 1 WHERE id = %s"
        cursor.execute(query, (user_id,))
        conn.commit()
        query = "SELECT * FROM topics WHERE user_id = %s AND subject_id = %s AND id = %s"
        cursor.execute(query, (user_id, subject_id, topic_id,))
        topic = cursor.fetchall()
        #log_user_action(user_id, 'update', 'topics', topic_id, datetime.now(), conn, cursor)
        return topic
    except Exception as e:
        log_error(str(e))
        return e
    finally:
        if conn and cursor:
            close(conn, cursor)

def get_tasks(user_id, subject_id, topic_id=None):
    conn, cursor = connect()

    try:
        if topic_id is None:
            # Get tasks for the subject (where topic_id is NULL)
            query = "SELECT * FROM tasks WHERE user_id = %s AND subject_id = %s AND topic_id IS NULL"
            cursor.execute(query, (user_id, subject_id,))
        else:
            # Get tasks for the specific topic
            query = "SELECT * FROM tasks WHERE user_id = %s AND subject_id = %s AND topic_id = %s"
            cursor.execute(query, (user_id, subject_id, topic_id,))
            
        tasks = cursor.fetchall()
        return tasks
    except Exception as e:
        log_error(str(e))
        return e
    finally:
        if conn and cursor:
            close(conn, cursor)

def add_task(user_id, subject_id, name, due_date, topic_id=None):
    conn, cursor = connect()

    try:
        if topic_id is None:
            # Add task for the subject (topic_id is NULL)
            query = "INSERT INTO tasks (user_id, subject_id, title, due_date) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (user_id, subject_id, name, due_date,))
        else:
            # Add task for the specific topic
            query = "INSERT INTO tasks (user_id, subject_id, topic_id, title, due_date) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (user_id, subject_id, topic_id, name, due_date,))
            
        conn.commit()
        
        if topic_id is None:
            # Retrieve the newly added subject task
            query = "SELECT * FROM tasks WHERE user_id = %s AND subject_id = %s AND title = %s AND due_date = %s AND topic_id IS NULL ORDER BY id DESC LIMIT 1"
            cursor.execute(query, (user_id, subject_id, name, due_date,))
        else:
            # Retrieve the newly added topic task
            query = "SELECT * FROM tasks WHERE user_id = %s AND subject_id = %s AND topic_id = %s AND title = %s AND due_date = %s ORDER BY id DESC LIMIT 1"
            cursor.execute(query, (user_id, subject_id, topic_id, name, due_date,))
            
        task = cursor.fetchall()
        #log_user_action(user_id, 'add', 'tasks', task['id'], datetime.now(), conn, cursor)
        return task
    except Exception as e:
        log_error(str(e))
        return e
    finally:
        if conn and cursor:
            close(conn, cursor)
    
def update_task(user_id, subject_id, task_id, name, due_date, topic_id=None):
    conn, cursor = connect()

    try:
        if topic_id is None:
            # Update task for subject (topic_id remains NULL)
            query = "UPDATE tasks SET title = %s, due_date = %s, topic_id = NULL WHERE user_id = %s AND subject_id = %s AND id = %s"
            cursor.execute(query, (name, due_date, user_id, subject_id, task_id,))
        else:
            # Update task for topic
            query = "UPDATE tasks SET title = %s, due_date = %s, topic_id = %s WHERE user_id = %s AND subject_id = %s AND id = %s"
            cursor.execute(query, (name, due_date, topic_id, user_id, subject_id, task_id,))
            
        conn.commit()
        query = "SELECT * FROM tasks WHERE user_id = %s AND subject_id = %s AND id = %s"
        cursor.execute(query, (user_id, subject_id, task_id,))
        task = cursor.fetchall()
        #log_user_action(user_id, 'update', 'tasks', task_id, datetime.now(), conn, cursor)
        return task
    except Exception as e:
        log_error(str(e))
        return e
    finally:
        if conn and cursor:
            close(conn, cursor)
    
def delete_task(user_id, subject_id, task_id, topic_id=None):
    conn, cursor = connect()

    try:
        query = "DELETE FROM tasks WHERE user_id = %s AND subject_id = %s AND id = %s"
        cursor.execute(query, (user_id, subject_id, task_id,))
        conn.commit()
        
        if topic_id is None:
            # Get remaining subject tasks (where topic_id is NULL)
            query = "SELECT * FROM tasks WHERE user_id = %s AND subject_id = %s AND topic_id IS NULL"
            cursor.execute(query, (user_id, subject_id,))
        else:
            # Get remaining tasks for the specific topic
            query = "SELECT * FROM tasks WHERE user_id = %s AND subject_id = %s AND topic_id = %s"
            cursor.execute(query, (user_id, subject_id, topic_id,))
            
        tasks = cursor.fetchall()
        #log_user_action(user_id, 'delete', 'tasks', task_id, datetime.now(), conn, cursor)
        return tasks
    except Exception as e:
        log_error(str(e))
        return e
    finally:
        if conn and cursor:
            close(conn, cursor)
    
def complete_task(user_id, subject_id, task_id, topic_id=None):
    conn, cursor = connect()

    try:
        if topic_id is None:
            query = "UPDATE tasks SET status = 'Completed' WHERE user_id = %s AND subject_id = %s AND id = %s"
            cursor.execute(query, (user_id, subject_id, task_id,))
            query = "UPDATE users SET total_tasks_completed = total_tasks_completed + 1 WHERE id = %s"
            cursor.execute(query, (user_id,))
            conn.commit()
        else:
            query = "UPDATE tasks SET status = 'Completed' WHERE user_id = %s AND subject_id = %s AND id = %s AND topic_id = %s"
            cursor.execute(query, (user_id, subject_id, task_id,topic_id,))
            query = "UPDATE users SET total_tasks_completed = total_tasks_completed + 1 WHERE id = %s"
            cursor.execute(query, (user_id,))
            conn.commit()
        if topic_id is None:
            # Get completed subject task (where topic_id is NULL)
            query = "SELECT * FROM tasks WHERE user_id = %s AND subject_id = %s AND id = %s AND topic_id IS NULL"
            cursor.execute(query, (user_id, subject_id, task_id,))
        else:
            # Get completed topic task
            query = "SELECT * FROM tasks WHERE user_id = %s AND subject_id = %s AND id = %s AND topic_id = %s"
            cursor.execute(query, (user_id, subject_id, task_id, topic_id,))
            
        task = cursor.fetchall()
        #log_user_action(user_id, 'update', 'tasks', task_id, datetime.now(), conn, cursor)
        return task
    except Exception as e:
        log_error(str(e))
        return e
    finally:
        if conn and cursor:
            close(conn, cursor)

def get_notes(user_id):
    conn, cursor = connect()

    try:
        query = "SELECT * FROM notes WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        notes = cursor.fetchall()
        return notes
    except Exception as e:
        log_error(str(e))
        return e
    finally:
        if conn and cursor:
            close(conn, cursor)
    
def add_note(user_id, title, content):
    conn, cursor = connect()

    try:
        query = "INSERT INTO notes (user_id, title, content) VALUES (%s, %s, %s)"
        cursor.execute(query, (user_id, title, content,))
        conn.commit()
        query = "SELECT * FROM notes WHERE user_id = %s AND title = %s AND content = %s ORDER BY id DESC LIMIT 1"
        cursor.execute(query, (user_id, title, content,))
        note = cursor.fetchall()
        #THE FETCHALL CHANGE
        log_user_action(user_id, 'add', 'notes', note['id'], datetime.now(), conn, cursor)
        return note
    except Exception as e:
        log_error(str(e))
        return e
    finally:
        if conn and cursor:
            close(conn, cursor)
    
def delete_note(user_id, note_id):
    conn, cursor = connect()

    try:
        query = "DELETE FROM notes WHERE user_id = %s AND id = %s"
        cursor.execute(query, (user_id, note_id,))
        conn.commit()
        query = "SELECT * FROM notes WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        notes = cursor.fetchall()
        log_user_action(user_id, 'delete', 'notes', note_id, datetime.now(), conn, cursor)
        close(conn, cursor)
        return notes
    except Exception as e:
        log_error(str(e))
        return False
    finally:
        if conn and cursor:
            close(conn, cursor)
    
def update_note(user_id, note_id, title, content):
    conn, cursor = connect()

    try:
        query = "UPDATE notes SET title = %s, content = %s WHERE user_id = %s AND id = %s"
        cursor.execute(query, (title, content, user_id, note_id,))
        conn.commit()
        query = "SELECT * FROM notes WHERE user_id = %s AND id = %s"
        cursor.execute(query, (user_id, note_id,))
        note = cursor.fetchall()
        #THE FETCHALL CHANGE
        log_user_action(user_id, 'update', 'notes', note_id, datetime.now(), conn, cursor)
        return note
    except Exception as e:
        log_error(str(e))
        return e
    finally:
        if conn and cursor:
            close(conn, cursor)

def get_study_points(user_id):
    conn, cursor = connect()

    try:
        query = "SELECT total_study_points FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))
        study_points = cursor.fetchall()
        close(conn, cursor)
        return study_points
    except Exception as e:
        log_error(str(e))
        return e
    finally:
        if conn and cursor:
            close(conn, cursor)

def add_study_points(user_id, points):
    conn, cursor = connect()

    try:
        query = "UPDATE users SET total_study_points = total_study_points + %s WHERE id = %s"
        cursor.execute(query, (points, user_id,))
        conn.commit()
        query = "SELECT total_study_points FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))
        study_points = cursor.fetchall()
        return study_points
    except Exception as e:
        log_error(str(e))
        return e
    finally:
        if conn and cursor:
            close(conn, cursor)

def get_achievements(user_id):
    conn, cursor = connect()

    try:
        query = """
            SELECT a.name, a.description
            FROM achievements a
            JOIN user_achievements ua ON a.id = ua.achievement_id
            WHERE ua.user_id = %s
        """
        cursor.execute(query, (user_id,))
        achievements = cursor.fetchall()
        close (conn, cursor)
        return achievements
    except Exception as e:
        log_error(str(e))
        return e
    finally:
        if conn and cursor:
            close(conn, cursor)

def get_user_achievements(user_id):
    conn, cursor = connect()

    try:
        query = "SELECT * FROM user_achievements WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        achievements = cursor.fetchall()
        return achievements
    except Exception as e:
        log_error(str(e))
        return e
    finally:
        if conn and cursor:
            close(conn, cursor)

def add_user_achievement(user_id):
    conn, cursor = connect()

    try:
        query = '''
        INSERT IGNORE INTO user_achievements (user_id, achievement_id, achieved_at)
        SELECT %s, achievements.id, NOW()
        FROM achievements
        WHERE (condition_type = 'points' AND condition_value <= (SELECT total_study_points FROM users WHERE id = %s))
           OR (condition_type = 'tasks' AND condition_value <= (SELECT total_tasks_completed FROM users WHERE id = %s))
           OR (condition_type = 'topics' AND condition_value <= (SELECT total_topics_completed FROM users WHERE id = %s))
        AND NOT EXISTS (
            SELECT 1 FROM user_achievements
            WHERE user_id = %s AND achievement_id = achievements.id
        );
        '''
        cursor.execute(query, (user_id, user_id, user_id, user_id, user_id))
        conn.commit()

        # Retrieve the latest achievement(s) added
        query = "SELECT * FROM user_achievements WHERE user_id = %s ORDER BY achieved_at DESC"
        cursor.execute(query, (user_id,))
        newest_achievements = cursor.fetchall()
        return newest_achievements
    except Exception as e:
        log_error(str(e))
        return e
    finally:
        if conn and cursor:
            close(conn, cursor)

def get_study_sessions(user_id):
    conn, cursor = connect()
    try:
        query = "SELECT DAY(date), HOUR(start_time), HOUR(end_time) FROM study_sessions WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        study_sessions = cursor.fetchall()
        return study_sessions
    except Exception as e:
        log_error(str(e))
        return e
    finally:
        if conn and cursor:
            close(conn, cursor)

def get_all_themes():
    conn, cursor = connect()
    try:
        cursor.execute("SELECT id, color_1, color_2, color_3, color_4 FROM themes")
        themes = cursor.fetchall()
        return themes
    except Exception as e:
        log_error(str(e))
        return e
    finally:
        if conn and cursor:
            close(conn, cursor)

def get_user_theme(user_id):
    conn, cursor = connect()
    try:
        query = """
        SELECT t.id, t.color_1, t.color_2, t.color_3, t.color_4 
        FROM themes t
        JOIN user_theme ut ON t.id = ut.theme_id
        WHERE ut.user_id = %s
        """
        cursor.execute(query, (user_id,))
        theme = cursor.fetchone()
        
        # If no theme is set, return the first theme as default
        if not theme:
            cursor.execute("SELECT id, color_1, color_2, color_3, color_4 FROM themes LIMIT 1")
            theme = cursor.fetchone()
        return theme
    except Exception as e:
        log_error(str(e))
        return e
    finally:
        if conn and cursor:
            close(conn, cursor)

def set_user_theme(user_id, theme_id):
    conn, cursor = connect()
    try:
        cursor.execute("SELECT 1 FROM user_theme WHERE user_id = %s", (user_id,))
        exists = cursor.fetchone()

        if exists:
            query = "UPDATE user_theme SET theme_id = %s WHERE user_id = %s"
            cursor.execute(query, (theme_id, user_id))
        else:
            query = "INSERT INTO user_theme (user_id, theme_id) VALUES (%s, %s)"
            cursor.execute(query, (user_id, theme_id))

        conn.commit()
        success = True
    except mysql.connector.Error as e:
        success = False
        log_error(str(e))
    finally:
        close(conn, cursor)
    
    return success

def get_all_characters():
    conn, cursor = connect()
    try:
        cursor.execute("SELECT id, name FROM characters")
        characters = cursor.fetchall()
        return characters
    except Exception as e:
        log_error(str(e))
        return e
    finally:
        if conn and cursor:
            close(conn, cursor)

def get_user_character(user_id):
    conn, cursor = connect()
    try:
        query = """
        SELECT c.id, c.name 
        FROM characters c
        JOIN user_character uc ON c.id = uc.character_id
        WHERE uc.user_id = %s
        """
        cursor.execute(query, (user_id,))
        character = cursor.fetchone()

        if not character:
            cursor.execute("SELECT id,name FROM characters LIMIT 1")
            character = cursor.fetchone()
        return character
    except Exception as e:
        log_error(str(e))
        return e
    finally:
        if conn and cursor:
            close(conn, cursor)

def set_user_character(user_id, character_id):
    conn, cursor = connect()
    try:
        cursor.execute("SELECT 1 FROM user_character WHERE user_id = %s", (user_id,))
        exists = cursor.fetchone()

        if exists:
            query = "UPDATE user_character SET character_id = %s WHERE user_id = %s"
            cursor.execute(query, (character_id, user_id))
        else:
            query = "INSERT INTO user_character (user_id, character_id) VALUES (%s, %s)"
            cursor.execute(query, (user_id, character_id))

        conn.commit()
        success = True
    except mysql.connector.Error as e:
        log_error(str(e))
        success = False
    finally:
        close(conn, cursor)
    
    return success

def get_flashcards_by_subject(user_id, subject_id):
    conn, cursor = connect()
    try:
        query = "SELECT * FROM flashcards WHERE user_id = %s AND subject_id = %s"
        cursor.execute(query, (user_id, subject_id))
        flashcards = cursor.fetchall()
        return flashcards
    except Exception as e:
        log_error(str(e))
        return e
    finally:
        if conn and cursor:
            close(conn, cursor)

def get_all_flashcards(user_id):
    conn, cursor = connect()
    try:
        query = "SELECT * FROM flashcards WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        flashcards = cursor.fetchall()
        return flashcards
    except Exception as e:
        log_error(str(e))
        return e
    finally:
        if conn and cursor:
            close(conn, cursor)

def add_flashcard(user_id, subject_id, question, answer):
    conn, cursor = connect()
    try:
        query = "INSERT INTO flashcards (user_id, subject_id, question, answer) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (user_id, subject_id, question, answer))
        conn.commit()
        query = "SELECT * FROM flashcards WHERE user_id = %s AND subject_id = %s AND question = %s AND answer = %s ORDER BY id DESC LIMIT 1"
        cursor.execute(query, (user_id, subject_id, question, answer))
        flashcard = cursor.fetchone()
        log_user_action(user_id, 'add', 'flashcards', flashcard['id'], datetime.now(), conn, cursor)

        return flashcard
    except Exception as e:
        log_error(str(e))
        return e
    finally:
        if conn and cursor:
            close(conn, cursor)

def update_flashcard(user_id, flashcard_id, question, answer):
    conn, cursor = connect()
    try:
        query = "UPDATE flashcards SET question = %s, answer = %s WHERE id = %s AND user_id = %s"
        cursor.execute(query, (question, answer, flashcard_id, user_id))
        conn.commit()
        query = "SELECT * FROM flashcards WHERE id = %s AND user_id = %s"
        cursor.execute(query, (flashcard_id, user_id))
        flashcard = cursor.fetchone()
        log_user_action(user_id, 'update', 'flashcards', flashcard_id, datetime.now(), conn, cursor)
        return flashcard
    except Exception as e:
        log_error(str(e))
        return e
    finally:
        if conn and cursor:
            close(conn, cursor)

def delete_flashcard(user_id, flashcard_id):
    conn, cursor = connect()
    try:
        query = "DELETE FROM flashcards WHERE id = %s AND user_id = %s"
        cursor.execute(query, (flashcard_id, user_id))
        conn.commit()
        query = "SELECT * FROM flashcards WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        flashcards = cursor.fetchall()
        log_user_action(user_id, 'delete', 'flashcards', flashcard_id, datetime.now(), conn, cursor)
        return flashcards
    except Exception as e:
        log_error(str(e))
        return e
    finally:
        if conn and cursor:
            close(conn, cursor)
    
def get_daily_challenges():
    conn, cursor = connect()
    try:
        today = date.today()
        query = "SELECT challenge_id FROM daily_challenge_selection WHERE selection_date = %s"
        cursor.execute(query, (today,))
        result = cursor.fetchone()
        
        if result:
            challenge_id = result['challenge_id']
            query = "SELECT * FROM challenges WHERE challenge_id = %s"
            cursor.execute(query, (challenge_id,))
            challenge = cursor.fetchone()
            return [challenge] if challenge else []

        query = "SELECT challenge_id FROM challenges"
        cursor.execute(query)
        challenge_ids = [row['challenge_id'] for row in cursor.fetchall()]
        
        if not challenge_ids:
            return []

        selected_challenge_id = random.choice(challenge_ids)
        query = "INSERT INTO daily_challenge_selection (selection_date, challenge_id) VALUES (%s, %s)"
        cursor.execute(query, (today, selected_challenge_id))
        conn.commit()

        query = "SELECT * FROM challenges WHERE challenge_id = %s"
        cursor.execute(query, (selected_challenge_id,))
        challenge = cursor.fetchone()
        return [challenge] if challenge else []

    except Exception as e:
        log_error(str(e))
        return []
    finally:
        if conn and cursor:
            close(conn, cursor)

def mark_challenge_completed(user_id, challenge_id, completed_date):
    conn, cursor = connect()
    try:
        query = "SELECT * FROM user_challenges WHERE user_id = %s AND challenge_id = %s AND completed_date = %s"
        cursor.execute(query, (user_id, challenge_id, completed_date))
        if cursor.fetchone():
            return "Challenge already completed today"

        query = "INSERT INTO user_challenges (user_id, challenge_id, completed_date) VALUES (%s, %s, %s)"
        cursor.execute(query, (user_id, challenge_id, completed_date))
        conn.commit()

        return True
    except Exception as e:
        log_error(str(e))
        return str(e)
    finally:
        if conn and cursor:
            close(conn, cursor)

def add_study_points(user_id, points):
    conn, cursor = connect()
    try:
        query = "UPDATE users SET total_study_points = total_study_points + %s WHERE id = %s"
        cursor.execute(query, (points, user_id))
        conn.commit()
        return True
    except Exception as e:
        log_error(str(e))
        return False
    finally:
        if conn and cursor:
            close(conn, cursor)

def is_challenge_completed(user_id, challenge_id):
    conn, cursor = connect()
    try:
        today = date.today()
        query = "SELECT * FROM user_challenges WHERE user_id = %s AND challenge_id = %s AND completed_date = %s"
        cursor.execute(query, (user_id, challenge_id, today))
        result = cursor.fetchone()
        return result is not None
    except Exception as e:
        log_error(str(e))
        return False
    finally:
        if conn and cursor:
            close(conn, cursor)

def get_app():
    conn, cursor = connect()

    try:
        query = "SELECT * FROM apps"
        cursor.execute(query)
        app = cursor.fetchone()
        return app
    except Exception as e:
        log_error(str(e))
        return e
    finally:
        if conn and cursor:
            close(conn, cursor)

def get_panels(app_id):
    conn, cursor = connect()

    try:
        query = "SELECT * FROM app_panels WHERE app_id = %s"
        cursor.execute(query, (app_id,))
        panels = cursor.fetchall()
        return panels
    except Exception as e:
        log_error(str(e))
        return e
    finally:
        if conn and cursor:
            close(conn, cursor)

def get_resources(app_id):
    conn, cursor = connect()

    try:
        query = "SELECT * FROM app_resources WHERE app_id = %s"
        cursor.execute(query, (app_id,))
        resources = cursor.fetchall()
        return resources
    except Exception as e:
        log_error(str(e))
        return e
    finally:
        if conn and cursor:
            close(conn, cursor)

def get_developer(name):
    conn, cursor = connect()
    try:
        query = "SELECT * FROM developers WHERE name = %s"
        cursor.execute(query, (name,))
        developer = cursor.fetchone()
        if developer:
            return developer
        else:
            return "Invalid name"
    except Exception as e:
        log_error(str(e))
        return e
    finally:
        close(conn, cursor)

def get_developers():
    conn, cursor = connect()
    try:
        query = """
            SELECT developers.id, developers.name, developers.email, developer_roles.role_name, developer_roles.description
            FROM developers
            JOIN developer_roles ON developers.role_id = developer_roles.id
        """
        cursor.execute(query)
        developers = cursor.fetchall()
        return developers
    except Exception as e:
        log_error(str(e))
        return e
    finally:
        if conn and cursor:
            close(conn, cursor)

def start_study_session(user_id, start_time, session_date):
    conn, cursor = connect()
    try:
        query = "INSERT INTO study_sessions (user_id, start_time, date) VALUES (%s, %s, %s)"
        cursor.execute(query, (user_id, start_time, session_date,))
        conn.commit()
        query = "SELECT * FROM study_sessions WHERE user_id = %s AND date = %s AND start_time = %s ORDER BY id DESC LIMIT 1"
        cursor.execute(query, (user_id, session_date, start_time,))
        study_session = cursor.fetchone()
        log_user_action(user_id, 'add', 'study_sessions', study_session['id'], datetime.now(), conn, cursor)
        return study_session
    except Exception as e:
        log_error(str(e))
        return e
    finally:
        if conn and cursor:
            close(conn, cursor)

def end_study_session(started_session, end_time, duration, duration_in_min):
    conn, cursor = connect()
    try:
        
        query = "UPDATE study_sessions SET end_time = %s, duration = %s, duration_in_min = %s WHERE user_id = %s AND date = %s AND end_time IS NULL ORDER BY start_time DESC LIMIT 1"
        cursor.execute(query, (end_time, duration, duration_in_min, started_session["user_id"], started_session["date"]))
        conn.commit()
        
        query = "SELECT * FROM study_sessions WHERE user_id = %s AND date = %s ORDER BY start_time DESC LIMIT 1" 
        cursor.execute(query, (started_session["user_id"], started_session["date"]))
        study_session = cursor.fetchone()
        
        add_study_points(started_session["user_id"], duration) 
        return study_session

    except Exception as e:
        log_error(str(e))
        return e
    finally:
        if conn and cursor:
            close(conn, cursor)

def count_users():
    conn, cursor = connect()
    try:
        query = "SELECT COUNT(*) as user_count FROM users"
        cursor.execute(query)
        user_count = cursor.fetchone()
        return user_count
    except Exception as e:
        log_error(str(e))
        return e
    finally:
        if conn and cursor:
            close(conn, cursor)

def count_study_sessions():
    conn, cursor = connect()
    try:
        query = "SELECT COUNT(*) as session_count FROM study_sessions"
        cursor.execute(query)
        session_count = cursor.fetchone()
        return session_count
    except Exception as e:
        log_error(str(e))
        return e
    finally:
        if conn and cursor:
            close(conn, cursor)

def count_flashcards():
    conn, cursor = connect()
    try:
        query = "SELECT COUNT(*) as flashcard_count FROM flashcards"
        cursor.execute(query)
        flashcard_count = cursor.fetchone()
        return flashcard_count
    except Exception as e:
        log_error(str(e))
        return e
    finally:
        if conn and cursor:
            close(conn, cursor)

def count_notes():
    conn, cursor = connect()
    try:
        query = "SELECT COUNT(*) as note_count FROM notes"
        cursor.execute(query)
        note_count = cursor.fetchone()
        return note_count
    except Exception as e:
        log_error(str(e))
        return e
    finally:
        if conn and cursor:
            close(conn, cursor)

def count_tasks():
    conn, cursor = connect()
    try:
        query = "SELECT COUNT(*) as task_count FROM tasks"
        cursor.execute(query)
        task_count = cursor.fetchone()
        return task_count
    except Exception as e:
        log_error(str(e))
        return e
    finally:
        if conn and cursor:
            close(conn, cursor)

def count_achievements():
    conn, cursor = connect()
    try:
        query = "SELECT COUNT(*) as achievement_count FROM achievements"
        cursor.execute(query)
        achievement_count = cursor.fetchone()
        return achievement_count
    except Exception as e:
        log_error(str(e))
        return e
    finally:
        if conn and cursor:
            close(conn, cursor)

def count_subjects():
    conn, cursor = connect()
    try:
        query = "SELECT COUNT(*) as subject_count FROM subjects"
        cursor.execute(query)
        subject_count = cursor.fetchone()
        return subject_count
    except Exception as e:
        log_error(str(e))
        return e
    finally:
        if conn and cursor:
            close(conn, cursor)

def count_topics():
    conn, cursor = connect()
    try:
        query = "SELECT COUNT(*) as topic_count FROM topics"
        cursor.execute(query)
        topic_count = cursor.fetchone()
        return topic_count
    except Exception as e:
        log_error(str(e))
        return e
    finally:
        if conn and cursor:
            close(conn, cursor)

def count_user_achievements(user_id):
    conn, cursor = connect()
    try:
        query = "SELECT COUNT(*) as user_achievement_count FROM user_achievements WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        user_achievement_count = cursor.fetchone()
        return user_achievement_count
    except Exception as e:
        log_error(str(e))
        return e
    finally:
        if conn and cursor:
            close(conn, cursor)

def init_quotes_table():
    conn, cursor = connect()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS daily_quotes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                date DATE NOT NULL,
                quote TEXT NOT NULL,
                author TEXT NOT NULL
            )
        """)
        conn.commit()
        return True
    except Exception as e:
        log_error(str(e))
        return e
    finally:
        if conn and cursor:
            close(conn, cursor)

def cleanup_old_quotes():
    conn, cursor = connect()
    try:
        thirty_days_ago = date.today() - timedelta(days=30)
        cursor.execute("DELETE FROM daily_quotes WHERE date < %s", (thirty_days_ago,))
        conn.commit()
        return True
    except Exception as e:
        log_error(str(e))
        return e
    finally:
        if conn and cursor:
            close(conn, cursor)

def fetch_quote_from_api():
    conn, cursor = connect()
    today = date.today()

    try:
        # Try to get today's quote from DB
        cursor.execute("SELECT quote, author FROM daily_quotes WHERE date = %s", (today,))
        result = cursor.fetchone()
        if result:
            return result['quote'], result['author']

        # Clean up old entries
        cleanup_old_quotes()

        # Fetch new quote
        url = "https://zenquotes.io/api/today"
        try:
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()

                if isinstance(data, list) and data and "q" in data[0] and "a" in data[0]:
                    quote, author = data[0]["q"], data[0]["a"]

                    cursor.execute(
                        "INSERT INTO daily_quotes (date, quote, author) VALUES (%s, %s, %s)",
                        (today, quote, author)
                    )
                    conn.commit()
                    return quote, author
                else:
                    print("Invalid API response format")

            else:
                print("API request failed")

        except requests.exceptions.RequestException as e:
            print(f"API request error: {e}")

        # Fallback: return the latest quote in DB
        cursor.execute("SELECT quote, author FROM daily_quotes ORDER BY date DESC LIMIT 1")
        fallback = cursor.fetchone()
        if fallback:
            print("Using fallback quote from database")
            return fallback['quote'], fallback['author']

        print("No quote found, using default")
        return "Failed to fetch quote", "Unknown"

    except Exception as e:
        log_error(str(e))
        return str(e), "Unknown"
    finally:
        if conn and cursor:
            close(conn, cursor)

def get_user_subject_overview(user_id):
    conn, cursor = connect()
    try:
        query = "SELECT * FROM user_subject_overview WHERE user_id = %s"
        cursor.execute(query, (user_id, user_id, user_id))
        subjects = cursor.fetchall()
        close(conn, cursor)
        return subjects

    except Exception as e:
        log_error(str(e))  # Automatically logs file, function, line
        close(conn, cursor)
        return e

def save_message(user_id, user_query, ai_response):
    conn, cursor = connect()
    if not conn or not cursor:
        return "Failed to connect to database"

    try:
        # Get current timestamp
        timestamp = datetime.now()
        
        # Insert the message
        query = "INSERT INTO chat_history (user_id, timestamp, user_query, ai_response) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (user_id, timestamp, user_query, ai_response))
        conn.commit()
        return None  # Return None on success

    except mysql.connector.Error as e:
        log_error(str(e))
        return f"Database error: {str(e)}"
    finally:
        if conn and cursor:
            close(conn, cursor)

def load_user_chat(user_id):
    conn, cursor = connect()
    if not conn or not cursor:
        print("Database connection failed")
        return []

    try:
        query = "SELECT user_query, ai_response FROM chat_history WHERE user_id = %s ORDER BY timestamp ASC"
        cursor.execute(query, (user_id,))

        rows = cursor.fetchall()
        return rows

    except mysql.connector.Error as e:
        log_error(str(e))
        return []
    finally:
        if conn and cursor:
            close(conn, cursor)

def load_history(user_id):
    conn, cursor = connect()
    if not conn or not cursor:
        print("Database connection failed")
        return []

    try:
        query = "SELECT timestamp, user_query, ai_response FROM chat_history WHERE user_id = %s ORDER BY timestamp DESC"
        cursor.execute(query, (user_id,))
        
        # Fetch all results
        all_rows = cursor.fetchall()
        
        # Filter out the initial greeting
        filtered_rows = [(timestamp, query, response) for timestamp, query, response in all_rows if query != "Initial greeting"]

        return filtered_rows

    except mysql.connector.Error as e:
        log_error(str(e))
        return []
    finally:
        if conn and cursor:
            close(conn, cursor)

def delete_history(user_id):
    conn, cursor = connect()
    if not conn or not cursor:
        return "Failed to connect to database"

    try:
        query = "DELETE FROM chat_history WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        conn.commit()
        return None  # Return None on success
    except mysql.connector.Error as e:
        log_error(str(e))
        return f"Database error: {str(e)}"
    finally:
        if conn and cursor:
            close(conn, cursor)

def get_user_chat(user_id):
    conn, cursor = connect()
    try:
        query = "SELECT user_query, ai_response FROM chat_history WHERE user_id = %s ORDER BY timestamp ASC"
        cursor.execute(query, (user_id,))
        history = cursor.fetchall()
        return history[1:]
    except Exception as e:
        log_error(str(e))
        return False
    finally:
        if conn and cursor:
            close(conn, cursor)

def log_api_call(api_endpoint, request_data, response_status, response_time, error_message=None, user_id=None):
    conn, cursor = connect()

    try:
        query = """
            INSERT INTO api_logs (api_endpoint, request_data, response_status, response_time, error_message, user_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (api_endpoint, request_data, response_status, response_time, error_message, user_id))
        conn.commit()

    except Exception as e:
        print(f"Error logging API call: {e}")
    finally:
        close(conn, cursor)

def log_user_login(user_id):
    """Log a user's login date."""
    conn, cursor = connect()
    if conn is None or cursor is None:
        print("Failed to establish database connection")
        return False
    try:
        login_date = date.today()
        query = "INSERT IGNORE INTO logins (user_id, login_date) VALUES (%s, %s)"
        cursor.execute(query, (user_id, login_date))
        conn.commit()
    except mysql.connector.Error as e:
        print(f"Error logging login: {e}")
        return e
    finally:
        close(conn, cursor)
    return True

def get_login_streak(user_id):
    conn, cursor = connect()
    if conn is None or cursor is None:
        return 0, []
    try:
        query = "SELECT login_date FROM logins WHERE user_id = %s ORDER BY login_date DESC"
        cursor.execute(query, (user_id,))
        dates = [row['login_date'] for row in cursor.fetchall()]
        if not dates:
            return 0, []
        streak = 0
        today = date.today()
        current = today
        while current in dates:
            streak += 1
            current -= timedelta(days=1)
        return streak, dates
    except mysql.connector.Error as e:
        print(f"Error getting streak: {e}")
        return 0, []
    finally:
        close(conn, cursor)
        
def get_login_dates_for_month(user_id, year, month):
    conn, cursor = connect()
    if conn is None or cursor is None:
        return []
    try:
        query = """
            SELECT login_date FROM logins
            WHERE user_id = %s AND YEAR(login_date) = %s AND MONTH(login_date) = %s
        """
        cursor.execute(query, (user_id, year, month))
        login_dates = [row['login_date'] for row in cursor.fetchall()]
        return login_dates
    except mysql.connector.Error as e:
        print(f"Error getting login dates: {e}")
        return []
    finally:
        close(conn, cursor)

def get_user_logins(identifier):
    conn, cursor = connect()
    if conn is None or cursor is None:
        return []
    try:
        query = "SELECT * FROM logins_view WHERE user_id = %s OR username = %s"
        cursor.execute(query, (identifier, identifier))
        logins = cursor.fetchall()
        return logins
    except mysql.connector.Error as e:
        print(f"Error getting logins: {e}")
        return []
    finally:
        close(conn, cursor)

def get_logins():
    conn, cursor = connect()
    if conn is None or cursor is None:
        return []
    try:
        query = "SELECT * FROM logins_view"
        cursor.execute(query)
        logins = cursor.fetchall()
        return logins
    except mysql.connector.Error as e:
        print(f"Error getting logins: {e}")
        return []
    finally:
        close(conn, cursor)