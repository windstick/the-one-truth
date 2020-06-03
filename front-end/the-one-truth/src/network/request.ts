import axios from 'axios'

export function request(config){
    const instance = axios.create({
        timeout: 5000
    })

    instance.interceptors.response.use(result =>{
        return result.data
    })

    return instance(config)
}