<template>
  <router-view />
</template>

<style>
* {
  margin: 0;
  padding: 0;
  font-family: Arial, sans-serif;
  box-sizing: border-box;
}

html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
  background-color: #4a7ab7; /* 배경색 */
  /* overflow: hidden; 는 제거 */
}
body {
  /* 굳이 flex 안 써도 가로 중앙정렬 가능 */
  display: block;
}
</style>
