import React from "react";
import { useEffect, useState } from "react";
import { getTasks, createTask, deleteTask, toggleTask } from "./api";

export default function App() {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState("");

  const loadTasks = async () => {
    const data = await getTasks();
    setTasks(data);
  };

  useEffect(() => {
    loadTasks();
  }, []);

  const addTask = async () => {
    if (!title.trim()) return alert("Title is required");
    try {
      await createTask({ title: title.trim() });
      setTitle("");
      loadTasks();
    } catch (error) {
      alert("Failed to add task");
    }
  };

  const handleToggle = async (id) => {
    try {
      await toggleTask(id);
      loadTasks();
    } catch (error) {
      alert("Failed to toggle task");
    }
  };

  const handleDelete = async (id) => {
    try {
      await deleteTask(id);
      loadTasks();
    } catch (error) {
      alert("Failed to delete task");
    }
  };

  return (
    <div>
      <h2>Task Manager</h2>

      <div className="task-form">
        <input
          type="text"
          placeholder="Task title"
          value={title}
          onChange={e => setTitle(e.target.value)}
        />

        <button onClick={addTask}>Add Task</button>
      </div>

      <ul className="task-list">
        {tasks.map(task => (
          <li key={task.id} className={`task-item ${task.completed ? 'completed' : ''}`}>
            <span>{task.title}</span>
            <div>
              <button className="toggle" onClick={() => handleToggle(task.id)}>
                {task.completed ? "Mark Pending" : "Mark Done"}
              </button>
              <button className="delete" onClick={() => handleDelete(task.id)}>
                Delete
              </button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
