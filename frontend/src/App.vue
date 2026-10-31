<script setup>
  import { onMounted, ref } from 'vue'
  
  import TaskForm from './components/TaskForm.vue'
  import TaskList from './components/TaskList.vue'
  import {
    createTask,
    deleteTask,
    getTasks,
    updateTask,
  } from './services/taskService.js'
  
  const tasks = ref([])
  const isLoading = ref(true)
  const loadError = ref('')
  const formError = ref('')
  const deleteError = ref('')
  const isMutating = ref(false)
  const deletingTaskId = ref(null)
  const formVersion = ref(0)
  const editingTask = ref(null)
  
  async function loadTasks() {
    isLoading.value = true
    loadError.value = ''
  
    try {
      const responseTasks = await getTasks()
  
      if (!Array.isArray(responseTasks)) {
        throw new Error('Backend mengirim format daftar task yang tidak valid.')
      }
  
      tasks.value = responseTasks
    } catch (error) {
      console.error('Gagal memuat daftar task:', error)
      loadError.value =
        error instanceof Error ? error.message : 'Gagal memuat daftar task.'
    } finally {
      isLoading.value = false
    }
  }
  
  function startEdit(task) {
    if (isMutating.value) {
      return
    }
  
    editingTask.value = task
    formError.value = ''
  }
  
  function cancelEdit() {
    if (isMutating.value) {
      return
    }
  
    editingTask.value = null
    formError.value = ''
  }
  
  async function handleCreateTask(taskData) {
    if (isMutating.value) {
      return
    }
  
    isMutating.value = true
    formError.value = ''
  
    try {
      const createdTask = await createTask(taskData)
      tasks.value = [...tasks.value, createdTask]
      formVersion.value += 1
    } catch (error) {
      console.error('Gagal membuat task:', error)
      formError.value =
        error instanceof Error ? error.message : 'Gagal membuat task.'
    } finally {
      isMutating.value = false
    }
  }
  
  async function handleUpdateTask(taskData) {
    if (isMutating.value) {
      return
    }
  
    const taskBeingEdited = editingTask.value
  
    if (!taskBeingEdited) {
      return
    }
  
    isMutating.value = true
    formError.value = ''
  
    try {
      const updatedTask = await updateTask(taskBeingEdited.id, taskData)
  
      tasks.value = tasks.value.map((task) =>
        task.id === updatedTask.id ? updatedTask : task,
      )
  
      editingTask.value = null
    } catch (error) {
      console.error('Gagal memperbarui task:', error)
      formError.value =
        error instanceof Error ? error.message : 'Gagal memperbarui task.'
  
      if (error?.status === 404) {
        await loadTasks()
      }
    } finally {
      isMutating.value = false
    }
  }
  
  async function handleFormSubmit(taskData) {
    if (isMutating.value) {
      return
    }
  
    if (editingTask.value) {
      await handleUpdateTask(taskData)
      return
    }
  
    await handleCreateTask(taskData)
  }
  
  async function handleDeleteTask(taskId) {
    if (isMutating.value) {
      return
    }
  
    const taskToDelete = tasks.value.find((task) => task.id === taskId)
  
    if (!taskToDelete) {
      return
    }
  
    const confirmed = window.confirm(
      `Delete "${taskToDelete.title}"? This cannot be undone.`,
    )
  
    if (!confirmed) {
      return
    }
  
    isMutating.value = true
    deletingTaskId.value = taskId
    deleteError.value = ''
  
    try {
      await deleteTask(taskId)
      tasks.value = tasks.value.filter((task) => task.id !== taskId)
    } catch (error) {
      console.error('Gagal menghapus task:', error)
      deleteError.value =
        error instanceof Error ? error.message : 'Gagal menghapus task.'
  
      if (error?.status === 404) {
        await loadTasks()
      }
    } finally {
      isMutating.value = false
      deletingTaskId.value = null
    }
  }
  
  onMounted(loadTasks)
</script>

<template>
  <div class="app-shell">
    <header class="site-header">
      <div class="site-brand">DAYMARK</div>
      <p class="header-caption">Simple task tracker</p>
    </header>

    <main class="main-content">
      <section class="page-intro" aria-labelledby="page-title">
        <h1 id="page-title">Tasks</h1>
        <p class="intro-copy">Create and manage your tasks.</p>
      </section>

      <div class="workspace-grid">
        <section class="workspace-panel" aria-labelledby="form-heading">
          <div class="section-heading">
            <p class="eyebrow">{{ editingTask ? 'Update' : 'Create' }}</p>
            <h2 id="form-heading">
              {{ editingTask ? 'Edit task' : 'Add a task' }}
            </h2>
          </div>

          <TaskForm
            :key="formVersion"
            :task="editingTask"
            :submitting="isMutating"
            @submit="handleFormSubmit"
            @cancel="cancelEdit"
          />

          <p v-if="formError" class="form-request-error" role="alert">
            {{ formError }}
          </p>
        </section>

        <section
          class="workspace-panel task-list-region"
          aria-labelledby="list-heading"
        >
          <div class="section-heading">
            <p class="eyebrow">Your work</p>
            <h2 id="list-heading">Your tasks</h2>
          </div>

          <p v-if="deleteError" class="request-error" role="alert">
            {{ deleteError }}
          </p>

          <p v-if="isLoading" class="request-state" role="status">
            Loading tasks…
          </p>

          <p
            v-else-if="loadError && tasks.length === 0"
            class="request-state request-state--error"
            role="alert"
          >
            {{ loadError }}
          </p>

          <template v-else>
            <p
              v-if="loadError"
              class="request-error"
              role="alert"
            >
              {{ loadError }}
            </p>

            <TaskList
              :tasks="tasks"
              :deleting-task-id="deletingTaskId"
              :is-mutating="isMutating"
              @edit="startEdit"
              @delete="handleDeleteTask"
            />
          </template>
        </section>
      </div>
    </main>
  </div>
</template>

<style scoped>
  .app-shell {
    min-height: 100vh;
  }
  
  .site-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    max-width: 1120px;
    margin: 0 auto;
    padding: var(--space-4) var(--space-8);
    border-bottom: 1px solid var(--color-border);
  }
  
  .site-brand {
    color: var(--color-text-primary);
    font-size: var(--font-size-body);
    font-weight: 750;
    letter-spacing: 0.14em;
  }
  
  .header-caption {
    color: var(--color-text-secondary);
    font-size: var(--font-size-small);
  }
  
  .main-content {
    max-width: 1120px;
    margin: 0 auto;
    padding: var(--space-12) var(--space-8);
  }
  
  .page-intro {
    max-width: 620px;
    margin-bottom: var(--space-8);
  }
  
  .eyebrow {
    margin-bottom: var(--space-2);
    color: var(--color-accent);
    font-size: var(--font-size-small);
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
  }
  
  .page-intro h1 {
    margin-bottom: var(--space-3);
    color: var(--color-text-primary);
    font-size: clamp(1.75rem, 4vw, 2.25rem);
    line-height: var(--line-height-heading);
  }
  
  .intro-copy {
    color: var(--color-text-secondary);
    line-height: var(--line-height-body);
  }
  
  .workspace-grid {
    display: grid;
    grid-template-columns: minmax(260px, 0.9fr) minmax(0, 1.6fr);
    align-items: start;
    gap: var(--space-8);
  }
  
  .workspace-panel {
    min-width: 0;
    padding: var(--space-6);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-large);
    background-color: var(--color-surface);
  }
  
  .section-heading {
    margin-bottom: var(--space-6);
  }
  
  .section-heading h2 {
    color: var(--color-text-primary);
    font-size: var(--font-size-large);
    line-height: var(--line-height-heading);
  }
  
  .form-request-error,
  .request-error {
    padding: var(--space-3) var(--space-4);
    border: 1px solid var(--color-accent);
    border-radius: var(--radius-medium);
    color: var(--color-accent);
    font-size: var(--font-size-small);
    overflow-wrap: anywhere;
  }
  
  .form-request-error {
    margin-top: var(--space-4);
  }
  
  .request-error {
    margin-bottom: var(--space-4);
  }
  
  .request-state {
    display: grid;
    min-height: 160px;
    place-items: center;
    padding: var(--space-6);
    border: 1px dashed var(--color-border);
    border-radius: var(--radius-medium);
    color: var(--color-text-secondary);
    font-size: var(--font-size-small);
    text-align: center;
  }
  
  .request-state--error {
    border-color: var(--color-accent);
    color: var(--color-accent);
  }
  
  @media (max-width: 820px) {
    .site-header {
      padding: var(--space-4);
    }
  
    .main-content {
      padding: var(--space-8) var(--space-4);
    }
  
    .workspace-grid {
      grid-template-columns: minmax(0, 1fr);
      gap: var(--space-6);
    }
  
    .workspace-panel {
      padding: var(--space-4);
    }
  }
  
  @media (max-width: 480px) {
    .main-content {
      padding-top: var(--space-6);
      padding-bottom: var(--space-6);
    }
  
    .page-intro {
      margin-bottom: var(--space-6);
    }
  }
</style>