import Vue from 'vue'
import App from './App.vue'
import router from './router'

import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import axios from 'axios'
import store from './store'

Vue.use(ElementUI);

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')

/*
import {request} from '@/network/request'

request({
  method: 'post',
  url: '/api/get_friends_list/',
  data: {
    username: 'Ivy'
  }
}).then(msg =>{
  console.log(msg)
})
*/