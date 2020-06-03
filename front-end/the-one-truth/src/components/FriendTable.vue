<template>
  <el-table :data="friend_list" style="width: 100%; padding-top: 15px;">
    <el-table-column label="好友名称" min-width="200" prop="name"/>
      <!---template slot-scope="scope">
        {{ scope.row.order_no | orderNoFilter }}
      </template>
    </el-table-column--->
  </el-table>
</template>

<script>

export default {
  props: {
    friend_list: {
      type: Array,
      default(){
        return []
      }
    }
  }
}
</script>
