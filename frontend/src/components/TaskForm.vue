<script setup>
  import { computed, ref, watch } from 'vue'
  
  const props = defineProps({
    task: {
      type: Object,
      default: null,
    },
    submitting: {
      type: Boolean,
      default: false,
    },
  })
  
  const emit = defineEmits(['submit', 'cancel'])
  
  const title = ref('')
  const description = ref('')
  const status = ref('Todo')
  const titleError = ref('')
  
  const isEditing = computed(() => props.task !== null)
  
  watch(
    () => props.task,
    (task) => {
      title.value = task?.title ?? ''
      description.value = task?.description ?? ''
      status.value = task?.status ?? 'Todo'
      titleError.value = ''
    },
    { immediate: true },
  )
  
  function clearTitleError() {
    titleError.value = ''
  }
  
  function handleSubmit() {
    if (props.submitting) {
      return
    }
  
    const normalizedTitle = title.value.trim()
  
    if (!normalizedTitle) {
      titleError.value = 'Title tidak boleh kosong atau hanya berisi spasi.'
      return
    }
  
    if (normalizedTitle.length > 255) {
      titleError.value = 'Title maksimal 255 karakter.'
      return
    }
  
    titleError.value = ''
  
    emit('submit', {
      title: normalizedTitle,
      description: description.value,
      status: status.value,
    })
  }
  
  function handleCancel() {
    emit('cancel')
  }
</script>

<template>
  <form
    class="task-form"
    novalidate
    :aria-busy="submitting"
    @submit.prevent="handleSubmit"
  >
    <div class="form-field">
      <label for="task-title">
        Title <span class="required-mark" aria-hidden="true">*</span>
      </label>
      <input
        id="task-title"
        v-model="title"
        type="text"
        maxlength="255"
        autocomplete="off"
        required
        :disabled="submitting"
        :aria-invalid="titleError ? 'true' : 'false'"
        :aria-describedby="titleError ? 'task-title-error' : undefined"
        @input="clearTitleError"
      />
      <p
        v-if="titleError"
        id="task-title-error"
        class="form-error"
        role="alert"
      >
        {{ titleError }}
      </p>
    </div>

    <div class="form-field">
      <label for="task-description">Description</label>
      <textarea
        id="task-description"
        v-model="description"
        rows="4"
        :disabled="submitting"
      ></textarea>
    </div>

    <div class="form-field">
      <label for="task-status">Status</label>
      <select
        id="task-status"
        v-model="status"
        required
        :disabled="submitting"
      >
        <option value="Todo">Todo</option>
        <option value="In Progress">In Progress</option>
        <option value="Done">Done</option>
      </select>
    </div>

    <div class="form-actions">
      <button
        v-if="isEditing"
        class="button button-secondary"
        type="button"
        :disabled="submitting"
        @click="handleCancel"
      >
        Cancel
      </button>

      <button
        class="button button-primary"
        type="submit"
        :disabled="submitting"
      >
        {{
          submitting
            ? isEditing
              ? 'Saving…'
              : 'Adding…'
            : isEditing
              ? 'Save changes'
              : 'Add task'
        }}
      </button>
    </div>
  </form>
</template>

<style scoped>
  .task-form {
    display: grid;
    gap: var(--space-4);
  }
  
  .form-field {
    display: grid;
    gap: var(--space-2);
  }
  
  .form-field label {
    color: var(--color-text-primary);
    font-size: var(--font-size-small);
    font-weight: 600;
  }
  
  .required-mark {
    color: var(--color-accent);
  }
  
  .form-field input,
  .form-field textarea,
  .form-field select {
    width: 100%;
    padding: var(--space-3);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-medium);
    background-color: var(--color-surface);
    color: var(--color-text-primary);
  }
  
  .form-field textarea {
    min-height: 7rem;
    resize: vertical;
  }
  
  .form-error {
    color: var(--color-accent);
    font-size: var(--font-size-small);
  }
  
  .form-actions {
    display: flex;
    justify-content: flex-end;
    gap: var(--space-3);
    margin-top: var(--space-2);
  }
  
  .button {
    min-height: 44px;
    padding: var(--space-2) var(--space-4);
    border: 1px solid transparent;
    border-radius: var(--radius-medium);
    font-weight: 600;
    cursor: pointer;
  }
  
  .button-primary {
    border-color: var(--color-accent);
    background-color: var(--color-accent);
    color: var(--color-surface);
  }
  
  .button-primary:not(:disabled):hover {
    filter: brightness(0.94);
  }
  
  .button-secondary {
    border-color: var(--color-border);
    background-color: var(--color-surface);
    color: var(--color-text-primary);
  }
  
  .button-secondary:not(:disabled):hover {
    background-color: var(--color-background);
  }
  
  .button:disabled {
    opacity: 0.65;
    cursor: wait;
  }
  
  @media (max-width: 420px) {
    .form-actions {
      display: grid;
      grid-template-columns: minmax(0, 1fr);
    }
  
    .form-actions .button {
      width: 100%;
    }
  }
</style>