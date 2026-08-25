function loadTodos() {
  $.getJSON("/get_todos", function (response) {
    const todosDiv = $("#todos");
    todosDiv.empty(); // Vide le conteneur avant d'ajouter le contenu

    // response.todos contient la liste des tableaux [id, title, content, done]
    response.todos.forEach(function (todo) {
      const id = todo[0];
      const title = todo[1];
      const content = todo[2];
      const isDone = todo[3];

      // Génération du bloc HTML pour chaque tâche
      const todoHtml = `
      <div class="todo-item ${isDone ? "completed" : ""}" id="todo-${id}">
        <h3>${title}</h3>
        <p>${content}</p>
        <span>Statut : ${isDone ? "Terminé" : "À faire"}</span>
      </div>
    `;

      todosDiv.append(todoHtml);
    });
  });
}

$(function () {
  loadTodos();

  $("#create_todo").on("click", function (e) {
    let title = $("#title").val();
    let content = $("#content").val();
    e.preventDefault();
    if (title && content) {
      $.ajax({
        method: "POST",
        url: "/create_todo",
        contentType: "application/json",
        data: JSON.stringify({
          title: title,
          content: content,
        }),
      });
      $("#create_todo_form")[0].reset();
      loadTodos();
    }
  });
});
