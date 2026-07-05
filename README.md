# Custom App Example

Example custom application for ERPNext multi-tenant setup demonstrating how to build and deploy tenant-specific features.

## Features

### Customer Feedback Management

A complete customer feedback system with:

- **Customer Feedback DocType**: Capture and manage customer feedback with ratings (1-5 stars)
- **Automatic Priority Setting**: Auto-assigns priority based on rating (Low/Medium/High)
- **Email Notifications**: Automatic alerts for low ratings to customer service team
- **Status Tracking**: New → In Review → Resolved → Closed workflow
- **Categories**: Product Quality, Customer Service, Delivery, Pricing, Other

### API Endpoints

#### 1. Send Thank You Email
```python
frappe.call({
    method: 'custom_app_example.api.v1.send_thank_you_email',
    args: { feedback_id: 'CUST-FB-2024-00001' }
})
```

#### 2. Submit Feedback (Public API)
```bash
curl -X POST http://your-site.localhost/api/method/custom_app_example.api.v1.submit_feedback_api \
  -H "Content-Type: application/json" \
  -d '{
    "customer": "CUST-00001",
    "rating": "5",
    "feedback_text": "Excellent service!",
    "category": "Customer Service"
  }'
```

#### 3. Get Analytics
```python
frappe.call({
    method: 'custom_app_example.api.v1.get_feedback_analytics',
    args: {
        from_date: '2024-01-01',
        to_date: '2024-12-31'
    }
})
```

#### 4. Get Customer Feedback History
```python
frappe.call({
    method: 'custom_app_example.api.v1.get_customer_feedback_history',
    args: { customer: 'CUST-00001' }
})
```

## Installation

### 1. Add app to your bench
```bash
cd /workspace/frappe-bench
bench get-app custom_app_example /path/to/apps/custom_app_example
```

### 2. Install app to specific site
```bash
bench --site your-site.localhost install-app custom_app_example
```

### 3. Run migrations
```bash
bench --site your-site.localhost migrate
```

### 4. Build assets
```bash
bench build --app custom_app_example
```

## Usage

### Creating Customer Feedback

1. Navigate to **Customer Feedback** list
2. Click **New**
3. Select **Customer**
4. Choose **Rating** (1-5)
5. Select **Category**
6. Enter **Feedback** text
7. Save

### Features in Action

- **Low Rating Alert**: When rating ≤ 2, system shows warning and sends email to support team
- **Auto Priority**: Priority set automatically based on rating
- **Customer Info**: Customer details auto-filled when customer selected
- **Send Thank You**: Button to send thank you email to customer
- **Response Tracking**: Track who responded and when

## Development

### Hot Reload

When running in development mode, code changes are automatically reloaded:

```bash
# Enable developer mode for site
bench --site your-site.localhost set-config developer_mode 1

# Start with watch
bench watch
```

### File Structure

```
custom_app_example/
├── custom_app_example/
│   ├── __init__.py
│   ├── hooks.py                    # App configuration
│   ├── custom_app_example/         # Main module
│   │   └── doctype/
│   │       └── customer_feedback/
│   │           ├── customer_feedback.json    # DocType metadata
│   │           ├── customer_feedback.py      # Server-side controller
│   │           └── customer_feedback.js      # Client-side script
│   └── api/
│       └── v1.py                   # REST API endpoints
├── setup.py
├── requirements.txt
├── package.json
└── README.md
```

## Multi-Tenant Support

This app can be installed on multiple sites independently:

```bash
# Install on Site 1
bench --site company1.localhost install-app custom_app_example

# Install on Site 2
bench --site company2.localhost install-app custom_app_example
```

Each site maintains its own:
- Database tables
- Customer feedback records
- Configuration
- Email templates

## Testing

```bash
# Run unit tests
bench --site your-site.localhost run-tests --app custom_app_example

# Run specific test
bench --site your-site.localhost run-tests --app custom_app_example --module custom_app_example.tests.test_customer_feedback
```

## License

MIT

## Support

For support, email support@company.com
