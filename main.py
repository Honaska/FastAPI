import React, { useState, useEffect } from "react";
import axios from "axios"; // ✅ added for API calls
import "./index.css";

// ✅ Set your FastAPI backend base URL here
const API_BASE_URL = "https://your-fastapi-render-url.onrender.com";

export default function TodoList() {
    const [tasks, setTasks] = useState([]);
    const [showForm, setShowForm] = useState(false);
    const [newTask, setNewTask] = useState({ title: "", details: "" });
    const [selectedTaskIndex, setSelectedTaskIndex] = useState(null);
    const [isEditing, setIsEditing] = useState(false);

    // ✅ Fetch tasks from FastAPI on component mount
    useEffect(() => {
        axios.get(`${API_BASE_URL}/tasks`)
            .then(response => {
                setTasks(response.data);
            })
            .catch(error => console.error("Error fetching tasks:", error));
    }, []);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setNewTask(prevTask => ({ ...prevTask, [name]: value }));
    };

    const handleTaskClick = (index) => {
        setSelectedTaskIndex(index);
    };

    const addTask = () => {
        if (newTask.title.trim() === "") return;

        // ✅ Send task to backend
        axios.post(`${API_BASE_URL}/tasks`, newTask)
            .then(response => {
                setTasks([...tasks, response.data]);
                setNewTask({ title: "", details: "" });
                setShowForm(false);
            })
            .catch(error => console.error("Error adding task:", error));
    };

    const handleEditClick = () => {
        setIsEditing(true);
        setNewTask(tasks[selectedTaskIndex]);
        setShowForm(true); // ✅ Show the form when editing
    };

    const handleUpdateTask = () => {
        if (newTask.title.trim() === "") return;

        const taskId = tasks[selectedTaskIndex].id; // ✅ assume each task has an `id` from backend

        // ✅ Send updated task to backend
        axios.put(`${API_BASE_URL}/tasks/${taskId}`, newTask)
            .then(response => {
                const updatedTasks = tasks.map((task, index) =>
                    index === selectedTaskIndex ? response.data : task
                );
                setTasks(updatedTasks);
                setIsEditing(false);
                setSelectedTaskIndex(null);
                setNewTask({ title: "", details: "" });
                setShowForm(false);
            })
            .catch(error => console.error("Error updating task:", error));
    };

    const removeTask = (index) => {
        const taskId = tasks[index].id; // ✅ use task `id` to delete from backend

        // ✅ Delete from backend
        axios.delete(`${API_BASE_URL}/tasks/${taskId}`)
            .then(() => {
                setTasks(tasks.filter((_, i) => i !== index));
                setSelectedTaskIndex(null);
            })
            .catch(error => console.error("Error deleting task:", error));
    };

    return (
        <div className="app-container">
            <h1>To Do List</h1>

            <div className="todo-container">
                {!showForm && (
                    <button onClick={() => setShowForm(true)}>Add Task</button>
                )}

                {showForm && (
                    <div className="task-form">
                        <h2>{isEditing ? "Edit Task" : "Add New Task"}</h2>
                        <div className="form-group">
                            <label htmlFor="title">Task name:*</label>
                            <input
                                type="text"
                                id="title"
                                name="title"
                                placeholder="Enter task title"
                                value={newTask.title}
                                onChange={handleInputChange}
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label htmlFor="details">Task details:*</label>
                            <textarea
                                id="details"
                                name="details"
                                placeholder="Enter task details"
                                value={newTask.details}
                                onChange={handleInputChange}
                                required
                            />
                        </div>
                        <div className="form-actions">
                            <button onClick={isEditing ? handleUpdateTask : addTask}>
                                {isEditing ? "Update Task" : "Add Task"}
                            </button>
                            <button type="button" onClick={() => {
                                setShowForm(false);
                                setIsEditing(false);
                                setNewTask({ title: "", details: "" });
                            }}>
                                Cancel
                            </button>
                        </div>
                    </div>
                )}

                <h2>Tasks</h2>
                {tasks.length === 0 ? (
                    <p>No tasks yet!</p>
                ) : (
                    <ul>
                        {tasks.map((task, index) => (
                            <li
                                key={task.id} // ✅ use unique task ID from backend
                                onClick={() => handleTaskClick(index)}
                                className={selectedTaskIndex === index ? 'selected' : ''}
                            >
                                {task.title}
                            </li>
                        ))}
                    </ul>
                )}

                {selectedTaskIndex !== null && (
                    <div className="task-details">
                        <h3>Task Details</h3>
                        <h4>{tasks[selectedTaskIndex].title}</h4>
                        <p>{tasks[selectedTaskIndex].details}</p>
                        <div className="task-actions">
                            <button onClick={() => removeTask(selectedTaskIndex)}>Delete</button>
                            <button onClick={handleEditClick}>Edit</button>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}
