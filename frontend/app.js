const API_URL = 'http://localhost:8000/api/v1';
let token = localStorage.getItem('token');

function showMessage(msg, type) {
    const div = document.createElement('div');
    div.id = 'message';
    div.className = type;
    div.textContent = msg;
    document.body.appendChild(div);
    setTimeout(() => div.remove(), 3000);
}

function showLogin() {
    document.getElementById('login-form').classList.remove('hidden');
    document.getElementById('register-form').classList.add('hidden');
    document.querySelectorAll('.tab-btn').forEach((btn, i) => btn.classList.toggle('active', i === 0));
}

function showRegister() {
    document.getElementById('login-form').classList.add('hidden');
    document.getElementById('register-form').classList.remove('hidden');
    document.querySelectorAll('.tab-btn').forEach((btn, i) => btn.classList.toggle('active', i === 1));
}

async function handleLogin(e) {
    e.preventDefault();
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    try {
        const res = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        if (!res.ok) throw await res.json();
        const data = await res.json();
        token = data.access_token;
        localStorage.setItem('token', token);
        document.getElementById('auth-section').classList.add('hidden');
        document.getElementById('dashboard').classList.remove('hidden');
        loadDashboard();
    } catch (err) {
        showMessage(err.detail || 'Login failed', 'error');
    }
}

async function handleRegister(e) {
    e.preventDefault();
    const full_name = document.getElementById('reg-name').value;
    const email = document.getElementById('reg-email').value;
    const password = document.getElementById('reg-password').value;
    try {
        const res = await fetch(`${API_URL}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password, full_name })
        });
        if (!res.ok) throw await res.json();
        showMessage('Registration successful! Please login.', 'success');
        showLogin();
    } catch (err) {
        showMessage(err.detail || 'Registration failed', 'error');
    }
}

function logout() {
    token = null;
    localStorage.removeItem('token');
    document.getElementById('dashboard').classList.add('hidden');
    document.getElementById('auth-section').classList.remove('hidden');
    showLogin();
}

async function loadDashboard() {
    const headers = { 'Authorization': `Bearer ${token}` };
    try {
        const [meRes, itemsRes, opsRes] = await Promise.all([
            fetch(`${API_URL}/auth/me`, { headers }),
            fetch(`${API_URL}/inventory/?limit=100`, { headers }),
            fetch(`${API_URL}/operations/?limit=10`, { headers })
        ]);
        const user = await meRes.json();
        const items = await itemsRes.json();
        const ops = await opsRes.json();
        document.getElementById('user-email').textContent = user.email;
        document.getElementById('user-info').classList.remove('hidden');
        document.getElementById('stat-total').textContent = items.length;
        document.getElementById('stat-qty').textContent = items.reduce((s, i) => s + i.quantity, 0);
        document.getElementById('stat-ops').textContent = ops.length;
        renderItems(items);
        renderOperations(ops);
    } catch (err) {
        showMessage('Failed to load dashboard', 'error');
    }
}

function renderItems(items) {
    const grid = document.getElementById('inventory-list');
    if (!items.length) {
        grid.innerHTML = '<p>No items found.</p>';
        return;
    }
    grid.innerHTML = items.map(item => `
        <div class="inventory-card">
            <h4>${item.name}</h4>
            <p class="sku">SKU: ${item.sku}</p>
            <div class="details">
                <span>Qty: ${item.quantity}</span>
                <span>Loc: ${item.location || '-'}</span>
                <span>RFID: ${item.rfid_tag || '-'}</span>
            </div>
            <p>${item.description || ''}</p>
            <div class="actions">
                <button class="btn btn-primary" onclick="editItem('${item.id}')">Edit</button>
                <button class="btn btn-secondary" onclick="deleteItem('${item.id}')">Delete</button>
            </div>
        </div>
    `).join('');
}

function renderOperations(ops) {
    const list = document.getElementById('operations-list');
    list.innerHTML = ops.map(op => `
        <div class="operation-item">
            <span class="op-type ${op.type}">${op.type}</span>
            Item: ${op.item_id.slice(0,8)}... | Qty: ${op.quantity_change > 0 ? '+' : ''}${op.quantity_change}
            <br><small>${new Date(op.created_at).toLocaleString()}</small>
        </div>
    `).join('');
}

function showAddItemForm() {
    document.getElementById('add-item-modal').classList.remove('hidden');
}

function closeModal() {
    document.getElementById('add-item-modal').classList.add('hidden');
}

async function handleAddItem(e) {
    e.preventDefault();
    const data = {
        sku: document.getElementById('item-sku').value,
        name: document.getElementById('item-name').value,
        description: document.getElementById('item-desc').value,
        quantity: parseInt(document.getElementById('item-qty').value),
        location: document.getElementById('item-location').value,
        rfid_tag: document.getElementById('item-rfid').value
    };
    try {
        const res = await fetch(`${API_URL}/inventory/`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if (!res.ok) throw await res.json();
        closeModal();
        loadDashboard();
        showMessage('Item added!', 'success');
    } catch (err) {
        showMessage(err.detail || 'Failed to add item', 'error');
    }
}

let editingItemId = null;

async function editItem(id) {
    const headers = { 'Authorization': `Bearer ${token}` };
    const res = await fetch(`${API_URL}/inventory/${id}`, { headers });
    if (!res.ok) return showMessage('Failed to load item', 'error');
    const item = await res.json();
    editingItemId = id;
    document.getElementById('edit-item-id').value = id;
    document.getElementById('edit-name').value = item.name;
    document.getElementById('edit-desc').value = item.description || '';
    document.getElementById('edit-qty').value = item.quantity;
    document.getElementById('edit-location').value = item.location || '';
    document.getElementById('edit-rfid').value = item.rfid_tag || '';
    document.getElementById('edit-item-modal').classList.remove('hidden');
}

function closeEditModal() {
    document.getElementById('edit-item-modal').classList.add('hidden');
    editingItemId = null;
}

async function handleEditItem(e) {
    e.preventDefault();
    const data = {
        name: document.getElementById('edit-name').value,
        description: document.getElementById('edit-desc').value,
        quantity: parseInt(document.getElementById('edit-qty').value),
        location: document.getElementById('edit-location').value,
        rfid_tag: document.getElementById('edit-rfid').value
    };
    try {
        const res = await fetch(`${API_URL}/inventory/${editingItemId}`, {
            method: 'PUT',
            headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if (!res.ok) throw await res.json();
        closeEditModal();
        loadDashboard();
        showMessage('Item updated!', 'success');
    } catch (err) {
        showMessage(err.detail || 'Failed to update item', 'error');
    }
}

async function deleteItem(id) {
    if (!confirm('Delete this item?')) return;
    try {
        const res = await fetch(`${API_URL}/inventory/${id}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!res.ok) throw await res.json();
        loadDashboard();
        showMessage('Item deleted', 'success');
    } catch (err) {
        showMessage(err.detail || 'Failed to delete', 'error');
    }
}

function searchItems() {
    // Basic filter - in production would call API with query params
}

if (token) {
    document.getElementById('auth-section').classList.add('hidden');
    document.getElementById('dashboard').classList.remove('hidden');
    loadDashboard();
} else {
    showLogin();
}