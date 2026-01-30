const API_BASE = "http://127.0.0.1:8000";

const loginForm = document.getElementById("loginForm");
const msg = document.getElementById("msg");

loginForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  msg.textContent = "Logging in...";
  msg.className = "msg";

  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();

  try {
    // IMPORTANT: backend login uses Form data (OAuth2PasswordRequestForm)
    const formData = new URLSearchParams();
    formData.append("username", email);
    formData.append("password", password);

    const res = await fetch(`${API_BASE}/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: formData.toString(),
    });

    const data = await res.json();

    if (!res.ok) {
      msg.textContent = data.detail || "Login failed";
      msg.className = "msg error";
      return;
    }

    // Save token and role
    localStorage.setItem("token", data.access_token);
    localStorage.setItem("role", data.role);
    localStorage.setItem("email", email);

    msg.textContent = "Login successful ✅ Redirecting...";
    msg.className = "msg success";

    // Redirect based on role
    // Force employee to change password if required
    if (data.role === "employee" && data.must_change_password === true) {
      msg.textContent = "First login detected ✅ Please change password...";
      msg.className = "msg success";

      setTimeout(() => {
        window.location.href = "change_password.html";
      }, 800);

      return;
    }

    //  Normal redirect
    setTimeout(() => {
      if (data.role === "admin") {
        window.location.href = "admin_dashboard.html";
      } else {
        window.location.href = "employee_dashboard.html";
      }
    }, 800);


  } catch (err) {
    msg.textContent = "Server error. Check backend running.";
    msg.className = "msg error";
  }
});
