<template>
  <div class="main">
    <el-container>
  <el-header>语音识别</el-header>
  <el-main>
    <el-row class='grid-content'>
    录音选项：
    <el-button @click= "handleclick()">录音开始</el-button>
    <el-button @click= "handleclicks()">录音结束</el-button>
    <el-button @click= "handleclickp()">录音播放</el-button>
    <el-button @click= "handleclickb()">录音保存</el-button>
    </el-row>
    <!--
    <el-button @click= "changewave()" type= "primary">改变语音文件</el-button>
    
    <audio controls>
  <source id='wid' src= 'http://127.0.0.1:5000/api/download' type="audio/wav">
您的浏览器不支持 audio 元素。
</audio>
-->


    <el-row class='grid-content'>
    <!--  <el-col :span="12" class='grid-content'>  -->
        <el-button @click= "getwavelist()" type= "info">获取语音文件列表</el-button>
    <!--  </el-col>  -->
    <!--  <el-col :span="12" class='grid-content'>  -->
      <el-select v-model="value" placeholder="请选择">
    <el-option
      v-for="item in wl"
      :key="item"
      :label="item"
      :value="item">
    </el-option>
  </el-select>
 <!-- {{value}}  -->
    <!--</el-col> -->
    </el-row>
    <el-row class= 'grid-content'>
          <audio  id= 'waveid' v-bind:src= 'wname' controls>
您的浏览器不支持 audio 元素。
</audio> 
  </el-row>
      <el-row>
       <div class='grid-content bg-purple'>{{speech}}</div>
      </el-row>
     <el-row>
       <div class='grid-content bg-purple'>{{sentence}}</div>
    </el-row>
  </el-main>
  <el-footer>
    <el-button @click= "getsentence()" type= "primary">识别语音</el-button>
    <el-button @click="gowave()"  type="primary">分析语音</el-button>
  </el-footer>
</el-container>
   </div>
</template>

<script>
import Recorder from 'js-audio-recorder'
let recorder = new Recorder()
console.log(recorder)
recorder.config.sampleRate=16000
recorder.outputSampleRate=16000
export default {
  name: 'main',
  data () {
    return {
      msg: 'Hello',
      url: 'http://127.0.0.1:20000/api',
      speech:'speech',
      sentence: 'text',
      value:'',
      sum: 0,
      mytime: '',
      options:{},
      wl: [],
      catchcf:1,
      fname: 'http://127.0.0.1:5000/api/download',
      wname:  'http://127.0.0.1:5000/api/download',
      fname1: '/static/wavelist/20170001P00001A0001.wav'
    }
  },
  methods:{
    getsentence:function(){ 
       const  _this = this;
    /*this.$axios
      .post('/',{fname : this.fanme})
      .then(response => (this.sentence = response.data))
      .catch(function (error) { // 请求失败处理
        console.log(error);
      });*/
      this.axios({
        method: 'post',
        url: '/getsentence',
        data: {
          fname: this.value,
        }
      })
      .then(response => (this.sentence = response.data.r,this.speech=response.data.r_speech));
    },
    getwavelist:function(){
      this.axios({
        method: 'post',
        url: '/wavelist',
      })
  .then(response => (this.wl = response.data.wavelist));
    },
     /*
    changewave:function(){
      var mys = document.getElementById("wid");
      this.fname=this.fname1
      this.$forceUpdate();
      console.log(mys.src)
    },
    
    playSound() {
      audio.src = this.fname;
      audio.play();
    },
    */
    gowave:function(){
      this.axios({
        method: 'post',
        url: '/changefname',
        data: {
          fname: this.value
        }
      })
      .then(response => (this.catchcf = response.data));
      this.$router.push({name:'wave',params:{fname:this.value}})
    },
     handleclick () {
      console.log(1)
      recorder.start()// 开始录音
    },
    handleclicks () {
      console.log(3)
      recorder.stop() // 结束录音
    },
    handleclickp () {
      console.log(4)
      recorder.play() // 录音播放
    },
    handleclickb (){
      this.mytime=new  Date().getTime();
      recorder.downloadWAV(this.mytime);
    }
  },
  watch:{
    value:function(val){
      console.log(7)
      this.axios({
        method: 'post',
        url: '/changefname',
        data: {
          fname: this.value
        }
      })
      .then(response => (this.catchcf = response.data));
      this.speech='speech'
      this.sentence='text'
      let getTimestamp = new  Date().getTime();
      let mywav=document.getElementById("waveid")
      this.wname=this.wname + "?timestamp=" + getTimestamp
      console.log(mywav.src)
      mywav.load()
    }
  },
  created(){
      this.fname='/static/wavelist/20170001P00001A0002.wav'
      //const audio = document.createElement("audio");
      //document.body.appendChild(audio);
  }

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
.el-row {
    margin-bottom: 20px;
    &:last-child {
      margin-bottom: 0;
    }
  }
  .el-col {
    border-radius: 4px;
    text-align: center;
    padding-left: 10px;
    padding-right: 10px;
  }
  .el-col-2{
    border-radius: 4px;
    text-align: center;
    line-height: 300px;
    padding-left: 10px;
    padding-right: 10px;
  }
  .bg-purple-dark {
    background: #99a9bf;
  }
  .bg-purple {
    background: #d3dce6;
  }
  .bg-purple-light {
    background: #e5e9f2;
  }
  .bg-red {
    background: #f56c6c;
  }
  .grid-content {
    border-radius: 4px;
    min-height: 36px;
    line-height: 30px;
  }
  .grid-content2 {
    border-radius: 4px;
    min-height: 36px;
    line-height: 300px;
  }
  .row-bg {
    padding: 10px 0;
    background-color: #f9fafc;
  }
  .el-header, .el-footer {
    background-color: #B3C0D1;
    color: #333;
    text-align: center;
    line-height: 60px;
  }
  
  .el-aside {
    background-color: #D3DCE6;
    color: #333;
    text-align: center;
    line-height: 200px;
  }
  
  .el-main {
    background-color: #E9EEF3;
    color: #333;
    text-align: center;
    line-height: 300px;
  }
  
  body > .el-container {
    margin-bottom: 40px;
  }
  
  .el-container:nth-child(5) .el-aside,
  .el-container:nth-child(6) .el-aside {
    line-height: 260px;
  }
  
  .el-container:nth-child(7) .el-aside {
    line-height: 320px;
  }
</style>
