# Development Guide

This guide provides detailed information for developers working on the Payment Milestone Tracker project.

## Development Environment Setup

### Prerequisites

- Python 3.8+
- Node.js 18+
- pnpm (recommended) or npm
- Git

### Initial Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd milestone
   ```

2. **Set up backend:**
   ```bash
   cd backend
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # source .venv/bin/activate  # macOS/Linux
   pip install -r requirements.txt
   python manage.py migrate
   ```

3. **Set up frontend:**
   ```bash
   cd frontend
   pnpm install
   ```

## Architecture Overview

### Backend Architecture

The backend follows Django's MVT (Model-View-Template) pattern with REST API:

```
backend/
├── milestone_backend/          # Django project configuration
│   ├── settings.py            # Project settings
│   ├── urls.py               # URL routing
│   └── wsgi.py               # WSGI configuration
├── milestones/               # Payment milestone app
│   ├── models.py             # Data models
│   ├── views.py              # API views
│   ├── serializers.py        # Data serialization
│   ├── urls.py               # App URL routing
│   └── tests.py              # Unit tests
├── equipment/                # Equipment sales app
│   ├── models.py             # Data models
│   ├── views.py              # API views
│   ├── serializers.py        # Data serialization
│   ├── urls.py               # App URL routing
│   └── tests.py              # Unit tests
└── utils/                    # Utility functions
    ├── calculations.py       # Business logic calculations
    ├── validators.py         # Data validation
    ├── formatters.py         # Data formatting
    └── helpers.py            # General utilities
```

### Frontend Architecture

The frontend uses Vue.js 3 with Composition API:

```
frontend/src/
├── components/               # Vue components
│   ├── Dashboard.vue         # Main dashboard
│   ├── MilestoneForm.vue     # Milestone structure form
│   ├── EquipmentSaleForm.vue # Equipment sale form
│   └── GanttChart.vue        # Gantt chart visualization
├── stores/                   # Pinia state management
│   ├── milestoneStore.js     # Milestone data store
│   └── equipmentStore.js     # Equipment data store
├── assets/                   # Static assets
│   └── styles.css            # Global styles
└── main.js                   # Application entry point
```

## Data Flow

### Creating a Payment Milestone Structure

1. User fills out form in `MilestoneForm.vue`
2. Form data is sent to `milestoneStore.js`
3. Store makes API call to `/api/milestones/structures/`
4. Django `PaymentMilestoneStructureViewSet` processes request
5. `PaymentMilestoneStructureSerializer` validates and saves data
6. Response sent back to frontend
7. UI updates with new structure

### Creating an Equipment Sale

1. User fills out form in `EquipmentSaleForm.vue`
2. Form data is sent to `equipmentStore.js`
3. Store makes API call to `/api/equipment/sales/`
4. Django `EquipmentSaleViewSet` processes request
5. `EquipmentSaleSerializer` validates and saves data
6. Response sent back to frontend
7. UI updates with new sale

### Viewing Payment Schedule

1. User selects sale in `GanttChart.vue`
2. Component calls `equipmentStore.getEquipmentSaleSchedule()`
3. API call to `/api/equipment/sales/{id}/schedule/`
4. Django generates schedule data using `get_milestone_schedule()` method
5. Highcharts renders gantt chart with schedule data

## API Design

### RESTful Endpoints

All API endpoints follow REST conventions:

- `GET /api/milestones/structures/` - List milestone structures
- `POST /api/milestones/structures/` - Create milestone structure
- `GET /api/milestones/structures/{id}/` - Get specific structure
- `PUT /api/milestones/structures/{id}/` - Update structure
- `DELETE /api/milestones/structures/{id}/` - Delete structure

### Response Format

All API responses use JSON format:

```json
{
  "id": 1,
  "name": "Standard 30-60-90",
  "description": "Standard payment structure",
  "milestones": [
    {
      "id": 1,
      "name": "Down Payment",
      "payment_percentage": "30.00",
      "net_terms_days": 0,
      "days_after_previous": 0,
      "order": 0
    }
  ],
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### Error Handling

API errors return appropriate HTTP status codes:

- `400 Bad Request` - Validation errors
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server errors

Error response format:

```json
{
  "detail": "Error message",
  "field_errors": {
    "field_name": ["Specific error message"]
  }
}
```

## Database Design

### Entity Relationship Diagram

```
PaymentMilestoneStructure (1) ----< (N) PaymentMilestone
                    |
                    | (1)
                    |
                    | (N)
                EquipmentSale
```

### Key Relationships

- **PaymentMilestoneStructure** has many **PaymentMilestones**
- **EquipmentSale** belongs to one **PaymentMilestoneStructure**
- **PaymentMilestone** belongs to one **PaymentMilestoneStructure**

### Constraints

- Milestone structure names must be unique
- Payment percentages must sum to 100% or less
- Equipment sale quantities must be positive
- Total amounts must be non-negative

## Testing Strategy

### Backend Testing

#### Model Tests
- Test model validation
- Test relationships
- Test business logic methods
- Test constraints

#### API Tests
- Test CRUD operations
- Test validation
- Test error handling
- Test authentication (if added)

#### Utility Tests
- Test calculation functions
- Test validation functions
- Test formatting functions

### Frontend Testing

#### Component Tests
- Test component rendering
- Test user interactions
- Test form validation
- Test API integration

#### Store Tests
- Test state management
- Test API calls
- Test error handling

### Running Tests

```bash
# Backend tests
cd backend
python manage.py test

# Frontend tests (when implemented)
cd frontend
pnpm test
```

## Code Quality

### Python Code Style

- Follow PEP 8
- Use type hints where appropriate
- Write docstrings for functions and classes
- Use meaningful variable names

### JavaScript/Vue Code Style

- Use ESLint configuration
- Follow Vue.js style guide
- Use Composition API
- Write JSDoc comments

### Git Workflow

1. Create feature branch from main
2. Make small, focused commits
3. Write descriptive commit messages
4. Run tests before committing
5. Submit pull request for review

## Performance Considerations

### Backend Optimization

- Use database indexes for frequently queried fields
- Implement pagination for large datasets
- Use select_related() and prefetch_related() for queries
- Cache frequently accessed data

### Frontend Optimization

- Lazy load components
- Use virtual scrolling for large lists
- Optimize bundle size
- Implement proper caching strategies

## Security Considerations

### Backend Security

- Validate all input data
- Use CSRF protection
- Implement proper CORS settings
- Sanitize user input
- Use secure session configuration

### Frontend Security

- Sanitize user input
- Validate data on client side
- Use HTTPS in production
- Implement proper error handling

## Deployment

### Development Deployment

1. **Backend:**
   ```bash
   cd backend
   python manage.py runserver
   ```

2. **Frontend:**
   ```bash
   cd frontend
   pnpm dev
   ```

### Production Deployment

1. **Backend:**
   - Use PostgreSQL database
   - Configure environment variables
   - Use Gunicorn WSGI server
   - Set up Nginx reverse proxy
   - Configure static file serving

2. **Frontend:**
   - Build production bundle: `pnpm build`
   - Serve static files with Nginx
   - Configure proper caching headers

## Troubleshooting

### Common Issues

1. **Database Migration Errors:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Frontend Build Errors:**
   ```bash
   pnpm install
   pnpm build
   ```

3. **API CORS Issues:**
   - Check CORS settings in Django settings
   - Verify frontend API base URL

4. **Highcharts Not Loading:**
   - Check if Highcharts is properly installed
   - Verify component imports

### Debug Mode

Enable debug mode in Django settings for development:

```python
DEBUG = True
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Update documentation
6. Submit pull request

## Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Vue.js Documentation](https://vuejs.org/guide/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Highcharts Documentation](https://www.highcharts.com/docs)
- [Pinia Documentation](https://pinia.vuejs.org/)
