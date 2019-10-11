<template>
  <div class="row">
    <nav id="sidebar" class="col-3 col-lg-2 d-none d-md-block text-left border-right">
      <h3 class="rounded bg-dark text-white border border-dark" style="margin: 4px 0px; padding: 6px 12px;">Search</h3>
      <Searchbar @search="select_buildings"/>
    </nav>
    <div id="content" class="col-12 col-md-9 col-lg-10">
      <div class="border rounded text-left mb-3 d-md-none">
        <button class="btn btn-dark mx-3 my-1" data-toggle="collapse" data-target="#searchbar-holder" aria-expand="false" aria-controls="searchbar-holder">
          Search
        </button>
        <div class="collapse" id="searchbar-holder">
          <div class="card card-body border-0 p-0">
            <Searchbar @search="select_buildings"/>
          </div>
        </div>
      </div>
      <div id="rooms" class="row">
        <div v-for="b in Object.keys(building).sort((a, b) => Object.keys(building[b]).length - Object.keys(building[a]).length)" :key="b" class="col-6 col-md-3">
          <table class="table">
            <thead class="thead-light"><tr><th class="text-left">{{ b }}号館</th></tr></thead>
            <tr v-for="r in Object.keys(building[b])" :key="r"><th>{{ r }}</th></tr>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Searchbar from '@/components/Searchbar'

export default {
  components: {
    Searchbar
  },
  computed: mapState([
    'base_url',
    'rooms'
  ]),
  data () {
    return {
      building: {}
    }
  },
  methods: {
    select_buildings (func) {
      this.building = {}
      for (let k in this.rooms){
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
  async created () {
    await this.$store.dispatch('search_room', {
      term: -1,
      weekday: -1,
      period: -1
    })
    this.select_buildings((b, r, v) => v === 0)
  }
}
</script>