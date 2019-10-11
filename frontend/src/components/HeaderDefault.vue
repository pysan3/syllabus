<template>
  <div id="headerDefault" class="header-default">
    <b-navbar toggleable="sm" type="dark" variant="dark" sticky="true">
      <b-navbar-brand to="/" class="mr-auto">FreeroomFinder</b-navbar-brand>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item to="/">Home</b-nav-item>
        </b-navbar-nav>
        <b-navbar-nav class="ml-auto">
          <b-nav-item-dropdown right id="user-dropdown">
            <template slot="button-content">User</template>
            <b-dropdown-item to="/">まだ実装してないよ(´;ω;｀)</b-dropdown-item>
          </b-nav-item-dropdown>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </div>
</template>

<script>
</script>