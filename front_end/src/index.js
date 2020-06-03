import Vue from 'vue';
import VeeValidate from 'vee-validate';

import { store } from './_store';
import { router } from './_helpers';
import App from './app/App';
import axios from 'axios'
import VueAxios from 'vue-axios'

Vue.use(VeeValidate);

// setup fake backend
// import { configureFakeBackend } from './_helpers';
// configureFakeBackend();

Vue.use(VueAxios, axios)
Vue.prototype.$axios = axios;
axios.defaults.baseURL = '/api'
axios.defaults.headers.post['Content-Type'] = 'application/json';

new Vue({
    el: '#app',
    router,
    store,
    render: h => h(App)
});