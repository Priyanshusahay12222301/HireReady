(function () {
  function getUser() {
    try {
      const raw = localStorage.getItem("hireready_user");
      if (!raw) {
        return null;
      }
      return JSON.parse(raw);
    } catch (error) {
      return null;
    }
  }

  function setText(id, value) {
    const el = document.getElementById(id);
    if (!el) {
      return;
    }
    el.textContent = value;
  }

  function setInputValue(id, value) {
    const el = document.getElementById(id);
    if (!el) {
      return;
    }
    el.value = value;
  }

  function setSelectValue(id, value) {
    const el = document.getElementById(id);
    if (!el || !value) {
      return;
    }

    const options = Array.from(el.options || []);
    const match = options.find((opt) => opt.value === value || opt.text === value);
    if (match) {
      el.value = match.value;
    }
  }

  function normalizeGender(value) {
    const raw = String(value || "").trim().toLowerCase();
    if (raw === "male" || raw === "female" || raw === "other") {
      return raw;
    }
    return "other";
  }

  function getAvatarUrl(user) {
    const name = encodeURIComponent((user && user.name) || "Student");
    const gender = normalizeGender(user && user.gender);
    if (gender === "female") {
      return `https://api.dicebear.com/9.x/notionists/svg?seed=${name}&backgroundColor=fde68a,93c5fd,c4b5fd`;
    }
    if (gender === "male") {
      return `https://api.dicebear.com/9.x/adventurer/svg?seed=${name}&backgroundColor=93c5fd,a7f3d0,fde68a`;
    }
    return `https://api.dicebear.com/9.x/pixel-art/svg?seed=${name}&backgroundColor=c7d2fe,bae6fd,a7f3d0`;
  }

  function setProfileAvatars(user) {
    const url = getAvatarUrl(user);
    const nav = document.getElementById("profile-avatar-nav");
    const main = document.getElementById("profile-avatar-main");

    if (nav) {
      nav.src = url;
    }

    if (main) {
      main.src = url;
    }
  }

  function renderSkills(containerId, skills) {
    const container = document.getElementById(containerId);
    if (!container) {
      return;
    }

    container.innerHTML = "";

    const skillItems = (skills || "")
      .split(",")
      .map((item) => item.trim())
      .filter(Boolean);

    if (skillItems.length === 0) {
      const chip = document.createElement("span");
      chip.className = "px-4 py-2 bg-surface-container-high text-on-surface-variant rounded-full font-medium italic";
      chip.textContent = "No skills extracted yet";
      container.appendChild(chip);
      return;
    }

    skillItems.forEach((skill) => {
      const chip = document.createElement("span");
      chip.className = "px-4 py-2 bg-primary text-white rounded-full font-medium";
      chip.textContent = skill;
      container.appendChild(chip);
    });
  }

  function setResumeFeedback(message, isError) {
    const el = document.getElementById("resume-feedback");
    if (!el) {
      return;
    }
    el.textContent = message || "";
    el.style.color = isError ? "#fecaca" : "#bbf7d0";
  }

  function setProfileSaveFeedback(message, isError) {
    const el = document.getElementById("profile-save-feedback");
    if (!el) {
      return;
    }
    el.textContent = message || "";
    el.style.color = isError ? "#dc2626" : "#0f766e";
  }


  function animateNumber(el, target, suffix = "") {
    if (!el) {
      return;
    }
    const duration = 900;
    const start = performance.now();

    function frame(now) {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      const value = Math.round(target * eased);
      el.textContent = `${value}${suffix}`;
      if (progress < 1) {
        requestAnimationFrame(frame);
      }
    }

    requestAnimationFrame(frame);
  }

  function setBar(id, value) {
    const bar = document.getElementById(id);
    if (!bar) {
      return;
    }
    requestAnimationFrame(() => {
      bar.style.width = `${Math.max(0, Math.min(100, value))}%`;
    });
  }

  function getAccountScore(userId) {
    if (!userId) {
      return Math.floor(Math.random() * 26) + 75;
    }

    const key = `hireready_dynamic_score_${userId}`;
    const cached = Number(localStorage.getItem(key));
    if (Number.isFinite(cached) && cached >= 75 && cached <= 100) {
      return cached;
    }

    const generated = Math.floor(Math.random() * 26) + 75;
    localStorage.setItem(key, String(generated));
    return generated;
  }

  function applyReadinessScore(score) {
    const clamped = Math.max(75, Math.min(100, Math.round(score)));
    const scoreEl = document.getElementById("readiness-score-value");
    const ring = document.getElementById("readiness-ring");
    const circumference = 502.6;

    animateNumber(scoreEl, clamped, "%");

    if (ring) {
      const offset = circumference * (1 - clamped / 100);
      requestAnimationFrame(() => {
        ring.style.strokeDashoffset = `${offset}`;
      });
    }
  }

  async function hydrateDashboard(user) {
    const testsTakenEl = document.getElementById("stat-tests-taken");
    const avgScoreEl = document.getElementById("stat-avg-score");
    const jobsAppliedEl = document.getElementById("stat-jobs-applied");
    const successRateEl = document.getElementById("stat-success-rate");
    const profileTextEl = document.getElementById("metric-profile-text");
    const testsTextEl = document.getElementById("metric-tests-text");
    const interviewsTextEl = document.getElementById("metric-interviews-text");

    const fallbackScore = getAccountScore(user.id);
    applyReadinessScore(fallbackScore);
    setBar("metric-profile-bar", 90);
    setBar("metric-tests-bar", 68);
    setBar("metric-interviews-bar", 72);

    try {
      if (!window.HireReadyAPI || !window.HireReadyAPI.getDashboard || !user.id) {
        return;
      }

      const payload = await window.HireReadyAPI.getDashboard(user.id);
      const stats = payload.stats || {};

      const dynamicScore = getAccountScore(user.id);
      applyReadinessScore(dynamicScore);

      const profileCompletion = Math.round(Number(stats.profile_completion || 90));
      const testPerformance = Math.round(Number(stats.avg_mock_test_score || 68));
      const mockInterviews = Math.max(75, dynamicScore - Math.floor(Math.random() * 8));

      if (profileTextEl) {
        profileTextEl.textContent = `${profileCompletion}%`;
      }
      if (testsTextEl) {
        testsTextEl.textContent = `${testPerformance}%`;
      }
      if (interviewsTextEl) {
        interviewsTextEl.textContent = `${mockInterviews}%`;
      }

      setBar("metric-profile-bar", profileCompletion);
      setBar("metric-tests-bar", testPerformance);
      setBar("metric-interviews-bar", mockInterviews);

      animateNumber(testsTakenEl, Number(stats.tests_taken || 0));
      animateNumber(avgScoreEl, testPerformance, "%");
      animateNumber(jobsAppliedEl, Number(stats.jobs_applied || 0));
      animateNumber(successRateEl, Math.max(10, Math.round((testPerformance + dynamicScore) / 2 - 40)), "%");
    } catch (error) {
      // Keep dashboard usable with fallback visuals if API call fails.
    }
  }

  function setupResumeUpload(user) {
    const button = document.getElementById("update-resume-btn");
    const input = document.getElementById("resume-file-input");
    if (!button || !input) {
      return;
    }

    button.addEventListener("click", () => {
      input.click();
    });

    input.addEventListener("change", async () => {
      const file = input.files && input.files[0];
      if (!file) {
        return;
      }

      const lower = file.name.toLowerCase();
      const allowed = lower.endsWith(".pdf") || lower.endsWith(".doc") || lower.endsWith(".docx");
      if (!allowed) {
        setResumeFeedback("Only PDF, DOC, and DOCX files are allowed.", true);
        input.value = "";
        return;
      }

      const maxSizeBytes = 5 * 1024 * 1024;
      if (file.size > maxSizeBytes) {
        setResumeFeedback("File size must be 5MB or less.", true);
        input.value = "";
        return;
      }

      if (!window.HireReadyAPI || !window.HireReadyAPI.uploadResume || !user.id) {
        setResumeFeedback("Resume upload is unavailable right now.", true);
        return;
      }

      const form = new FormData();
      form.append("cv_file", file);

      button.disabled = true;
      const originalText = button.textContent;
      button.textContent = "Uploading...";
      setResumeFeedback("", false);

      try {
        const result = await window.HireReadyAPI.uploadResume(user.id, form);
        if (result && result.user) {
          localStorage.setItem("hireready_user", JSON.stringify(result.user));
          renderSkills("profile-skills-list", result.user.skills);
          if (typeof result.user.cgpa === "number") {
            setText("profile-cgpa", result.user.cgpa.toFixed(2));
          }
        }
        setResumeFeedback("Resume updated successfully.", false);
      } catch (error) {
        setResumeFeedback(error.message || "Failed to update resume.", true);
      } finally {
        button.disabled = false;
        button.textContent = originalText;
        input.value = "";
      }
    });
  }


  function setupNewApplicationFlow(user) {
    const openBtn = document.getElementById("new-application-btn");
    const modal = document.getElementById("new-application-modal");
    const closeBtn = document.getElementById("close-application-modal-btn");
    const cancelBtn = document.getElementById("cancel-new-application-btn");
    const form = document.getElementById("new-application-form");
    const select = document.getElementById("new-application-job");
    const feedback = document.getElementById("new-application-feedback");
    const submitBtn = document.getElementById("submit-new-application-btn");

    if (!openBtn || !modal || !form || !select || !submitBtn || !feedback) {
      return;
    }

    function setFeedback(message, isError) {
      feedback.textContent = message || "";
      feedback.style.color = isError ? "#dc2626" : "#475569";
    }

    function openModal() {
      modal.classList.remove("hidden");
      modal.classList.add("flex");
      setFeedback("", false);
    }

    function closeModal() {
      modal.classList.add("hidden");
      modal.classList.remove("flex");
      setFeedback("", false);
    }

    async function loadAvailableJobs() {
      if (!window.HireReadyAPI || !window.HireReadyAPI.listJobs || !window.HireReadyAPI.listApplications) {
        select.innerHTML = '<option value="">Application service unavailable</option>';
        setFeedback("Application service is unavailable.", true);
        return;
      }

      try {
        const [jobs, applications] = await Promise.all([
          window.HireReadyAPI.listJobs(),
          window.HireReadyAPI.listApplications(user.id),
        ]);

        const appliedJobIds = new Set((applications || []).map((item) => item.job_id));
        const available = (jobs || []).filter((job) => !appliedJobIds.has(job.id));

        if (!available.length) {
          select.innerHTML = '<option value="">No new jobs available</option>';
          setFeedback("You have already applied to all available jobs.", false);
          return;
        }

        select.innerHTML = '<option value="">Choose a job...</option>' +
          available
            .map((job) => `<option value="${job.id}">${job.company} - ${job.role} (${job.job_type})</option>`)
            .join("");
      } catch (error) {
        select.innerHTML = '<option value="">Failed to load jobs</option>';
        setFeedback(error.message || "Failed to load jobs.", true);
      }
    }

    openBtn.addEventListener("click", async () => {
      if (!user || !user.id) {
        setFeedback("Please login first.", true);
        return;
      }
      openModal();
      await loadAvailableJobs();
    });

    if (closeBtn) {
      closeBtn.addEventListener("click", closeModal);
    }

    if (cancelBtn) {
      cancelBtn.addEventListener("click", closeModal);
    }

    modal.addEventListener("click", (event) => {
      if (event.target === modal) {
        closeModal();
      }
    });

    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const jobId = Number(select.value);
      if (!jobId) {
        setFeedback("Please select a job.", true);
        return;
      }

      submitBtn.disabled = true;
      const oldText = submitBtn.textContent;
      submitBtn.textContent = "Submitting...";

      try {
        await window.HireReadyAPI.applyToJob({ user_id: user.id, job_id: jobId });
        setFeedback("Application submitted successfully. Redirecting...", false);
        setTimeout(() => {
          window.location.href = "my-applications.html";
        }, 650);
      } catch (error) {
        setFeedback(error.message || "Failed to submit application.", true);
      } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = oldText;
      }
    });
  }

  function setupProfileSaveChanges(user) {
    const saveBtn = document.getElementById("profile-save-btn");
    const cancelBtn = document.getElementById("profile-cancel-btn");
    const nameEl = document.getElementById("profile-full-name");
    const phoneEl = document.getElementById("profile-phone");
    const genderEl = document.getElementById("profile-gender");
    const branchEl = document.getElementById("profile-branch");
    const yearEl = document.getElementById("profile-year");

    if (!saveBtn || !nameEl || !phoneEl || !genderEl || !branchEl || !yearEl) {
      return;
    }

    function applyUserToInputs(currentUser) {
      setInputValue("profile-full-name", currentUser.name || "");
      setInputValue("profile-phone", currentUser.phone || "");
      setSelectValue("profile-gender", normalizeGender(currentUser.gender));
      setSelectValue("profile-branch", currentUser.branch || "");
      setSelectValue("profile-year", currentUser.current_year || "");
    }

    async function saveProfile() {
      const payload = {
        name: nameEl.value.trim(),
        phone: phoneEl.value.trim(),
        gender: normalizeGender(genderEl.value),
        branch: branchEl.value,
        current_year: yearEl.value,
      };

      if (!payload.name) {
        setProfileSaveFeedback("Full Name is required.", true);
        return;
      }

      if (!window.HireReadyAPI || !window.HireReadyAPI.updateUserProfile || !user.id) {
        setProfileSaveFeedback("Profile update service is unavailable.", true);
        return;
      }

      saveBtn.disabled = true;
      const oldText = saveBtn.textContent;
      saveBtn.textContent = "Saving...";
      setProfileSaveFeedback("", false);

      try {
        const result = await window.HireReadyAPI.updateUserProfile(user.id, payload);
        if (result && result.user) {
          user = result.user;
          localStorage.setItem("hireready_user", JSON.stringify(result.user));
          setText("profile-display-name", result.user.name || "");
          setText("dash-welcome-name", result.user.name || "");
          setProfileAvatars(result.user);
        }
        setProfileSaveFeedback("Profile updated successfully.", false);
      } catch (error) {
        setProfileSaveFeedback(error.message || "Failed to save profile changes.", true);
      } finally {
        saveBtn.disabled = false;
        saveBtn.textContent = oldText;
      }
    }

    saveBtn.addEventListener("click", saveProfile);

    if (cancelBtn) {
      cancelBtn.addEventListener("click", () => {
        applyUserToInputs(user);
        setProfileSaveFeedback("Changes reverted.", false);
      });
    }
  }

  const user = getUser();
  if (!user) {
    return;
  }

  if (user.name) {
    setText("dash-welcome-name", user.name);
    setText("profile-display-name", user.name);
    setInputValue("profile-full-name", user.name);
  }

  if (user.roll_no && user.email) {
    setText("dash-subtitle", "RN: " + user.roll_no + " • " + user.email);
  }

  if (user.roll_no) {
    setText("profile-display-roll", "RN: " + user.roll_no);
  }

  if (user.email) {
    setText("profile-display-email", user.email);
    setInputValue("profile-email", user.email);
  }

  if (user.phone) {
    setInputValue("profile-phone", user.phone);
  }

  if (user.gender) {
    setSelectValue("profile-gender", normalizeGender(user.gender));
  }

  if (user.branch) {
    setSelectValue("profile-branch", user.branch);
  }

  if (user.current_year) {
    setSelectValue("profile-year", user.current_year);
  }

  if (typeof user.cgpa === "number") {
    setText("profile-cgpa", user.cgpa.toFixed(2));
  } else {
    setText("profile-cgpa", "--");
  }

  renderSkills("profile-skills-list", user.skills);
  setProfileAvatars(user);
  hydrateDashboard(user);
  setupResumeUpload(user);
  setupProfileSaveChanges(user);
  setupNewApplicationFlow(user);
})();
