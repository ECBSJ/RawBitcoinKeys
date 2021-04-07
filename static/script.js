const binaryinput = document.getElementById('input-field')
const form = document.getElementById('form')
const errorElement = document.getElementById('error')

form.addEventListener('submit', (e) => {
    let messages = []
    if (binaryinput.value.length != 256 || binaryinput.value.includes(2) || binaryinput.value.includes(3) || binaryinput.value.includes(4) || binaryinput.value.includes(5) || binaryinput.value.includes(6) || binaryinput.value.includes(7) || binaryinput.value.includes(8) || binaryinput.value.includes(9)) {
        messages.push('The length of the input must be exactly 256 binary (only using digits 1 & 0) digits long')
    }

    // if (binaryinput.value.includes(2,3,4,5,6,7,8,9)) {
    //     messages.push('Your input can only contain binary digits which are 1 and/or 0')
    // }

    if (messages.length > 0) {
        e.preventDefault()
        errorElement.innerText = messages.join(', ')
    }
})