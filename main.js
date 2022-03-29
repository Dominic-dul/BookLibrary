const myForm = document.querySelector('#my-form');
let bookNameInput = document.querySelector('#bookName');
let bookAuthorInput = document.querySelector('#bookAuthor');
let bookYearInput = document.querySelector('#bookYear');
const msg = document.querySelector('.msg');

myForm.addEventListener('submit', onSubmit);

function onSubmit(e) {
    e.preventDefault();
    if (bookNameInput.value === '' || bookAuthorInput.value === '' || bookYearInput.value === '') {
        msg.classList.add('error');
        msg.innerHTML = 'Please enter all fields';

        setTimeout(() => msg.remove(), 2000);
    } else {
        let table = document.querySelector('#fl-table');

        console.log(table);

        let row = table.insertRow(-1);
        let name = row.insertCell(0);
        let author = row.insertCell(1);
        let date = row.insertCell(2);

        name.innerHTML = bookNameInput.value;
        author.innerHTML = bookAuthorInput.value;
        date.innerHTML = bookYearInput.value;
    }
}