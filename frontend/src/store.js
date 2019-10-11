import Vue from 'vue'
import Vuex from 'vuex'
import Axios from 'axios'
Vue.use(Vuex)

const state = {
  base_url: 'http://127.0.0.1:5042',
  rooms: []
}

const mutations = {
  update_rooms (state, r) {
    state.rooms = r
  }
}

const actions = {
  search_room ({ commit }, {term, weekday, period}) {
    return Axios.get(state.base_url + '/roomon', {params: {
      term: term,
      weekday: weekday,
      period: period
    }}).then(resp => commit('update_rooms', resp.data))
  }
}

export default new Vuex.Store({
  state,
  mutations,
  actions
})
