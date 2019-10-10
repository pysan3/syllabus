import Vue from 'vue'
import Router from 'vue-router'
Vue.use(Router)

const routerOptions = [
  { path: '/', component: 'Home' },
  { path: '*', component: 'HelloWorld' },
]

const routes = routerOptions.map(route => ({
  path: route.path,
  name: `${route.component}`.toLowerCase(),
  component: () => import(`@/views/${route.component}.vue`),
  meta: {
    requiredAuth: route.requiredAuth
  }
}))

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})