// MetaGuard — client-side metaverse room
(function () {
  const cfg = window.METAGUARD_CONFIG;
  const canvas = document.getElementById("room-canvas");
  const ctx = canvas.getContext("2d");
  const chatBox = document.getElementById("chat-messages");
  const chatInput = document.getElementById("chat-input");
  const chatSend = document.getElementById("chat-send");
  const chatStatus = document.getElementById("chat-status");
  const toastContainer = document.getElementById("toast-container");

  let me = null;
  let users = [];
  let messages = [];
  const seenMessageIds = new Set();

  const STEP = 8;
  const keys = {};

  // ----------- Rendering -----------
  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // grid
    ctx.strokeStyle = "rgba(76, 201, 240, 0.06)";
    ctx.lineWidth = 1;
    for (let x = 0; x < canvas.width; x += 40) {
      ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, canvas.height); ctx.stroke();
    }
    for (let y = 0; y < canvas.height; y += 40) {
      ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(canvas.width, y); ctx.stroke();
    }

    // central plaza
    ctx.fillStyle = "rgba(76, 201, 240, 0.04)";
    ctx.beginPath();
    ctx.arc(canvas.width / 2, canvas.height / 2, 90, 0, Math.PI * 2);
    ctx.fill();

    // avatars
    users.forEach((u) => {
      const isMe = me && u.id === me;
      // glow for me
      if (isMe) {
        ctx.shadowColor = u.color;
        ctx.shadowBlur = 18;
      }
      ctx.fillStyle = u.color;
      ctx.beginPath();
      ctx.arc(u.x, u.y, cfg.avatarRadius, 0, Math.PI * 2);
      ctx.fill();
      ctx.shadowBlur = 0;

      // ring
      ctx.strokeStyle = isMe ? "#ffffff" : "rgba(255,255,255,0.4)";
      ctx.lineWidth = isMe ? 2 : 1;
      ctx.stroke();

      // username
      ctx.fillStyle = "#e2e8f0";
      ctx.font = "12px Segoe UI, Arial";
      ctx.textAlign = "center";
      ctx.fillText(u.username + (isMe ? " (you)" : ""), u.x, u.y - cfg.avatarRadius - 6);
    });
  }

  // ----------- Movement -----------
  document.addEventListener("keydown", (e) => {
    if (document.activeElement === chatInput) return;
    keys[e.key.toLowerCase()] = true;
  });
  document.addEventListener("keyup", (e) => {
    keys[e.key.toLowerCase()] = false;
  });

  let pendingMove = false;
  async function tickMovement() {
    if (!me) return;
    const meUser = users.find((u) => u.id === me);
    if (!meUser) return;

    let dx = 0, dy = 0;
    if (keys["arrowleft"] || keys["a"]) dx -= STEP;
    if (keys["arrowright"] || keys["d"]) dx += STEP;
    if (keys["arrowup"] || keys["w"]) dy -= STEP;
    if (keys["arrowdown"] || keys["s"]) dy += STEP;

    if (dx === 0 && dy === 0) return;

    const newX = Math.max(cfg.avatarRadius, Math.min(cfg.roomWidth - cfg.avatarRadius, meUser.x + dx));
    const newY = Math.max(cfg.avatarRadius, Math.min(cfg.roomHeight - cfg.avatarRadius, meUser.y + dy));
    meUser.x = newX;
    meUser.y = newY;

    if (pendingMove) return;
    pendingMove = true;
    try {
      await fetch("/api/move", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ x: newX, y: newY }),
      });
    } finally {
      pendingMove = false;
    }
  }

  // ----------- Polling -----------
  async function pollPositions() {
    try {
      const r = await fetch("/api/positions");
      if (!r.ok) throw new Error("positions http " + r.status);
      const data = await r.json();
      me = data.me;
      // Preserve our own predicted position to avoid jitter
      const prevMe = users.find((u) => u.id === me);
      users = data.users.map((u) => {
        if (prevMe && u.id === me) return { ...u, x: prevMe.x, y: prevMe.y };
        return u;
      });
      chatStatus.textContent = "connected";
      chatStatus.classList.remove("text-danger");
    } catch (e) {
      chatStatus.textContent = "reconnecting...";
      chatStatus.classList.add("text-danger");
    }
  }

  async function pollMessages() {
    try {
      const r = await fetch("/api/messages");
      if (!r.ok) return;
      const data = await r.json();
      const newMsgs = data.messages.filter((m) => !seenMessageIds.has(m.id));
      newMsgs.forEach((m) => {
        seenMessageIds.add(m.id);
        appendMessage(m);
      });
    } catch (e) {
      // ignored
    }
  }

  // ----------- Chat -----------
  function appendMessage(m) {
    const row = document.createElement("div");
    row.className = "chat-msg";
    const dot = `<span class="dot" style="background:${m.color}"></span>`;
    row.innerHTML = `${dot}<span class="name" style="color:${m.color}">${escapeHtml(m.username)}:</span> ${escapeHtml(m.content)}`;
    chatBox.appendChild(row);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  async function sendMessage() {
    const text = chatInput.value.trim();
    if (!text) return;
    chatInput.disabled = true;
    chatSend.disabled = true;
    try {
      const r = await fetch("/api/chat/send", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ content: text }),
      });
      const data = await r.json();
      if (data.blocked) {
        showToast(data);
      } else {
        chatInput.value = "";
        // Don't append optimistically — next poll will pick it up.
      }
    } catch (e) {
      showToast({ blocked: true, reason: "network error" });
    } finally {
      chatInput.disabled = false;
      chatSend.disabled = false;
      chatInput.focus();
    }
  }

  function showToast(data) {
    const el = document.createElement("div");
    el.className = "threat-toast";
    let label = "blocked";
    if (data.toxic && data.phishing) label = "toxic + phishing";
    else if (data.toxic) label = "toxic content";
    else if (data.phishing) label = "phishing url";
    el.innerHTML = `
      <div class="label">⚠ ${escapeHtml(label)}</div>
      <div class="mt-1">Your message was flagged by the AI and was not sent.</div>
      <div class="text-secondary small mt-1">${escapeHtml(data.reason || "")}</div>
    `;
    toastContainer.appendChild(el);
    setTimeout(() => el.remove(), 6000);
  }

  chatSend.addEventListener("click", sendMessage);
  chatInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") sendMessage();
  });

  // ----------- Loops -----------
  pollPositions();
  pollMessages();
  setInterval(pollPositions, 500);
  setInterval(pollMessages, 1000);
  setInterval(tickMovement, 60);

  function renderLoop() {
    draw();
    requestAnimationFrame(renderLoop);
  }
  renderLoop();

  canvas.focus();
})();
