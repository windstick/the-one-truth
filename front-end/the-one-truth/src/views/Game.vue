<template>
  <div class="Game">
    <el-container>
  <el-header>THE ONE TRUTH</el-header>
  <el-main>
    <el-row>
  <el-col :span="4"><div v-bind:class="{'grid-content bg-purple-dark':dark[0],'grid-content bg-purple':light[0]}">剧本环节</div></el-col>
  <el-col :span="4"><div v-bind:class="{'grid-content bg-purple-dark':dark[1],'grid-content bg-purple':light[1]}">介绍环节</div></el-col>
  <el-col :span="4"><div v-bind:class="{'grid-content bg-purple-dark':dark[2],'grid-content bg-purple':light[2]}">线索环节</div></el-col>
  <el-col :span="4"><div v-bind:class="{'grid-content bg-purple-dark':dark[3],'grid-content bg-purple':light[3]}">讨论环节</div></el-col>
  <el-col :span="4"><div v-bind:class="{'grid-content bg-purple-dark':dark[4],'grid-content bg-purple':light[4]}">投票环节</div></el-col>
  <el-col :span="4"><div v-bind:class="{'grid-content bg-purple-dark':dark[5],'grid-content bg-purple':light[5]}">真相环节</div></el-col>
</el-row>
<div v-if= "stage==4" class='grid-content bg-red'>
  <el-row>
    请选出你认为的凶手：
    <el-button  v-for= 'role in role_info' @click= 'selectedCriminal=role.role_id'>{{role.role_name}}</el-button>
  </el-row>
</div>
    <el-row>
      <el-col :span="8">
        <div class='grid-content bg-purple'>
          <el-radio v-model="scriptText" label="0">背景故事</el-radio>
          <el-radio v-model="scriptText" label="1">时间线</el-radio>
          <el-radio v-model="scriptText" label="2">任务</el-radio>
          <el-radio v-model="scriptText" label="3" v-if= 'stage==5'>真相</el-radio>
        </div>
        <div class='grid-content2 bg-purple'>
        <div  v-if= "scriptText==0">{{background}}</div>
        <div  v-if= "scriptText==1">{{timeline}}</div>
        <div  v-if= "scriptText==2">{{task}}</div>
        <div  v-if= "scriptText==3">凶手是：{{murder_name}}</div>
        </div>
      </el-col>
      <el-col :span="8">
        <div v-if= 'stage<=1' class='grid-content bg-purple' >
        </div>
        <div v-if= 'stage>1'> 
        <div class='grid-content bg-purple' >
        <el-radio v-for= 'role in role_info' v-model= 'selectedRole' v-bind:label= 'role.player_id_in_room'>{{role.role_name}}</el-radio>
        <el-button type='info' @click='searchClue()'>搜索| {{movementPoint}}/1</el-button>
        </div>
        <div v-for= 'clue in clue_info' class='grid-content2 bg-purple' v-if= "clue.role_id==role_info[selectedRole].role_id && clue.description==1" >{{clue.text}}</div>        
        </div>

      </el-col>
      <el-col :span="8">
          <div class='grid-content2 bg-purple' >
          <div v-for= 'msg in chat'>{{msg.name}}:{{msg.message}}</div>      
        </div>
            
                      <div class='grid-content bg-purple' >
                        <div>
          <el-input v-model="input" placeholder="请输入内容"></el-input>
                        </div>
                        <div>
          <el-button @click="mysend()"  type="plain">发送</el-button>
          </div>
            </div>

      </el-col>
    </el-row>
<el-footer>
<el-button @click="myready()"  type="primary">准备就绪</el-button>
</el-footer>
</el-main> 
</el-container> 
<el-button @click="gotest()"  type="primary">gotest</el-button>
<p>script_id:{{scriptid}},player:{{player}},room_id:{{room_id}}</p>
  </div>
</template>

<script>
export default {
  name: 'Game',
  data() {
    return {
      count: 0,
      stage: 0,
      player_id:1,
      dark:[1,0,0,0,0,0],
      light:[0,1,1,1,1,1],
      /* 以下是剧情文本相关的数据 */
      murderindex:0,
      scriptText:0,
      scriptid:1,
      player:1,
      room_id:0,
      script_title:'s',
      role_info:[{'1':1}],
      clue_info:[{'1':1}],
      murder_name:'',
      chat:'聊天内容',
      background: '这是背景故事\\n111111111111111111111111111111111111111111111111111111111111',
      timeline: '这是时间线。',
      task: '这是任务。',
      truth: '张三是凶手。',
      input:'',
      player_num:0,
      ready_player_num:0,
      /* 以下是线索相关的数据 */
      selectedRole:0,
      selectedCriminal:0,
      trueCriminal:-1,
      movementPoint:1,
      info:{},
      roles:[
        {id:0,name:'张三'},
        {id:1,name:'李四'},
        {id:2,name:'王五'},
      ],
      clues:[
        {id:0,text:'这是张三的线索,但不会告诉你谁是凶手',show:0},
        {id:1,text:'这是李四的线索，但不会告诉你谁是凶手',show:0},
        {id:2,text:'这是王五的线索，王五看见了张三行凶的过程，可推出张三是凶手',show:0},
      ]

    }
  },
  watch:{
    stage(curval,oldval){
      if(curval==5){
         if(this.selectedCriminal==this.trueCriminal){
           alert('恭喜你找出了凶手,游戏获胜！')
         }
         else{
           alert('没有找对凶手，游戏失败！')
         }
       }
       if(curval==0){
         this.movementPoint=1;
         for(let i=0;i<3;++i){
           this.clues[i].show=0;
         }
       }
    },
  },
  methods:{
    myready:function(){
       /*
       this.axios({
        method: 'post',
        url: '/synchronize/',
        data:{
 
        room_id:this.room_id,
        player_id:1
       
        }
      })
      .then(response => (
        //console.log(response.data),
        this.player_num=response.data.data.player_num,
        this.ready_player_num=response.data.data.ready_player_num
        ));
      */
       this.count=this.count+1;
       //if(this.player_num==this.ready_player_num){
       if(this.count>0){
         this.count=0;
         this.light[this.stage]=1;
         this.dark[this.stage]=0;
         this.stage=this.stage+1;
         this.light[this.stage]=0;
         this.dark[this.stage]=1;
       }
       if(this.stage==6)this.stage=0;
    },
    searchClue:function(){
      if(this.movementPoint>0 && this.stage==2 && this.clue_info[this.selectedRole].description!=1){
      this.clue_info[this.selectedRole].description=1;
      this.movementPoint--;
      }
    },
    gotest:function(){
      this.$router.push({name:'test',params:{mytimeline:this.timeline,mytask:this.task}})
    },
    mysend:function(){
      this.axios({
        method: 'post',
        url: '/send_message/',
        data:{
          room_id:this.room_id,
          player_id:this.role_info[this.player].player_id,
          message:this.input
        }
      })
      .then(response => (
        console.log(response.data),
        this.chat=response.data.data,
        this.input=''
        ));
    }
  },
  mounted () {
    /* this.$axios
      .get('/site/info.json')
      .then(response => (this.task = response))
      .catch(function (error) { // 请求失败处理
        console.log(error);
      });
      */
    this.scriptid=this.$route.query.script_id
    this.player=this.$route.query.player
    this.room_id=this.$route.query.room_id
    console.log("current player " + this.player)

    /*
    this.axios({
        method: 'post',
        url: '/room_owner_choose_script/',
        data:{
          //username:'u2',
          room_id:1,
          script_title:'a_test_script_title'
          //is_master:0
          //password:'123456',
          //group_id:1,
          //email:"54321@pku.edu.cn"
          //num_person:2
       
        }
      })
      .then(response => (
        console.log(response.data)
        
        this.role_info=response.data.role_info,
        this.clue_info=response.data.clue_info,
        this.trueCriminal=response.data.murder_id,
        this.script_title=response.data.script_title
      
        )); 
    */

    this.axios({
        method: 'post',
        url: '/start_game/',
        data:{
          room_id:this.room_id,
        }
      })
      .then(response => {
        console.log(response.data.data.role_info[0]),
        this.role_info=response.data.data.role_info,
        this.clue_info=response.data.data['clue_info'],
        this.trueCriminal=response.data.data.murder.role_id,
        this.murder_name=response.data.data.murder.role_name,
        this.script_title=response.data.data.script_title,
        this.background=response.data.data.role_info[this.player].background,
        // console.log(this.role_info),
        // console.log(this.clue_info),
        // console.log(this.trueCriminal),
        this.timeline=response.data.data.role_info[this.player].timeline,
        this.task=response.data.data.role_info[this.player].task

        console.log(this.background)
        }
      );
      // console.log(1)


      
  },
  created(){
      // console.log(this.$route.query)
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
    word-wrap: break-word;
    word-break: normal;
  }
  .grid-content2 {
    margin-top: 10px;
    border-radius: 2px;
    min-height: 300px;
    min-height: 300px;
    line-height: 30px;
    overflow-y: scroll;
    overflow-x: hidden;
    text-align: left;
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

