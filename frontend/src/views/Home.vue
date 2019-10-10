<template>
  <div id="home">
    <div id="rooms" class="row">
      <div v-for="b in Object.keys(building).sort((a, b) => Object.keys(building[b]).length - Object.keys(building[a]).length)" :key="b" class="col-6 col-md-2">
        <table class="table">
          <thead class="thead-light"><tr><th>{{ b }}</th></tr></thead>
          <tr v-for="r in Object.keys(building[b])" :key="r"><th>{{ r }}</th></tr>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import Axios from 'axios'
import { mapState } from 'vuex'

export default {
  computed: mapState([
    'base_url'
  ]),
  data () {
    return {
      rooms: [],
      building: {}
    }
  },
  methods: {
    search_room (term, weekday, period) {
      Axios.get(this.base_url + '/roomon', {params: {
        term: term,
        weekday: weekday,
        period: period
      }}).then(resp => {
        this.rooms = resp.data
        for (const k in this.rooms) {
          const b = parseInt(k.split('_')[0].replace('r', ''), 10)
          const r = parseInt(k.split('_')[1], 10)
          b in this.building || (this.building[b] = {})
          this.building[b][r] = this.rooms[k]
        }
        this.$forceUpdate()
      })
    },
    select_buildings (func) {
      this.building = {}
      for (k in this.rooms){
        const b = parseInt(k.split('_')[0].replace('r', ''), 10)
        const r = parseInt(k.split('_')[1], 10)
        const v = parseInt(this.rooms[k], 10)
        if (func(b, r, v)) {
          b in this.building || (this.building[b] = {})
          this.building[b][r] = this.rooms[k]
        }
      }
      this.$forceUpdate()
    }
  },
  created () {
    this.search_room(-1, -1, -1)
  }
}
</script>
