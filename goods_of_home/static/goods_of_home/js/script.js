// suppose the `id` attribute of element is `message_container`.
var message_ele = document.getElementById("message_container");

setTimeout(function(){
   message_ele.classList.toggle('visibility');
}, 3000);
// Timeout is 3 sec, you can change it