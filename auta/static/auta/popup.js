const wrapper = document.querySelector('.wrapper');
const loginLink = document.querySelector('.login-link');
const registerLink = document.querySelector('.register-link');
const btnLoginPopup = document.querySelectorAll('.btn-popup.login');
const btnLogoutPopup = document.querySelectorAll('.btn-popup.logout');
const iconClose = document.querySelector('.icon-close');
const background = document.querySelector('.background');
const toggleBtn = document.querySelector('.toggle_btn');
const toggleBtnIcon = document.querySelector('.toggle_btn i');
const dropdownMenu = document.querySelector('.dropdown_menu');

registerLink.addEventListener('click', () => {
    wrapper.classList.add('register');
    wrapper.classList.remove('login');
});

loginLink.addEventListener('click', () => {
    wrapper.classList.remove('register');
    wrapper.classList.add('login');
});

try{
    btnLoginPopup.forEach((button) => {
        button.addEventListener('click', () => {
            wrapper.classList.add('active-popup');
            wrapper.classList.add('login');
            wrapper.classList.remove('register');
            background.classList.add('active');
            dropdownMenu.classList.remove('open');
            const isOpen = dropdownMenu.classList.contains('open');

            toggleBtnIcon.classList = isOpen ? 'fas fa-xmark' : 'fas fa-bars';
        });
    });
}
catch(err){
    console.log(err);
}

try{
    btnLogoutPopup.forEach((button) => {
        button.addEventListener('click', () => {
            wrapper.classList.add('active-popup');
            wrapper.classList.add('logout');
            background.classList.add('active');
            dropdownMenu.classList.remove('open');
            const isOpen = dropdownMenu.classList.contains('open');

            toggleBtnIcon.classList = isOpen ? 'fas fa-xmark' : 'fas fa-bars';
        });
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
    dropdownMenu.classList.remove('open');
    const isOpen = dropdownMenu.classList.contains('open');

    toggleBtnIcon.classList = isOpen ? 'fas fa-xmark' : 'fas fa-bars';
});

toggleBtn.addEventListener('click', () => {
    dropdownMenu.classList.toggle('open');
    const isOpen = dropdownMenu.classList.contains('open');

    toggleBtnIcon.classList = isOpen ? 'fas fa-xmark' : 'fas fa-bars';
    background.classList.toggle('active');
});