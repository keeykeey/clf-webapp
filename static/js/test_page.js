const button = document.querySelector('.button');
button.addEventListener('mouseover',()=>{
    textFromForm = getTextFromForm();
    writeOver();
    
    console.log(textFromForm);
});    


function writeOver(){
    const stdout = document.querySelector('.text_out');
    textFromForm = getTextFromForm();
    stdout.innerHTML = textFromForm;
}

function getTextFromForm(){
    const textFromForm = document.getElementById('text_input1').value;
    return textFromForm;
}

    


