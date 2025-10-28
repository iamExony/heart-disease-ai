let userType = "patient";

// Handle user type tabs
const tabs = document.querySelectorAll(".tab");
tabs.forEach(tab => {
  tab.addEventListener("click", () => {
    tabs.forEach(t => t.classList.remove("active"));
    tab.classList.add("active");
    userType = tab.dataset.role;
  });
});

// Handle login
const loginForm = document.getElementById("loginForm");
loginForm.addEventListener("submit", (e) => {
  e.preventDefault();

  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();

  if (!email || !password) {
    alert("⚠️ Please fill in all fields.");
    return;
  }

  // Mock login
  alert("✅ Login successful!");

  // Simulate navigation
  switch (userType) {
    case "patient":
      window.location.href = "dashboard-patient.html";
      break;
    case "clinician":
      window.location.href = "dashboard-clinician.html";
      break;
    case "admin":
      window.location.href = "dashboard-admin.html";
      break;
  }
});

// Sign up button
document.getElementById("signupBtn").addEventListener("click", () => {
  alert("Redirecting to Sign Up page...");
  window.location.href = "signup.html";
});
