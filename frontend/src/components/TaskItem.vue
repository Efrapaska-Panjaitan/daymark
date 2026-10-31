<script setup>
  import { computed } from 'vue'
  
  const props = defineProps({
    task: {
      type: Object,
      required: true,
    },
    deleting: {
      type: Boolean,
      default: false,
    },
    disabled: {
      type: Boolean,
      default: false,
    },
  })
  
  const emit = defineEmits(['edit', 'delete'])
  
  const statusClass = computed(() => {
    if (props.task.status === 'In Progress') {
      return 'status-badge--progress'
    }
  
    if (props.task.status === 'Done') {
      return 'status-badge--done'
    }
  
    return 'status-badge--todo'
  })
  
  function requestEdit() {
    emit('edit', props.task)
  }
  
  function requestDelete() {
    if (!props.disabled && !props.deleting) {
      emit('delete', props.task.id)
    }
  }
</script>

<template>
  <article class="task-item">
    <div class="task-content">
      <div class="task-heading">
        <h3>{{ task.title }}</h3>
        <span class="status-badge" :class="statusClass">
          {{ task.status }}
        </span>
      </div>

      <p v-if="task.description" class="task-description">
        {{ task.description }}
      </p>
      <p v-else class="task-description task-description--empty">
        No description.
      </p>
    </div>

    <div class="task-actions">
      <button
        class="action-button"
        type="button"
        :aria-label="'Edit task: ' + task.title"
        :disabled="disabled || deleting"
        @click="requestEdit"
      >
        Edit
      </button>
      <button
        class="action-button action-button--delete"
        type="button"
        :aria-label="'Delete task: ' + task.title"
        :disabled="disabled || deleting"
        @click="requestDelete"
      >
        {{ deleting ? 'Deleting…' : 'Delete' }}
      </button>
    </div>
  </article>
</template>

<style scoped>
  .task-item {
    display: grid;
    grid-template-columns: minmax(0, 1fr) auto;
    align-items: start;
    gap: var(--space-4);
    padding: var(--space-4) 0;
    border-bottom: 1px solid var(--color-border);
  }
  
  .task-item:last-child {
    border-bottom: 0;
  }
  
  .task-content {
    min-width: 0;
  }
  
  .task-heading {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: var(--space-2) var(--space-3);
  }
  
  .task-heading h3 {
    min-width: 0;
    color: var(--color-text-primary);
    font-size: var(--font-size-body);
    line-height: var(--line-height-heading);
    overflow-wrap: anywhere;
  }
  
  .status-badge {
    display: inline-flex;
    flex: 0 0 auto;
    align-items: center;
    padding: 0.2rem var(--space-3);
    border-radius: var(--radius-pill);
    font-size: var(--font-size-small);
    font-weight: 600;
    line-height: var(--line-height-body);
  }
  
  .status-badge--todo {
    background-color: var(--color-status-todo-background);
    color: var(--color-status-todo-text);
  }
  
  .status-badge--progress {
    background-color: var(--color-status-progress-background);
    color: var(--color-status-progress-text);
  }
  
  .status-badge--done {
    background-color: var(--color-status-done-background);
    color: var(--color-status-done-text);
  }
  
  .task-description {
    margin-top: var(--space-2);
    color: var(--color-text-secondary);
    font-size: var(--font-size-small);
    line-height: var(--line-height-body);
    overflow-wrap: anywhere;
  }
  
  .task-description--empty {
    font-style: italic;
  }
  
  .task-actions {
    display: flex;
    align-items: center;
    gap: var(--space-1);
  }
  
  .action-button {
    min-height: 44px;
    padding: var(--space-2) var(--space-3);
    border: 0;
    border-radius: var(--radius-small);
    background: transparent;
    color: var(--color-text-secondary);
    font: inherit;
    font-size: var(--font-size-small);
    font-weight: 600;
    cursor: pointer;
  }
  
  .action-button:not(:disabled):hover {
    background-color: var(--color-background);
    color: var(--color-text-primary);
  }
  
  .action-button--delete:not(:disabled):hover {
    color: var(--color-accent);
  }
  
  .action-button:disabled {
    opacity: 0.65;
    cursor: wait;
  }
  
  @media (max-width: 560px) {
    .task-item {
      grid-template-columns: minmax(0, 1fr);
    }
  
    .task-actions {
      justify-content: flex-end;
    }
  }
</style>