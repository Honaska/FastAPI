import { getTasks, createTask, updateTask, deleteTask } from './api';
import { useEffect, useState } from 'react';

const [tasks, setTasks] = useState([]);

// Load tasks from backend
useEffect(() => {
  fetchTasks();
}, []);

const fetchTasks = () => {
  getTasks().then((res) => {
    setTasks(res.data);
  }).catch((err) => console.error(err));
};

const addTask = () => {
  if (newTask.title.trim() === "") return;
  createTask(newTask).then(() => {
    setNewTask({ title: "", details: "" });
    setShowForm(false);
    fetchTasks();
  });
};

const handleUpdateTask = () => {
  if (newTask.title.trim() === "") return;
  const taskId = tasks[selectedTaskIndex].id;
  updateTask(taskId, newTask).then(() => {
    setNewTask({ title: "", details: "" });
    setIsEditing(false);
    setSelectedTaskIndex(null);
    fetchTasks();
  });
};

const removeTask = (index) => {
  const taskId = tasks[index].id;
  deleteTask(taskId).then(() => {
    setSelectedTaskIndex(null);
    fetchTasks();
  });
};
