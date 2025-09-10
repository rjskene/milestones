# Payment Milestone Tracker

A web application that allows users to create custom payment milestone structures and visualize payment schedules for equipment sales using interactive gantt charts.

## Features

- **Payment Milestone Structures**: Create reusable milestone templates with custom payment percentages, timing, and net terms
- **Equipment Sales Management**: Track equipment sales with vendor information, quantities, and total amounts
- **Interactive Gantt Charts**: Visualize payment schedules using Highcharts with timeline and payment information
- **Responsive Design**: Clean, modern UI that works on desktop and mobile devices
- **RESTful API**: Full CRUD operations for all data entities
- **Data Validation**: Comprehensive validation to ensure data integrity

## Technology Stack

### Backend
- **Django 5.2.6** - Web framework
- **Django REST Framework** - API development
- **SQLite** - Database
- **Python 3.8+** - Programming language

### Frontend
- **Vue.js 3** - Frontend framework with Composition API
- **Vite** - Build tool and development server
- **Vue Router** - Client-side routing
- **Pinia** - State management
- **Highcharts** - Interactive charts and gantt charts
- **Axios** - HTTP client

### Development Tools
- **pnpm** - Package manager
- **Git** - Version control
- **ESLint** - Code linting

## Project Structure

```
milestone/
├── backend/                    # Django backend
│   ├── milestone_backend/      # Django project settings
│   ├── milestones/            # Payment milestone app
│   ├── equipment/             # Equipment sales app
│   ├── utils/                 # Utility functions
│   ├── requirements.txt       # Python dependencies
│   └── manage.py             # Django management script
├── frontend/                  # Vue.js frontend
│   ├── src/
│   │   ├── components/        # Vue components
│   │   ├── stores/           # Pinia stores
│   │   ├── assets/           # Static assets
│   │   └── main.js           # Application entry point
│   ├── package.json          # Node.js dependencies
│   └── vite.config.js        # Vite configuration
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- Node.js 18 or higher
- pnpm (recommended) or npm

### Backend Setup

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   
   # On Windows
   .venv\Scripts\activate
   
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the Django development server:**
   ```bash
   python manage.py runserver
   ```

   The backend API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   pnpm install
   ```

3. **Start the development server:**
   ```bash
   pnpm dev
   ```

   The frontend application will be available at `http://localhost:3000`

## Usage

### Creating Payment Milestone Structures

1. Navigate to the "Milestone Structures" page
2. Click "Create New Structure"
3. Enter a unique name and optional description
4. Add milestones with:
   - Name (e.g., "Down Payment", "Final Payment")
   - Payment percentage (0-100%)
   - Days after previous milestone
   - Net terms days (payment terms after due date)
5. Save the structure

### Creating Equipment Sales

1. Navigate to the "Equipment Sales" page
2. Click "Create New Sale"
3. Fill in the sale details:
   - Sale name
   - Vendor (optional)
   - Quantity
   - Total amount
   - Select a milestone structure
   - Project start date
4. Review the payment preview
5. Save the sale

### Viewing Payment Schedules

1. Navigate to the "Gantt Chart" page
2. Select an equipment sale from the dropdown
3. View the interactive timeline showing:
   - Milestone due dates
   - Payment amounts
   - Net terms periods
   - Visual timeline representation

## API Endpoints

### Milestone Structures
- `GET /api/milestones/structures/` - List all milestone structures
- `POST /api/milestones/structures/` - Create a new milestone structure
- `GET /api/milestones/structures/{id}/` - Get a specific milestone structure
- `PUT /api/milestones/structures/{id}/` - Update a milestone structure
- `DELETE /api/milestones/structures/{id}/` - Delete a milestone structure

### Equipment Sales
- `GET /api/equipment/sales/` - List all equipment sales
- `POST /api/equipment/sales/` - Create a new equipment sale
- `GET /api/equipment/sales/{id}/` - Get a specific equipment sale
- `PUT /api/equipment/sales/{id}/` - Update an equipment sale
- `DELETE /api/equipment/sales/{id}/` - Delete an equipment sale
- `GET /api/equipment/sales/{id}/schedule/` - Get payment schedule for a sale

## Data Models

### PaymentMilestoneStructure
- `name` (CharField, unique) - Structure name
- `description` (TextField, optional) - Structure description
- `created_at` (DateTimeField) - Creation timestamp
- `updated_at` (DateTimeField) - Last update timestamp

### PaymentMilestone
- `structure` (ForeignKey) - Parent milestone structure
- `name` (CharField) - Milestone name
- `payment_percentage` (DecimalField) - Payment percentage (0-100)
- `net_terms_days` (PositiveIntegerField) - Payment terms in days
- `days_after_previous` (PositiveIntegerField) - Days after previous milestone
- `order` (PositiveIntegerField) - Order within structure

### EquipmentSale
- `name` (CharField) - Sale name
- `vendor` (CharField, optional) - Vendor name
- `quantity` (PositiveIntegerField) - Equipment quantity
- `total_amount` (DecimalField) - Total sale amount
- `milestone_structure` (ForeignKey) - Associated milestone structure
- `project_start_date` (DateField) - Project start date
- `created_at` (DateTimeField) - Creation timestamp
- `updated_at` (DateTimeField) - Last update timestamp

## Testing

### Running Backend Tests

```bash
cd backend
python manage.py test
```

### Running Specific Test Suites

```bash
# Test milestone models
python manage.py test milestones.tests

# Test equipment models
python manage.py test equipment.tests

# Test API views
python manage.py test milestones.test_views
python manage.py test equipment.test_views

# Test utility functions
python manage.py test utils.test_utils
```

## Development

### Code Style

- **Python**: Follow PEP 8 guidelines
- **JavaScript/Vue**: Use ESLint configuration
- **Git**: Use descriptive commit messages

### Adding New Features

1. Create feature branch from main
2. Implement changes with tests
3. Update documentation if needed
4. Submit pull request

### Database Changes

1. Create model migrations:
   ```bash
   python manage.py makemigrations
   ```

2. Apply migrations:
   ```bash
   python manage.py migrate
   ```

## Deployment

### Production Considerations

- Use PostgreSQL instead of SQLite for production
- Set up proper environment variables
- Configure CORS settings for production domains
- Use a production WSGI server (e.g., Gunicorn)
- Set up static file serving
- Configure proper logging

### Environment Variables

Create a `.env` file in the backend directory:

```env
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=postgresql://user:password@localhost/dbname
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions or issues, please create an issue in the GitHub repository.

## Changelog

### Version 1.0.0
- Initial release
- Payment milestone structure management
- Equipment sale tracking
- Interactive gantt chart visualization
- RESTful API
- Responsive web interface