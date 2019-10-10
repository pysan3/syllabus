import Vue from 'vue'
import Vuex from 'vuex'
Vue.use(Vuex)

const state = {
  base_url: 'http://127.0.0.1:5042',
}

export default new Vuex.Store({
  state,
})
