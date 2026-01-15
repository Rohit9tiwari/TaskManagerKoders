const API = "http://127.0.0.1:5000";

export const getTasks = async () => {
  try {
    const res = await fetch(`${API}/tasks`);
    if (!res.ok) throw new Error('Failed to fetch tasks');
    return await res.json();
  } catch (error) {
    console.error(error);
    return [];
  }
};

export const createTask = async (task) => {
  try {
    const res = await fetch(`${API}/tasks`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(task),
    });
    if (!res.ok) throw new Error('Failed to create task');
    return await res.json();
  } catch (error) {
    console.error(error);
    throw error;
  }
};

export const deleteTask = async (id) => {
  try {
    const res = await fetch(`${API}/tasks/${id}`, { method: "DELETE" });
    if (!res.ok) throw new Error('Failed to delete task');
    return await res.json();
  } catch (error) {
    console.error(error);
    throw error;
  }
};

export const toggleTask = async (id) => {
  try {
    const res = await fetch(`${API}/tasks/${id}/toggle`, { method: "PATCH" });
    if (!res.ok) throw new Error('Failed to toggle task');
    return await res.json();
  } catch (error) {
    console.error(error);
    throw error;
  }
};
