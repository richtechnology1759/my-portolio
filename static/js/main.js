// --------------------
// DARK MODE TOGGLE
// --------------------
const toggleBtn = document.getElementById("theme-toggle");

if (toggleBtn) {
    toggleBtn.addEventListener("click", () => {
        document.body.classList.toggle("dark");
    });
}

// --------------------
// CONTACT FORM
// --------------------
const form = document.getElementById("contact-form");
const status = document.getElementById("form-status");

if (form) {
    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        status.textContent = "";
        status.className = "";

        const name = document.getElementById("name").value.trim();
        const email = document.getElementById("email").value.trim();
        const message = document.getElementById("message").value.trim();

        if (!name || !email || !message) {
            status.textContent = "Please fill in all fields.";
            status.classList.add("error");
            return;
        }

        try {
            const response = await fetch("/contact", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ name, email, message })
            });

            const result = await response.json();

            if (result.success) {
                status.textContent = "Message sent successfully.";
                status.classList.add("success");
                form.reset();
            } else {
                status.textContent = "Something went wrong.";
                status.classList.add("error");
            }
        } catch (error) {
            status.textContent = "Server error. Try again later.";
            status.classList.add("error");
        }
    });
}
