import os

css_code = """
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

:root {
  --primary: #133926;
  --primary-light: #1d5337;
  --accent: #2ec4b6;
  --gold: #e9c46a;
  --bg-canvas: #f6f9f6;
  --card-bg: #ffffff;
  --text-dark: #1a202c;
  --text-muted: #718096;
  --radius: 16px;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: 'Plus Jakarta Sans', sans-serif;
  background-color: var(--bg-canvas);
  color: var(--text-dark);
}

.navbar {
  background: linear-gradient(135deg, #0d281a, #1b4332) !important;
  box-shadow: 0 8px 30px rgba(13,40,26,0.15);
  padding: 14px 0;
}

.navbar-brand { font-weight: 800; font-size: 1.4rem; }

.nav-link {
  font-weight: 500;
  padding: 8px 16px !important;
  border-radius: 10px;
  transition: all .2s;
}

.nav-link:hover {
  background: rgba(255,255,255,0.08);
  color: #fff !important;
}

.hero-banner {
  background: radial-gradient(circle at 10% 20%, #1b4332 0%, #0d281a 90%);
  color: #fff;
  border-radius: 24px;
  padding: 70px 45px;
  box-shadow: 0 20px 40px rgba(13,40,26,0.2);
}

.card {
  background: var(--card-bg);
  border-radius: var(--radius);
  border: 1px solid rgba(0,0,0,0.06);
  box-shadow: 0 6px 20px rgba(0,0,0,0.03);
  transition: all .3s ease;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 18px 35px rgba(19,57,38,0.1);
}

.btn-cafe {
  background: linear-gradient(135deg, #2ec4b6, #208b81);
  color: #fff;
  font-weight: 600;
  border: none;
  border-radius: 12px;
  padding: 10px 22px;
  transition: all .25s;
}

.btn-cafe:hover {
  background: linear-gradient(135deg, #208b81, #16635c);
  color: #fff;
}

.stat-card {
  background: #fff;
  border-radius: 20px;
  padding: 24px;
  border: 1px solid rgba(0,0,0,0.05);
  box-shadow: 0 10px 25px rgba(0,0,0,0.02);
  display: flex;
  align-items: center;
  gap: 20px;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
}

.table-custom { border-collapse: separate; border-spacing: 0 10px; }
.table-custom tbody tr {
  background: #fff;
  box-shadow: 0 2px 10px rgba(0,0,0,0.02);
  border-radius: 12px;
}
"""

dashboard_html = """{% extends "base.html" %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
  <div>
    <h2 class="fw-bold text-success mb-1">Cafe Executive Admin Dashboard</h2>
    <p class="text-muted mb-0">Real-time insights, live kitchen status aur sales monitoring.</p>
  </div>
  <div class="d-flex gap-2">
    <a href="/admin/" class="btn btn-outline-secondary btn-sm">Database Master Admin</a>
    <a href="{% url 'home' %}" class="btn btn-cafe btn-sm">Public Website</a>
  </div>
</div>

<div class="row g-3 mb-4">
  <div class="col-md-3">
    <div class="stat-card">
      <div class="stat-icon bg-success-subtle text-success"><i class="bi bi-bag-check-fill"></i></div>
      <div>
        <div class="text-muted small fw-semibold">TOTAL ORDERS</div>
        <h3 class="fw-bold mb-0">{{ total_orders }}</h3>
      </div>
    </div>
  </div>
  <div class="col-md-3">
    <div class="stat-card">
      <div class="stat-icon bg-warning-subtle text-warning"><i class="bi bi-clock-history"></i></div>
      <div>
        <div class="text-muted small fw-semibold">PENDING ORDERS</div>
        <h3 class="fw-bold mb-0">{{ pending_orders }}</h3>
      </div>
    </div>
  </div>
  <div class="col-md-3">
    <div class="stat-card">
      <div class="stat-icon bg-info-subtle text-info"><i class="bi bi-currency-rupee"></i></div>
      <div>
        <div class="text-muted small fw-semibold">TOTAL SALES</div>
        <h3 class="fw-bold mb-0">₹{{ total_sales }}</h3>
      </div>
    </div>
  </div>
  <div class="col-md-3">
    <div class="stat-card">
      <div class="stat-icon bg-primary-subtle text-primary"><i class="bi bi-qr-code-scan"></i></div>
      <div>
        <div class="text-muted small fw-semibold">ACTIVE TABLES</div>
        <h3 class="fw-bold mb-0">{{ total_tables }}</h3>
      </div>
    </div>
  </div>
</div>

<div class="row g-4">
  <div class="col-lg-8">
    <div class="card p-4 border-0">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h5 class="fw-bold mb-0">Recent Customer Orders</h5>
        <a href="/admin/orders/order/" class="btn btn-sm btn-outline-success">Manage All Orders</a>
      </div>
      <div class="table-responsive">
        <table class="table table-custom align-middle">
          <thead>
            <tr>
              <th>Order ID</th>
              <th>Customer</th>
              <th>Type</th>
              <th>Total</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {% for o in recent_orders %}
            <tr>
              <td class="fw-bold text-success">{{ o.order_number }}</td>
              <td>
                <div>{{ o.customer_name }}</div>
                <small class="text-muted">{{ o.phone }}</small>
              </td>
              <td><span class="badge bg-light text-dark border">{{ o.get_order_type_display }}</span></td>
              <td class="fw-bold">₹{{ o.total_amount }}</td>
              <td>
                <span class="badge {% if o.order_status == 'completed' %}bg-success{% elif o.order_status == 'pending' %}bg-warning text-dark{% else %}bg-primary{% endif %}">
                  {{ o.get_order_status_display }}
                </span>
              </td>
              <td>
                <a href="/admin/orders/order/{{ o.id }}/change/" class="btn btn-sm btn-outline-secondary">
                  <i class="bi bi-pencil-square"></i> Edit
                </a>
              </td>
            </tr>
            {% empty %}
            <tr>
              <td colspan="6" class="text-center text-muted py-4">Abhi koi order nahi aaya hai.</td>
            </tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <div class="col-lg-4">
    <div class="card p-4 border-0 mb-4">
      <h5 class="fw-bold mb-3">Quick Cafe Controls</h5>
      <div class="d-grid gap-2">
        <a href="/admin/menu/fooditem/add/" class="btn btn-cafe text-start"><i class="bi bi-plus-circle me-2"></i> Add New Dish</a>
        <a href="/admin/tables/cafetable/" class="btn btn-outline-cafe text-start"><i class="bi bi-qr-code me-2"></i> View Table QRs</a>
        <a href="/admin/delivery/deliveryassignment/" class="btn btn-outline-secondary text-start"><i class="bi bi-bicycle me-2"></i> Assign Deliveries</a>
        <a href="/admin/contact/contactmessage/" class="btn btn-outline-secondary text-start"><i class="bi bi-envelope me-2"></i> View Feedback</a>
      </div>
    </div>
  </div>
</div>
{% endblock %}
"""

os.makedirs('static/css', exist_ok=True)
os.makedirs('templates/admin_custom', exist_ok=True)

with open('static/css/style.css', 'w', encoding='utf-8') as f:
    f.write(css_code.strip())

with open('templates/admin_custom/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(dashboard_html.strip())

print("\n>>> Premium UI & Stylish Dashboard Successfully Applied! <<<\n")