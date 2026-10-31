const rawApiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? "";
const API_BASE_URL = rawApiBaseUrl.trim().replace(/\/+$/, "");

function formatErrorDetail(detail) {
  if (typeof detail === "string" && detail.trim()) {
    return detail;
  }

  if (Array.isArray(detail)) {
    return detail
      .map((item) => {
        if (typeof item === "string") {
          return item;
        }

        const location = Array.isArray(item?.loc)
          ? item.loc.filter((part) => part !== "body").join(".")
          : "";

        const message =
          typeof item?.msg === "string" ? item.msg : "Input tidak valid.";

        return location ? `${location}: ${message}` : message;
      })
      .join("; ");
  }

  return null;
}

async function buildHttpError(response) {
  let payload = null;
  let rawBody = "";

  try {
    rawBody = await response.text();

    if (rawBody) {
      try {
        payload = JSON.parse(rawBody);
      } catch {
        payload = { unparsedBody: rawBody };
      }
    }
  } catch {
    // Jika body error tidak dapat dibaca, status HTTP tetap tersedia.
  }

  const detail = payload?.detail;
  const message =
    formatErrorDetail(detail) ??
    `Permintaan gagal dengan HTTP ${response.status}.`;

  const error = new Error(message);
  error.status = response.status;
  error.details = detail ?? payload;

  return error;
}

async function request(path, options = {}) {
  if (!API_BASE_URL) {
    throw new Error(
      "VITE_API_BASE_URL belum diatur. Periksa frontend/.env lalu restart Vite.",
    );
  }

  const headers = {
    Accept: "application/json",
  };

  if (options.body !== undefined) {
    headers["Content-Type"] = "application/json";
  }

  let response;

  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      ...options,
      headers,
    });
  } catch (cause) {
    throw new Error(
      "Backend tidak dapat dihubungi. Pastikan FastAPI berjalan dan alamat API benar.",
      { cause },
    );
  }

  if (!response.ok) {
    throw await buildHttpError(response);
  }

  if (response.status === 204) {
    return null;
  }

  try {
    return await response.json();
  } catch (cause) {
    throw new Error(
      `Backend mengirim response sukses tanpa JSON yang valid (HTTP ${response.status}).`,
      { cause },
    );
  }
}

export function getTasks() {
  return request("/tasks");
}

export function createTask(taskData) {
  return request("/tasks", {
    method: "POST",
    body: JSON.stringify(taskData),
  });
}

export function updateTask(id, taskData) {
  return request(`/tasks/${encodeURIComponent(id)}`, {
    method: "PUT",
    body: JSON.stringify(taskData),
  });
}

export function deleteTask(id) {
  return request(`/tasks/${encodeURIComponent(id)}`, {
    method: "DELETE",
  });
}
