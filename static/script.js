let lastSubmittedTime = null;   
let timerInterval = null;       


async function loadPayments() {
    const res = await fetch('/payments');
    let data = await res.json();

    const sortType = document.getElementById('sortSelect')?.value;

    if (sortType === "timestamp_desc") {
        data.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
    }
    else if (sortType === "timestamp_asc") {
        data.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
    }
    else if (sortType === "amount_desc") {
        data.sort((a, b) => b.amount - a.amount);
    }
    else if (sortType === "amount_asc") {
        data.sort((a, b) => a.amount - b.amount);
    }
    else if (sortType === "memo_asc") {
        data.sort((a, b) => a.memo.localeCompare(b.memo));
    }
    else if (sortType === "memo_desc") {
        data.sort((a, b) => b.memo.localeCompare(a.memo));
    }

    const container = document.getElementById('transactions');
    container.innerHTML = '';

    data.forEach(p => {
        const div = document.createElement('div');

        div.innerHTML = `
            <div><strong>Id:</strong> ${p.transactionId}</div>
            <div><strong>Memo:</strong> ${p.memo}</div>
            <div><strong>Amount:</strong> $${p.amount}</div>
            <div><strong>Status:</strong> ${p.status}</div>
            <div><strong>Timestamp:</strong> ${p.timestamp}</div>
        `;

        container.appendChild(div);
    });
}


async function submitPayment() {
    const amount = document.getElementById('amountInput').value;
    const memo = document.getElementById('memoInput').value;

    const formData = new FormData();
    formData.append("amount", amount);
    formData.append("memo", memo);

    await fetch('/payments', {
        method: 'POST',
        body: formData
    });

    lastSubmittedTime = Date.now();
    startLastSubmittedTimer();

    loadPayments(); // refresh transaction list
}

function startLastSubmittedTimer() {
    const label = document.getElementById("lastSubmitted");

    // clear old interval if it exists
    if (timerInterval) clearInterval(timerInterval);

    timerInterval = setInterval(() => {
        if (!lastSubmittedTime) return;

        const diffSeconds = Math.floor((Date.now() - lastSubmittedTime) / 1000);
        label.textContent = `Last payment was submitted ${diffSeconds} seconds ago`;
    }, 1000);  // update every second
}


loadPayments();
