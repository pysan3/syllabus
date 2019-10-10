<template>
  <div id="app">
    <header><HeaderDefault/></header>
    <div><router-view/></div>
  </div>
</template>

<script>
import HeaderDefault from '@/components/HeaderDefault'

export default {
  components: {
    HeaderDefault,
  }
}
</script>

<style lang="stylus">
#app
  font-family 'Avenir', Helvetica, Arial, sans-serif
  -webkit-font-smoothing antialiased
  -moz-osx-font-smoothing grayscale
  color #2c3e50
  text-align center
.row
  margin 0px
</style>
