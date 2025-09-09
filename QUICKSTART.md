# Quick Start Guide

Get the Payment Milestone Tracker up and running in 5 minutes!

## Prerequisites

- Python 3.8+
- Node.js 18+
- pnpm (install with `npm install -g pnpm`)

## 1. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd milestone

# Backend setup
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
python manage.py migrate

# Frontend setup
cd ../frontend
pnpm install
```

## 2. Start the Application

**Terminal 1 - Backend:**
```bash
cd backend
.venv\Scripts\activate
python manage.py runserver
```

**Terminal 2 - Frontend:**
```bash
cd frontend
pnpm dev
```

## 3. Access the Application

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **Django Admin:** http://localhost:8000/admin (optional)

## 4. Create Your First Milestone Structure

1. Go to http://localhost:3000
2. Click "Milestone Structures"
3. Click "Create New Structure"
4. Fill in:
   - Name: "Standard 30-60-90"
   - Description: "Standard payment structure"
   - Add milestones:
     - Down Payment: 30%, 0 days, 0 net terms
     - Progress Payment: 40%, 30 days, 15 net terms
     - Final Payment: 30%, 60 days, 30 net terms
5. Click "Create"

## 5. Create Your First Equipment Sale

1. Click "Equipment Sales"
2. Click "Create New Sale"
3. Fill in:
   - Name: "Industrial Equipment Sale"
   - Vendor: "ABC Equipment Co."
   - Quantity: 5
   - Total Amount: $100,000
   - Milestone Structure: Select "Standard 30-60-90"
   - Project Start Date: Today's date
4. Click "Create"

## 6. View the Payment Schedule

1. Click "Gantt Chart"
2. Select "Industrial Equipment Sale - $100,000"
3. View the interactive timeline showing:
   - Payment milestones
   - Due dates
   - Payment amounts
   - Net terms periods

## That's It! 🎉

You now have a fully functional Payment Milestone Tracker. You can:

- Create multiple milestone structures
- Track multiple equipment sales
- Visualize payment schedules
- Export data (when implemented)

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check out [DEVELOPMENT.md](DEVELOPMENT.md) for development guidelines
- Explore the API endpoints at http://localhost:8000/api/

## Troubleshooting

**Backend won't start:**
- Make sure virtual environment is activated
- Check if port 8000 is available
- Run `python manage.py migrate` if you see database errors

**Frontend won't start:**
- Make sure Node.js and pnpm are installed
- Run `pnpm install` to install dependencies
- Check if port 3000 is available

**API calls failing:**
- Make sure backend is running on port 8000
- Check browser console for CORS errors
- Verify API endpoints are accessible

## Need Help?

- Check the [README.md](README.md) for detailed setup instructions
- Review [DEVELOPMENT.md](DEVELOPMENT.md) for development guidelines
- Create an issue in the GitHub repository
