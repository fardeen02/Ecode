/* =========================================================
   ECODE // frontend controller
   One JS file for the initial public/authenticated experience.

   Backend contract used here:

     POST /api/auth/register
       {
         username,
         email,
         password,
         preferred_language
       }

     POST /api/auth/login
       {
         username,
         password
       }

   If your Flask API lives on another origin, change API_BASE.
   ========================================================= */

const ECODE = {
  API_BASE: "",

  endpoints: {
    register: "/api/auth/register",
    login: "/api/auth/login"
  },

  storage: {
    token: "ecode_access_token",
    user: "ecode_user"
  }
};


/* ---------- App startup ---------- */

document.addEventListener("DOMContentLoaded", () => {
  setupPasswordToggles();
  setupRegister();
  setupLogin();
  setupLogout();
  protectDashboard();
  hydrateIdentity();
});


/* ---------- API helper ---------- */

async function apiRequest(path, options = {}) {
  const response = await fetch(`${ECODE.API_BASE}${path}`, {
    ...options,

    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {})
    }
  });

  let data = null;

  try {
    data = await response.json();
  } catch {
    data = {};
  }

  if (!response.ok) {
    const message =
      data.error ||
      data.message ||
      `Request failed with status ${response.status}`;

    throw new Error(message);
  }

  return data;
}


/* =========================================================
   REGISTRATION
   ========================================================= */

function setupRegister() {
  const form = document.querySelector("#registerForm");

  if (!form) return;

  form.addEventListener("submit", async (event) => {
    /*
     * IMPORTANT:
     * Prevent the browser's normal form submission.
     *
     * Without this, the browser may put form data
     * directly into the URL.
     */
    event.preventDefault();

    const message =
      document.querySelector("#registerMessage");

    clearMessage(message);

    const formData = new FormData(form);

    const username =
      (formData.get("username") || "").trim();

    const email =
      (formData.get("email") || "").trim();

    const password =
      formData.get("password") || "";

    const preferredLanguage =
      formData.get("preferred_language") || "";

    const payload = {
      username: username,
      email: email,
      password: password,
      preferred_language: preferredLanguage
    };

    const validationError =
      validateRegistration(payload);

    if (validationError) {
      showMessage(
        message,
        validationError,
        "error"
      );

      return;
    }

    const submitButton =
      form.querySelector("button[type='submit']");

    setButtonLoading(
      submitButton,
      "CREATING..."
    );

    try {
      const data = await apiRequest(
        ECODE.endpoints.register,
        {
          method: "POST",
          body: JSON.stringify(payload)
        }
      );

      showMessage(
        message,
        data.message ||
          "Account created successfully. Redirecting...",
        "success"
      );

      /*
       * Registration does NOT automatically log
       * the user in.
       */
      setTimeout(() => {
        window.location.href = "/login";
      }, 900);

    } catch (error) {

      showMessage(
        message,
        error.message,
        "error"
      );

    } finally {

      setButtonLoading(
        submitButton,
        null
      );
    }
  });
}


function validateRegistration(data) {

  if (!data.username) {
    return "username is required.";
  }

  if (!data.email) {
    return "email is required.";
  }

  if (!data.password) {
    return "password is required.";
  }

  if (!data.preferred_language) {
    return "preferred language is required.";
  }

  if (data.username.length < 3) {
    return "username must contain at least 3 characters.";
  }

  if (data.password.length < 8) {
    return "password must contain at least 8 characters.";
  }

  if (!["python", "java"].includes(
    data.preferred_language
  )) {
    return "unsupported preferred language.";
  }

  return null;
}


/* =========================================================
   LOGIN
   ========================================================= */

function setupLogin() {

  const form =
    document.querySelector("#loginForm");

  if (!form) return;

  form.addEventListener("submit", async (event) => {

    /*
     * Prevent normal browser form submission.
     *
     * This keeps credentials out of the URL.
     */
    event.preventDefault();

    const message =
      document.querySelector("#loginMessage");

    clearMessage(message);

    const formData =
      new FormData(form);

    const username =
      (formData.get("username") || "").trim();

    const password =
      formData.get("password") || "";

    if (!username || !password) {

      showMessage(
        message,
        "username and password are required.",
        "error"
      );

      return;
    }

    const submitButton =
      form.querySelector("button[type='submit']");

    setButtonLoading(
      submitButton,
      "AUTHENTICATING..."
    );

    try {

      /*
       * Backend expects:
       *
       * {
       *   username,
       *   password
       * }
       */
      const data = await apiRequest(
        ECODE.endpoints.login,
        {
          method: "POST",

          body: JSON.stringify({
            username: username,
            password: password
          })
        }
      );

      /*
       * Flask-JWT-Extended returns access_token.
       */
      const token =
        data.access_token || data.token;

      if (!token) {

        throw new Error(
          "login succeeded but no access token was returned."
        );
      }

      /*
       * Store JWT.
       */
      localStorage.setItem(
        ECODE.storage.token,
        token
      );

      /*
       * Store user information.
       */
      const user =
        data.user || {
          username: username
        };

      localStorage.setItem(
        ECODE.storage.user,
        JSON.stringify(user)
      );

      showMessage(
        message,
        data.message ||
          "Access granted. Loading dashboard...",
        "success"
      );

      /*
       * Give the success message a moment
       * before opening the dashboard.
       */
      setTimeout(() => {
        window.location.href = "/dashboard";
      }, 650);

    } catch (error) {

      showMessage(
        message,
        error.message,
        "error"
      );

    } finally {

      setButtonLoading(
        submitButton,
        null
      );
    }
  });
}


/* =========================================================
   DASHBOARD PROTECTION
   ========================================================= */

function protectDashboard() {

  const isDashboard =
    document.body.classList.contains("app-page");

  if (!isDashboard) return;

  const token =
    localStorage.getItem(
      ECODE.storage.token
    );

  /*
   * No JWT = user isn't logged in.
   */
  if (!token) {

    window.location.replace("/login");

    return;
  }
}


/* =========================================================
   USER IDENTITY
   ========================================================= */

function hydrateIdentity() {

  const user =
    getStoredUser();

  if (!user) return;

  const username =
    user.username ||
    user.user_name ||
    user.email?.split("@")[0] ||
    "coder";

  const targets = [
    document.querySelector("#userIdentity"),
    document.querySelector("#sidebarUser"),
    document.querySelector("#welcomeUser")
  ];

  targets.forEach((element) => {

    if (element) {
      element.textContent = username;
    }

  });
}


/* =========================================================
   LOGOUT
   ========================================================= */

function setupLogout() {

  const button =
    document.querySelector("#logoutButton");

  if (!button) return;

  button.addEventListener("click", () => {

    localStorage.removeItem(
      ECODE.storage.token
    );

    localStorage.removeItem(
      ECODE.storage.user
    );

    window.location.replace("/");
  });
}


/* =========================================================
   STORED USER
   ========================================================= */

function getStoredUser() {

  try {

    return JSON.parse(
      localStorage.getItem(
        ECODE.storage.user
      ) || "null"
    );

  } catch {

    return null;
  }
}


/* =========================================================
   PASSWORD VISIBILITY
   ========================================================= */

function setupPasswordToggles() {

  document
    .querySelectorAll("[data-toggle-password]")
    .forEach((button) => {

      button.addEventListener("click", () => {

        const selector =
          button.dataset.togglePassword;

        const input =
          document.querySelector(selector);

        if (!input) return;

        /*
         * Determine current state.
         */
        const isVisible =
          input.type === "text";

        /*
         * Toggle password visibility.
         */
        input.type =
          isVisible
            ? "password"
            : "text";

        /*
         * Update button text.
         */
        button.textContent =
          isVisible
            ? "show"
            : "hide";

        /*
         * Accessibility.
         */
        button.setAttribute(
          "aria-label",
          isVisible
            ? "Show password"
            : "Hide password"
        );
      });

    });
}


/* =========================================================
   UI HELPERS
   ========================================================= */

function showMessage(
  element,
  text,
  type
) {

  if (!element) return;

  element.textContent =
    `> ${text}`;

  element.className =
    `form-message ${type}`;
}


function clearMessage(element) {

  if (!element) return;

  element.textContent = "";

  element.className =
    "form-message";
}


function setButtonLoading(
  button,
  text
) {

  if (!button) return;

  /*
   * Save original button text only once.
   */
  if (!button.dataset.originalText) {

    button.dataset.originalText =
      button.textContent;
  }

  if (text) {

    button.disabled = true;

    button.textContent =
      `[ ${text} ]`;

  } else {

    button.disabled = false;

    button.textContent =
      button.dataset.originalText;
  }
}