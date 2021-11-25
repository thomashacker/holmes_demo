

console.debug("TEST");
var element = document.getElementById("test")
console.debug(element)

var all = document.getElementsByTagName("*");

for (var i=0, max=all.length; i < max; i++) {
    console.debug(all[i])
}
