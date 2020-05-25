import Vue from 'vue'
import Router from 'vue-router'
import main from '@/components/main'
import wave from '@/components/wave'

Vue.use(Router)

export default new Router({
    routes: [{
            path: '/',
            name: 'main',
            component: main
        },
        {
            path: '/wave',
            name: 'wave',
            component: wave,
            meta: {
                keepAlive: false,
                isBack: false
            }
        }
    ]
})