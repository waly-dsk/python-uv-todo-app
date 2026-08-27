function escapeHtml(str) {
  if (!str) return "";
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function statusBadge(isDone) {
  return isDone
    ? '<span class="badge bg-success">Done</span>'
    : '<span class="badge bg-warning text-dark">To do</span>';
}

function showToast(message, type = "success") {
  const toastEl = document.getElementById("appToast");
  const toastBody = document.getElementById("toastBody");
  const toastTitle = document.getElementById("toastTitle");

  toastEl.classList.remove(
    "text-bg-success",
    "text-bg-danger",
    "text-bg-warning",
  );
  const bgClass =
    type === "error"
      ? "text-bg-danger"
      : type === "warning"
        ? "text-bg-warning"
        : "text-bg-success";
  toastEl.classList.add(bgClass);

  toastTitle.textContent =
    type === "error" ? "Error" : type === "warning" ? "Warning" : "Success";
  toastBody.textContent = message;

  const toast = bootstrap.Toast.getOrCreateInstance(toastEl, { delay: 3000 });
  toast.show();
}

function showConfirmModal(message, onConfirm) {
  const modalEl = document.getElementById("confirmModal");
  const modalBody = document.getElementById("confirmModalBody");
  const okBtn = document.getElementById("confirmModalOkBtn");

  modalBody.textContent = message;

  const modal = bootstrap.Modal.getOrCreateInstance(modalEl);

  // Remplace le bouton pour éviter d'empiler les listeners à chaque appel
  const newOkBtn = okBtn.cloneNode(true);
  okBtn.replaceWith(newOkBtn);
  newOkBtn.addEventListener("click", function () {
    modal.hide();
    onConfirm();
  });

  modal.show();
}

function loadTodos() {
  $.getJSON("/get_todos", function (response) {
    const todosDiv = $("#todos");
    todosDiv.empty();

    if (response.todos.length === 0) {
      todosDiv.append(
        '<p class="text-center text-muted">No todos yet. Click "Add a todo" to get started.</p>',
      );
      return;
    }

    response.todos.forEach(function (todo) {
      const id = todo[0];
      const title = todo[1];
      const content = todo[2];
      const isDone = !!todo[3];

      const preview =
        content && content.length > 90
          ? content.substring(0, 90) + "…"
          : content;

      const todoHtml = `
      <div class="col-md-6 col-lg-4">
        <div class="card h-100 todo-item ${isDone ? "completed border-success opacity-75" : ""}" id="todo-${id}">
          <div class="card-body d-flex flex-column">
            <div class="form-check mb-2">
              <input class="form-check-input todo-checkbox" type="checkbox" id="done-${id}" data-id="${id}" ${isDone ? "checked" : ""}>
              <label class="form-check-label ${isDone ? "text-decoration-line-through text-muted" : ""}" for="done-${id}">
                <strong>${escapeHtml(title)}</strong>
              </label>
            </div>
            <p class="card-text text-muted flex-grow-1">${escapeHtml(preview)}</p>
            <div class="mb-2">${statusBadge(isDone)}</div>
            <div class="btn-group">
              <button type="button" data-id="${id}" class="btn btn-sm btn-outline-primary show"><i class="bi bi-eye"></i> Show</button>
              <button type="button" data-id="${id}" class="btn btn-sm btn-outline-secondary edit"><i class="bi bi-pencil"></i> Edit</button>
              <button type="button" data-id="${id}" class="btn btn-sm btn-outline-danger delete"><i class="bi bi-trash"></i> Delete</button>
            </div>
          </div>
        </div>
      </div>
    `;

      todosDiv.append(todoHtml);
    });
  });
}

function resetTodoForm() {
  $("#todo_id").val("");
  $("#create_todo_form")[0].reset();
  $("#todoModalLabel").text("Add a todo");
}

$(function () {
  const todoModal = new bootstrap.Modal(document.getElementById("todoModal"));
  const showModal = new bootstrap.Modal(
    document.getElementById("showTodoModal"),
  );

  // Get all todos
  loadTodos();

  // Ouvrir le modal en mode création
  $("#open_create_modal").on("click", function () {
    resetTodoForm();
  });

  // Créer ou modifier un todo (formulaire unique pour les 2 cas)
  $("#create_todo_form").on("submit", function (e) {
    e.preventDefault();

    const todoId = $("#todo_id").val();
    const title = $("#title").val().trim();
    const content = $("#content").val().trim();

    if (!title) {
      showToast("Title is required", "warning");
      return;
    }

    const isEdit = !!todoId;
    const url = isEdit ? `/update_todo/${todoId}` : "/create_todo";

    $.ajax({
      method: "POST",
      url: url,
      contentType: "application/json",
      data: JSON.stringify({ title: title, content: content }),
      success: function () {
        todoModal.hide();
        resetTodoForm();
        showToast("Succesfull done");
        loadTodos();
      },
      error: function (xhr, status, error) {
        showToast("Error while saving: " + error, "error");
      },
    });
  });

  // Voir un todo
  $("#todos").on("click", ".show", function () {
    const id = $(this).data("id");
    $.getJSON(`/get_todo/${id}`, function (response) {
      const todo = response.todo;
      $("#show_todo_title").text(todo[1]);
      $("#show_todo_content").text(todo[2] || "(No content)");
      $("#show_todo_status").html(statusBadge(!!todo[3]));
      showModal.show();
    });
  });

  // Modifier un todo : pré-remplir le formulaire puis ouvrir le modal
  $("#todos").on("click", ".edit", function () {
    const id = $(this).data("id");
    $.getJSON(`/get_todo/${id}`, function (response) {
      const todo = response.todo;
      $("#todo_id").val(todo[0]);
      $("#title").val(todo[1]);
      $("#content").val(todo[2]);
      $("#todoModalLabel").text("Edit todo");
      todoModal.show();
    });
  });

  // Cocher/décocher : bascule le statut done
  $("#todos").on("change", ".todo-checkbox", function () {
    const id = $(this).data("id");
    const done = $(this).is(":checked");
    $.ajax({
      method: "POST",
      url: `/toggle_todo/${id}`,
      contentType: "application/json",
      data: JSON.stringify({ done: done }),
      success: function () {
        loadTodos();
      },
      error: function () {
        showToast("Error while updating status", "error");
      },
    });
  });

  // Delete todo
  $("#todos").on("click", ".delete", function () {
    const id = $(this).data("id");
    showConfirmModal("Delete this todo?", function () {
      $.ajax({
        method: "POST",
        url: `/delete_todo/${id}`,
        success: function () {
          loadTodos();
          showToast("Todo deleted successfully");
        },
        error: function () {
          showToast("Error while deleting the todo", "error");
        },
      });
    });
  });
});
