const msg = document.querySelector('.msg');

if (!msg) { }
else {
    setInterval(() => { msg.classList.add('hidden') }, 3000)
}
