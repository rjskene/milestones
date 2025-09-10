<template>
  <div id="app">
    <nav class="navbar bg-primary">
      <div class="container d-flex justify-between align-center">
        <div class="nav-brand">
          <h1 class="text-white m-0">Milestones</h1>
        </div>
        <div class="nav-links d-flex">
          <router-link to="/" class="nav-link text-white">Dashboard</router-link>
          <router-link to="/chart" class="nav-link text-white">Gantt</router-link>
          <router-link to="/projects" class="nav-link text-white">Projects</router-link>
          <router-link to="/milestones" class="nav-link text-white">Milestone</router-link>
          <router-link to="/equipment" class="nav-link text-white">Sales</router-link>
        </div>
      </div>
    </nav>
    
    <main class="main-content">
      <div class="container">
        <router-view />
      </div>
    </main>
  </div>
</template>

<script setup>
// Main app component with navigation
</script>

<style>
#app {
  min-height: 100vh;
}

.navbar {
  padding: var(--spacing-lg) 0;
  box-shadow: var(--shadow-md);
}

.nav-brand h1 {
  font-size: var(--font-size-2xl);
  font-weight: 600;
}

.nav-links {
  gap: var(--spacing-lg);
}

.nav-link {
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--radius-sm);
  transition: background-color var(--transition-normal);
  text-decoration: none;
}

.nav-link:hover,
.nav-link.router-link-active {
  background-color: rgba(255, 255, 255, 0.2);
}

.main-content {
  padding: var(--spacing-xl) 0;
}

@media (max-width: 768px) {
  .navbar .container {
    flex-direction: column;
    gap: var(--spacing-md);
  }
  
  .nav-links {
    flex-wrap: wrap;
    justify-content: center;
  }
}
</style>