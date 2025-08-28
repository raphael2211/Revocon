// =============== SIGNUP SCRIPT ===============
document.getElementById("joinnow").addEventListener("click", function () {
    let username = document.getElementById("username").value.trim();
    let email = document.getElementById("signup-email").value.trim();
    let password = document.getElementById("password").value.trim();
    let token = document.getElementById("token").value.trim();

    if (!username || !email || !password || !token) {
        alert("Please fill in all fields");
        return;
    }

    // Send signup data to backend
    fetch("signup.php", { // <-- Change to your backend signup file
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            username: username,
            email: email,
            password: password,
            token: token
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            window.location.href = "home.html"; // Redirect to site
        } else {
            let tokenField = document.getElementById("TOKEN_INPUT_ID");
            tokenField.style.color = "red";
            alert("Wrong token");
        }
    })
    .catch(err => console.error(err));
});


// =============== REFERRAL SCRIPT ===============
function updateReferral(referrerUsername) {
    fetch("updateReferral.php", { // <-- Change to your backend file
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ referrer: referrerUsername })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            console.log("Referral credited!");
        }
    })
    .catch(err => console.error(err));
}

// Detect ?ref=username in URL
let params = new URLSearchParams(window.location.search);
let ref = params.get("ref");
if (ref) {
    // You can store this temporarily until signup is complete
    localStorage.setItem("referrer", ref);
}

// After successful signup, credit referral
// (Run this in the signup success part)
let storedReferrer = localStorage.getItem("referrer");
if (storedReferrer) {
    updateReferral(storedReferrer);
    localStorage.removeItem("referrer");
}


// =============== WITHDRAWAL SCRIPT ===============
document.getElementById("withbtn").addEventListener("click", function () {
    let accountNumber = document.getElementById("account-number").value.trim();
    let accountName = document.getElementById("account-name").value.trim();
    let amount = parseFloat(document.getElementById("amount").value);
    let bank = document.getElementById("bank-name").value.trim();

    if (!accountNumber || !accountName || !amount || !bank) {
        alert("Please fill in all fields");
        return;
    }

    let date = new Date().toLocaleString();

    fetch("withdraw.php", { // <-- Change to your backend file
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            accountNumber: accountNumber,
            accountName: accountName,
            amount: amount,
            bank: bank,
            date: date
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            alert("Withdrawal request sent!");
            // Add to transaction history (Pending)
            let historyTable = document.getElementById("TRANSACTION_HISTORY_TABLE_ID");
            let row = historyTable.insertRow();
            row.innerHTML = `<td>${date}</td><td>₦${amount.toLocaleString()}</td><td>Pending</td>`;
        }
    })
    .catch(err => console.error(err));
});
