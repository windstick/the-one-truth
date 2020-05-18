import Vue from 'vue'
import Router from 'vue-router'
import Game from '@/components/Game'
import test from '@/components/test'

Vue.use(Router)

export default new Router({
    routes: [{
            path: '/',
            name: 'Game',
            component: Game
        },
        {
            path: '/test',
            name: 'test',
            component: test
        }
    ]
})