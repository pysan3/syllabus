<template>
  <div id="searchbar" class="px-3 py-2">
    <h4>絞り込み</h4>
    <div class="d-flex border rounded mb-2">
      <div class="bg-light flex-shrink-1 rounded-left border-right" style="padding: 6px 12px;">
        <input type="checkbox" @change="disp_free^=1; search();" checked>
      </div>
      <div style="padding: 6px 12px;">空室のみ表示</div>
    </div>
    <div class="d-flex border rounded mb-2">
      <div class="bg-light flex-shrink-1 rounded-left border-right" style="padding: 6px 12px;">
        <input type="checkbox" @change="first_floor^=1; search();">
      </div>
      <div style="padding: 6px 12px;">1階のみ表示</div>
    </div>
    <div class="input-group mb-2">
      <input type="text" class="rounded-left" style="width: 40px;" v-model="building" @change="search()">
      <div class="input-group-append bg-light">
        <span class="input-group-text">号館のみ表示</span>
      </div>
    </div>
    <hr class="my-2">
    <h4>時間</h4>
    <div class="input-group mb-2">
      <input type="text" class="rounded-left" style="width: 40px;" v-model="time.term" @change="time_on()">
      <div class="input-group-append bg-light">
        <span class="input-group-text">学期</span>
      </div>
    </div>
    <div class="input-group mb-2">
      <input type="text" class="rounded-left" style="width: 40px;" v-model="time.weekday" @change="time_on()">
      <div class="input-group-append bg-light">
        <span class="input-group-text">曜日</span>
      </div>
    </div>
    <div class="input-group mb-2">
      <input type="text" class="rounded-left" style="width: 40px;" v-model="time.period" @change="time_on()">
      <div class="input-group-append bg-light">
        <span class="input-group-text">時限</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      disp_free: true,
      first_floor: false,
      building: '',
      time: {
        term: '',
        weekday: '',
        period: '',
      }
    }
  },
  methods: {
    search () {
      const vm = this
      const check = [
        (b, r, v) => !vm.disp_free || v === 0,
        (b, r, v) => vm.building === '' || parseInt(vm.building, 10) === b,
        (b, r, v) => !vm.first_floor || Math.floor(r / 100) === 1,
      ]
      this.$emit('search', (b, r, v) => check.map(x => x(b, r, v)).reduce((a, b) => a && b))
    },
    async time_on () {
      const data = {
        term: this.time.term === '' ? -1 : parseInt(this.time.term),
        weekday: this.time.weekday === '' ? -1 : parseInt(this.time.weekday),
        period: this.time.period === '' ? -1 : parseInt(this.time.period)
      }
      for (const k in data) {
        if (data[k] === -1);
        else if (isNaN(data[k])) data[k] = this.time[k]
        else {
          let msg = ''
          const msg_name = {term: '学期', weekday: '曜日', period: '時限'}
          const limits = {term: [0, 3], weekday: [0, 6], period: [1, 7]}
          if (data[k] < limits[k][0]) {
            alert(`${msg_name[k]}を${limits[k][0]}以上にしてください。`)
            return
          }
          else if (data[k] > limits[k][1]) {
            alert(`${msg_name[k]}を${limits[k][1]}以下にしてください。`)
            return
          }
        }
      }
      await this.$store.dispatch('search_room', data)
      this.search()
    }
  }
}
</script>