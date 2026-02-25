async function loadOrders() {
  const res = await fetch("/api/orders");
  const data = await res.json();
  const tbody = document.getElementById("orders-body");
  tbody.innerHTML = "";
  data.orders.forEach(o => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${o.customer}</td>
      <td>${o.item}</td>
      <td>${o.quantity}</td>
      <td>${o.price.toFixed(2)}</td>
      <td>${o.status}</td>
      <td>${new Date(o.created_at).toLocaleString()}</td>
      <td><button class="del-btn" data-id="${o.id}">Delete</button></td>
    `;
    tbody.appendChild(tr);
  });
  tbody.querySelectorAll(".del-btn").forEach(btn => {
    btn.addEventListener("click", () => deleteOrder(btn.dataset.id));
  });
}

async function deleteOrder(id) {
  await fetch(`/api/orders/${id}`, { method: "DELETE" });
  await loadOrders();
}

document.getElementById("order-form").addEventListener("submit", async e => {
  e.preventDefault();
  const errEl = document.getElementById("error-msg");
  errEl.textContent = "";
  const body = {
    customer: document.getElementById("customer").value,
    item: document.getElementById("item").value,
    quantity: parseInt(document.getElementById("quantity").value, 10),
    price: parseFloat(document.getElementById("price").value),
  };
  const res = await fetch("/api/orders", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const err = await res.json();
    errEl.textContent = err.error || "Failed to create order.";
    return;
  }
  e.target.reset();
  await loadOrders();
});

loadOrders();
