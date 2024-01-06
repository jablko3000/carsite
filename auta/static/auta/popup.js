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
const nameEdit = document.querySelector('.name-edit');
const emailEdit = document.querySelector('.email-edit');
const passwordEdit = document.querySelector('.password-edit');
const phoneEdit = document.querySelector('.phone-edit');

if (registerLink) {
    registerLink.addEventListener('click', () => {
        wrapper.classList.add('register');
        wrapper.classList.remove('login');
    });
}

if (loginLink) {
    loginLink.addEventListener('click', () => {
        wrapper.classList.remove('register');
        wrapper.classList.add('login');
    });
}

if (btnLoginPopup) {
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

if (btnLogoutPopup) {
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

if (iconClose) {
    iconClose.addEventListener('click', () => {
        wrapper.classList.remove('active-popup');
        wrapper.classList.remove('edit');
        wrapper.classList.remove('name');
        wrapper.classList.remove('email');
        wrapper.classList.remove('password');
        wrapper.classList.remove('phone');
        background.classList.remove('active');
    });
}

if (background) {
    background.addEventListener('click', () => {
        wrapper.classList.remove('active-popup');
        wrapper.classList.remove('edit');
        wrapper.classList.remove('name');
        wrapper.classList.remove('email');
        wrapper.classList.remove('password');
        wrapper.classList.remove('phone');
        background.classList.remove('active');
        dropdownMenu.classList.remove('open');
        const isOpen = dropdownMenu.classList.contains('open');

        toggleBtnIcon.classList = isOpen ? 'fas fa-xmark' : 'fas fa-bars';
    });
}

if (toggleBtn) {
    toggleBtn.addEventListener('click', () => {
        dropdownMenu.classList.toggle('open');
        const isOpen = dropdownMenu.classList.contains('open');

        toggleBtnIcon.classList = isOpen ? 'fas fa-xmark' : 'fas fa-bars';
        background.classList.toggle('active');
    });
}

if (nameEdit){
    nameEdit.addEventListener('click', () => {
        wrapper.classList.add('active-popup');
        wrapper.classList.add('edit');
        wrapper.classList.add('name');
        background.classList.add('active');
    });
}

if (emailEdit){
    emailEdit.addEventListener('click', () => {
        wrapper.classList.add('active-popup');
        wrapper.classList.add('edit');
        wrapper.classList.add('email');
        background.classList.add('active');
    });
}

if (passwordEdit){
    passwordEdit.addEventListener('click', () => {
        wrapper.classList.add('active-popup');
        wrapper.classList.add('edit');
        wrapper.classList.add('password');
        background.classList.add('active');
    });
}

if (phoneEdit){
    phoneEdit.addEventListener('click', () => {
        wrapper.classList.add('active-popup');
        wrapper.classList.add('edit');
        wrapper.classList.add('phone');
        background.classList.add('active');
    });
}