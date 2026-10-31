<script setup>
  // Root layout Daymark
  import TaskForm from './components/TaskForm.vue'
  import TaskList from './components/TaskList.vue'

  const previewTasks = [
    {
      id: 1,
      title: 'Review API contract',
      description: 'Check request and response fields.',
      status: 'Todo',
    },
    {
      id: 2,
      title: 'Build the task form',
      description: 'Prepare the form for the next integration step.',
      status: 'In Progress',
    },
    {
      id: 3,
      title: 'Set up the project',
      description: 'Vue and Vite are ready.',
      status: 'Done',
    },
  ]
</script>

<template>
  <div class="app-shell">
    <header class="site-header">
      <div class="site-brand">DAYMARK</div>
      <p class="header-caption">Simple task tracker</p>
    </header>

    <main class="main-content">
      <section class="page-intro" aria-labelledby="page-title">
        <h1 id="page-title">Welcome!</h1>
        <p class="intro-copy">
          Create and Manage Your Tasks.
        </p>
      </section>

      <div class="workspace-grid">
        <section class="workspace-panel" aria-labelledby="form-heading">
          <div class="section-heading">
            <p class="eyebrow">Create</p>
            <h2 id="form-heading">Add a task</h2>
          </div>

          <TaskForm />
        </section>

        <section class="workspace-panel task-list-region" aria-labelledby="list-heading">
          <div class="section-heading">
            <p class="eyebrow">Your work</p>
            <h2 id="list-heading">Your tasks</h2>
          </div>

          <TaskList :tasks="previewTasks" />
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
    font-size: clamp(1.75rem, 4vw, 2.5rem);
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