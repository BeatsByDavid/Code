import openSocket from 'socket.io-client';

console.log('Starting socket io client!');

var namespace = '/namespace';

var socket = openSocket('http://davidkopala.com:8000' + namespace);
socket.on('connect', () => {
    console.log("Socket Connected!");
    socket.emit('join_room');
});
socket.on('event', (data) => {
    console.log("Socket received: ", data);
});
socket.on('new_data', (data) => {
    console.log("Socket 'new_data' event!");
    console.log(data);
})