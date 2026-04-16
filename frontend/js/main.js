function setText(id, message, isError = false) {
  const el = document.getElementById(id);
  if (!el) {
    return;
  }
  el.textContent = message;
  el.style.color = isError ? "#ef4444" : "#10b981";
}

const registerForm = document.getElementById("register-form");
if (registerForm) {
  registerForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const password = document.getElementById("password").value;
    const confirmPasswordEl = document.getElementById("confirm_password");
    const confirmPassword = confirmPasswordEl ? confirmPasswordEl.value : password;
    const termsEl = document.getElementById("terms");
    const cvInput = document.getElementById("cv_file");
    const cgpaEl = document.getElementById("cgpa");
    const branchEl = document.getElementById("branch");
    const yearEl = document.getElementById("current_year");

    if (confirmPassword !== password) {
      setText("register-message", "Password and confirm password must match.", true);
      return;
    }

    if (termsEl && !termsEl.checked) {
      setText("register-message", "Please accept terms before registering.", true);
      return;
    }

    if (!cvInput || !cvInput.files || cvInput.files.length === 0) {
      setText("register-message", "Please upload your CV before registering.", true);
      return;
    }

    const rawCgpa = (cgpaEl && cgpaEl.value ? cgpaEl.value.trim() : "");
    if (rawCgpa) {
      const cgpaNumber = Number(rawCgpa);
      if (!Number.isFinite(cgpaNumber) || cgpaNumber < 0 || cgpaNumber > 10) {
        setText("register-message", "CGPA must be between 0 and 10.", true);
        return;
      }
    }

    const payload = new FormData();
    payload.append("name", document.getElementById("name").value);
    payload.append("roll_no", document.getElementById("roll_no").value);
    payload.append("email", document.getElementById("email").value);
    payload.append("password", password);
    payload.append("gender", document.getElementById("gender").value);
    payload.append("branch", branchEl ? branchEl.value : "");
    payload.append("current_year", yearEl ? yearEl.value : "");
    payload.append("cgpa", rawCgpa);
    payload.append("cv_file", cvInput.files[0]);

    try {
      const result = await window.HireReadyAPI.register(payload);
      localStorage.setItem("hireready_user", JSON.stringify(result.user));
      setText("register-message", "Registration successful. Redirecting to dashboard...");
      setTimeout(() => {
        window.location.href = "student/dashboard.html";
      }, 800);
    } catch (error) {
      setText("register-message", error.message, true);
    }
  });
}

const loginForm = document.getElementById("login-form");
if (loginForm) {
  loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const payload = {
      identifier: document.getElementById("identifier").value,
      password: document.getElementById("login-password").value,
    };

    try {
      const result = await window.HireReadyAPI.login(payload);
      localStorage.setItem("hireready_user", JSON.stringify(result.user));
      setText("login-message", "Login successful. Redirecting to dashboard...");
      setTimeout(() => {
        window.location.href = "student/dashboard.html";
      }, 800);
    } catch (error) {
      setText("login-message", error.message, true);
    }
  });
}
