<template>
  <div class="wave">
    <el-container>
  <el-header>语音识别</el-header>
  <el-main>
      <el-row class='grid-content2'>
      <audio  id= 'wid' v-bind:src= 'fname' controls>
您的浏览器不支持 audio 元素。
</audio>
<!--
<el-button @click= "myplay()" type= "primary" >获得音频</el-button>
-->
</el-row>
<div class='grid-content bg-purple'>
          <el-radio v-model="pngtype" label="0">WAV</el-radio>
          <el-radio v-model="pngtype" label="1">SPEC</el-radio>
          <el-radio v-model="pngtype" label="2">CQT</el-radio>
          <el-radio v-model="pngtype" label="3">MFCC</el-radio>
          <el-radio v-model="pngtype" label="4">MFCCS</el-radio>
  </div>
<img v-bind:src= 'waveapi'  v-if= "pngtype==0" />
<img v-bind:src= 'specapi'  v-if= "pngtype==1" />
<img v-bind:src= 'CQTapi'  v-if= "pngtype==2" />
<img v-bind:src= 'mfccapi'  v-if= "pngtype==3" />
<img v-bind:src= 'mfccsapi'  v-if= "pngtype==4" />
  </el-main>
  <el-footer>
  <el-button @click="goback()"  type="primary">返回主界面</el-button>
  </el-footer>
    </el-container>
  </div>    
</template>

<script>
export default {
    name:"wave",
    data(){
        return{
            fname:'http://127.0.0.1:5000/api/download',
            fname2:'http://127.0.0.1:5000/api/download2',
            waveapi:'http://127.0.0.1:5000/api/plotwave',
            specapi:'http://127.0.0.1:5000/api/plotspec',
            CQTapi:'http://127.0.0.1:5000/api/plotCQT',
            mfccapi:'http://127.0.0.1:5000/api/plotmfcc',
            mfccsapi:'http://127.0.0.1:5000/api/plotmfccs',
            mytime:'',
            pngtype:1
        } 
    },
    methods:{
        myplay:function(){
            /*
            let mywav=document.getElementById("wid")
            mywav.src=this.fname2
            mywav.load()
            mywav.play()
            */
           let getTimestamp = new  Date().getTime();
           this.fname=this.fname + "?timestamp=" + getTimestamp
           const audio=document.createElement("audio");
           audio.src=this.fname;
           audio.load();
           this.$forceUpdate();
           //audio.play();
        },
        goback:function(){

      this.$router.push({name:'main'})
    },
    },
    mounted(){
         this.mytime=new  Date().getTime();
         
         this.fname=this.fname + "?timestamp=" + this.mytime
         this.waveapi=this.waveapi + "?timestamp=" + this.mytime
         this.specapi=this.specapi + "?timestamp=" + this.mytime
         this.CQTapi=this.CQTapi + "?timestamp=" + this.mytime
         this.mfccapi=this.mfccapi + "?timestamp=" + this.mytime
         this.mfccsapi=this.mfccsapi + "?timestamp=" + this.mytime
            let mywav=document.getElementById("wid")
            mywav.src=this.fname
            mywav.load()
         
    }
}

</script>

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
    border-radius: 0px;
    min-height: 0px;
    line-height: 0px;
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

