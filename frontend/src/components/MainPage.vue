<template>
  <div id="main-page">
    <Header />
    <Sidebar />
    <Workspace />
  </div>
</template>

<script>
import Header from './HeaDer.vue';
import Sidebar from './SideBar.vue';
import Workspace from './WorkSpace.vue';

export default {
  components: {
    Header,
    Sidebar,
    Workspace,
  },
};
</script>
