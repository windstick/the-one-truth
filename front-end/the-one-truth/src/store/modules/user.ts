import {request} from '@/network/request'

const state = {
    login: false,
    user_id: 0,
    name: "Ivy",
    passwd: "psIvywd",

    friend_list: [{name: 'user1'}, {name: 'user2'}, {name: 'user3'}, {name: 'user4'}]
}


const mutations = {
    updateFriendList(state, newFriendList){
        state.friend_list = newFriendList
    },
    setName(state, newName){
        state.name = newName
    },
    logIn(state){
        state.login = true
    },
    logOut(state){
        state.login = false
    }
}


const actions = {
    updateFriendListFromNetwork(context){
        // console.log(context.state.name)
        request({
            method: 'post',
            url: '/api/get_friends_list/',
            data: {
              username: context.state.name
            }
        }).then(msg =>{
            // console.log(msg.data.friend_list.map(function(user){return {name: user}}))
            context.commit('updateFriendList', msg.data.friend_list.map(function(user){return {name: user}}))
        }).catch(err => {
            console.log(err)
        })
    }
}

export default {
    namespaced: true,
    state,
    mutations,
    actions
  }