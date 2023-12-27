const wrapper = document.querySelector('.wrapper');
const loginLink = document.querySelector('.login-link');
const registerLink = document.querySelector('.register-link');
const btnLoginPopup = document.querySelector('.btnLogin-popup');
const btnLogoutPopup = document.querySelector('.btnLogout-popup');
const iconClose = document.querySelector('.icon-close');
const background = document.querySelector('.background');

registerLink.addEventListener('click', () => {
    wrapper.classList.add('active');
});

loginLink.addEventListener('click', () => {
    wrapper.classList.remove('active');
});

try{
    btnLoginPopup.addEventListener('click', () => {
        wrapper.classList.add('active-popup');
        background.classList.add('active');
    });
}
catch(err){
    console.log(err);
}

try{
    btnLogoutPopup.addEventListener('click', () => {
        wrapper.classList.add('active-popup');
        wrapper.classList.add('logout');
        background.classList.add('active');
    });
}
catch(err){
    console.log(err);
}

iconClose.addEventListener('click', () => {
    wrapper.classList.remove('active-popup');
    background.classList.remove('active');
});

background.addEventListener('click', () => {
    wrapper.classList.remove('active-popup');
    background.classList.remove('active');
});
