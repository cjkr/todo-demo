<script>
  // @ts-ignore
  import axios from "axios";
  import { onMount } from "svelte";

  let newToDo = "";
  let todos = [];

  onMount(async () => {
    try {
      let response = await axios.get("http://127.0.0.1:5000/api/v1/todos/");
      let data = response.data;
      console.log(data);
      if (data.todos.length > 0) {
        todos = [...data.todos];
      }
    } catch (e) {
      console.error(e.message);
    }
  });

  let submitTodo = async () => {
    let response = await axios
      .post(
        "http://127.0.0.1:5000/api/v1/todos/",
        {
          text: newToDo,
        },
        {
          headers: {
            "Access-Control-Allow-Origin": "http://127.0.0.1:5000",
            "Content-Type": "application/json",
          },
          withCredentials: false,
        }
      )
      .then((data) => {
        console.log(data);
        todos = [
          ...todos,
          {
            text: data.data.todo.text,
            is_completed: false,
            updated_at: data.data.todo.created_at,
            id: data.data.todo.id,
          },
        ];
        newToDo = "";
      })
      .catch((e) => {
        console.error(e);
      });
  };

  function handleCompleteTodo(id) {
    console.log(id);

    let response = axios
      .get(`http://127.0.0.1:5000/api/v1/todos/toggle_completed/${id}`)
      .then((data) => {
        todos = todos.map((todo) =>
          todo.id === id ? { ...todo, is_completed: !todo.is_completed } : todo
        );
      });
  }

  function deleteTodo(id) {
    let response = axios
      .delete(`http://127.0.0.1:5000/api/v1/todos/${id}`)
      .then(() => {
        todos = todos.filter((todo) => todo.id !== id);
      });
  }
</script>

<main class="container">
  <h2 class="display-6 text-center m-5">TO-DO Manager</h2>
  <form class="row" on:submit|preventDefault={submitTodo}>
    <div class="form-floating mb-3 col-sm-9">
      <input
        type="text"
        class="form-control flex-fill"
        name="Label"
        id="Label"
        placeholder="TODO here"
        bind:value={newToDo}
      />
      <label for="floatingLabel" class="ms-2">TODO</label>
    </div>
    <div class="col-sm-3 mb-3">
      <button
        type="submit"
        class="btn btn-primary h-100 w-100 fw-bold"
        on:click|preventDefault={submitTodo}>Add TO-DO</button
      >
    </div>
  </form>
  <ul class="list-group">
    {#each todos as todo}
      <div class="d-flex flex-row">
        <li class="list-group-item flex-fill todo-entry">
          <input
            class="form-check-input me-3"
            type="checkbox"
            name=""
            id=""
            on:click={() => handleCompleteTodo(todo.id)}
          />
          <span
            class={todo.is_completed
              ? "text-decoration-line-through text-muted"
              : "fw-light"}>{todo.text}</span
          >
        </li>
        <button class="btn btn-outline-success">
          <i class="bi bi-pencil" />
        </button>
        <button
          class="btn btn-danger delete-button"
          on:click={() => deleteTodo(todo.id)}
          ><i class="bi bi-trash" />
        </button>
      </div>
    {/each}
  </ul>
</main>

<style>
  main {
    width: 600px;
  }

  .delete-button {
    border: 1px solid #dee2e6;
    border-radius: 0 0.5em 0.5em 0 !important;
  }

  .todo-entry {
    border-radius: 0.5em 0 0 0.5em !important;
  }
</style>
