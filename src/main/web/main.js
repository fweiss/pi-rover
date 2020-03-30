$(function() {
    $('#joystick').joystick({
        moveEvent: function(pos) { console.log('throttle:' + pos.y) },
        endEvent: function(pos) { console.log('throttle:' + pos.y) }
    });
    $('#joystick').joystick('value', 0.5, 0);

})