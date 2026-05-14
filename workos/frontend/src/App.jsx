import { useEffect, useState } from "react";

const API_URL = "http://localhost:8000";

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const login = () => {
    window.location.href = `${API_URL}/auth/login`;
  };

  const logout = () => {
    window.location.href = `${API_URL}/auth/logout`;
  };

  useEffect(() => {
    const controller = new AbortController();

    fetch(`${API_URL}/api/me`, {
      credentials: "include",
      signal: controller.signal,
    })
      .then(async (res) => {
        if (!res.ok) {
          setUser(null);
          return;
        }

        const data = await res.json();
        setUser(data);
      })
      .catch((err) => {
        if (err.name !== "AbortError") {
          setUser(null);
        }
      })
      .finally(() => {
        setLoading(false);
      });

    return () => {
      controller.abort();
    };
  }, []);

  if (loading) {
    return (
      <div style={{ padding: "40px", fontFamily: "Arial" }}>
        <h2>Loading...</h2>
      </div>
    );
  }

  return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>
      <h1>WorkOS Auth with React + FastAPI</h1>

      {!user ? (
        <button onClick={login}>Login with WorkOS</button>
      ) : (
        <>
          <h2>Welcome {user.email}</h2>
          <p>User is authenticated</p>
          <button onClick={logout}>Logout</button>
        </>
      )}
    </div>
  );
}

export default App;