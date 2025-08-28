// const word = "jummy"
// alert("welcome"+ " " + word);


      
      // document.getElementById('submitbtn').addEventListener('click',function(){
      //       let board = document.getElementById('username').value; 
      //       console.log(board);
      // })
      //   alert("Wlcome" + " " + board)
  //  function handlelogin(event) {
  //   event.preventDefault();


  //   //Object(HTMLInputElement)
  //  }

  //  handlelogin(event)

  const button = document.querySelector('#submitbtn');
  const input = document.querySelector('#username');
//   button.addEventListener('click', (e) =>{
//       const my = alert('welcome')
//      my.textContent = input.value;

//   })
 

  button.addEventListener('click', () =>{
    const output = document.createElement('li');
    output.textContent = input.value.trim();
    
    const result = `welcome ${output}, to my website`;
    alert(result)

  })

  function updateBalance() {
    // Get the balance element
    let balanceElement = document.getElementById("balance");

    // Get current balance as a number
    let currentBalance = parseFloat(balanceElement.innerText.replace(/,/g, ''));

    // Add ₦500
    let newBalance = currentBalance + 500;

    // Format with commas and .00
    let formattedBalance = newBalance.toLocaleString('en-NG', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });

    // Update the HTML
    balanceElement.innerText = formattedBalance;
}

// Example: call this after a referral
updateBalance();
