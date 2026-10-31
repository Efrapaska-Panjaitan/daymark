<script setup>
import TaskItem from './TaskItem.vue'

defineProps({
  tasks: {
    type: Array,
    default: () => [],
  },
})

const emit = defineEmits(['edit', 'delete'])

function forwardEdit(task) {
  emit('edit', task)
}

function forwardDelete(taskId) {
  emit('delete', taskId)
}
</script>

<template>
  <div class="task-list">
    <p v-if="tasks.length === 0" class="empty-state" role="status">
      No tasks yet. Add your first task.
    </p>

    <ul v-else class="task-items">
      <li v-for="task in tasks" :key="task.id">
        <TaskItem
          :task="task"
          @edit="forwardEdit"
          @delete="forwardDelete"
        />
      </li>
    </ul>
  </div>
</template>

<style scoped>
  .task-list {
    min-width: 0;
  }
  
  .task-items {
    list-style: none;
  }
  
  .empty-state {
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
</style>
