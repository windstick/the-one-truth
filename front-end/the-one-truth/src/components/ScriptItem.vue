<template>
  <div id="item">
    <div id="nameAndFig" style="margin: 10px">
      <slot name="fig" id="fig">这是一张图片</slot>
      <span style="margin: 0 10px">
      <slot name="scriptName">这是一个剧本名称</slot>
      </span>
    </div>
    <slot id="intro" name="intro">这里是剧本简介</slot>
  </div>
</template>

<script>
export default {
  name: 'scriptItem',
  components: {
  },
}
</script>

<style>
  #item {
    background-color: rgba(249, 204, 157, 0.5);
    margin: 10px;
    border-style: dashed;
    border-width: 5px;
  }

  #nameAndFig{
    display: flex;
    text-align: center;
  }
  #fig{
    flex: 0;
    height: 50px;
  }



</style>