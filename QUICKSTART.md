# Quick Setup Guide - Fynd AI Assessment

Get started in 5 minutes!

## Prerequisites
- Python 3.8+
- Git
- Gemini API Key (free at https://ai.google.dev/)

## Local Setup (5 minutes)

### 1. Clone/Download Repository
```bash
cd c:\Users\Sabiha Anjum\Documents\Fynd AI Intern asignment
```

### 2. Set Up Environment
```bash
# Create .env file in task-2 directory
cd task-2
copy .env.example .env

# Edit .env and add your Gemini API key
```

### 3. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
cd ..
```

### 4. Run Backend
```bash
cd backend
python app.py
```

You'll see:
```
 * Running on http://127.0.0.1:5000
```

### 5. Open Dashboards (in browser)
- **User Dashboard**: http://localhost:5000/user
- **Admin Dashboard**: http://localhost:5000/admin
- **API Health**: http://localhost:5000/api/health

## Test It Out

1. Go to http://localhost:5000/user
2. Select a 5-star rating
3. Type a review: "Excellent service!"
4. Click "Submit Review & Get AI Response"
5. See AI-generated response
6. Go to http://localhost:5000/admin to see it in the feed

## Run Jupyter Notebook (Task 1)

```bash
cd task-1
jupyter notebook rating_prediction.ipynb
```

## Deploy in 10 minutes

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions to deploy to Render.com

### Quick Deploy Steps:
1. Push to GitHub
2. Sign up at Render.com
3. Connect GitHub repo
4. Add GEMINI_API_KEY
5. Click Deploy
6. Get your live URLs!

## Troubleshooting

### Backend won't start?
```bash
# Make sure port 5000 is free
netstat -ano | findstr :5000

# If in use, kill the process
taskkill /PID <PID> /F
```

### API connection error?
```bash
# Check if backend is running
curl http://localhost:5000/api/health
```

### LLM errors?
- Verify GEMINI_API_KEY in .env
- Check API quota
- Try again (rate limits are generous)

## File Structure Quick Reference

```
├── task-1/
│   └── rating_prediction.ipynb     ← Run this for Task 1
├── task-2/
│   ├── backend/
│   │   ├── app.py                  ← Main Flask app
│   │   ├── requirements.txt         ← Dependencies
│   │   └── .env.example             ← Copy to .env
│   ├── frontend/
│   │   ├── index.html               ← User dashboard
│   │   └── admin.html               ← Admin dashboard
│   └── data/
│       └── reviews.json             ← Auto-created
├── README.md                        ← Full documentation
├── DEPLOYMENT.md                    ← Deploy guide
└── docs/REPORT.md                   ← Detailed report
```

## Next Steps

1. **Test locally** (verify everything works)
2. **Review code** (in task-1 notebook and task-2/backend)
3. **Deploy** (follow DEPLOYMENT.md)
4. **Submit** with:
   - GitHub repo link
   - User Dashboard URL
   - Admin Dashboard URL
   - Report link

## Common Questions

**Q: Do I need to pay?**
A: No! Use free Gemini API tier + Render free tier

**Q: How long to deploy?**
A: 10-15 minutes once code is pushed to GitHub

**Q: Can I use a different LLM?**
A: Yes! See DEPLOYMENT.md for OpenRouter setup

**Q: Data is stored where?**
A: In JSON file (task-2/data/reviews.json). Upgrade to DB for production.

**Q: Can I customize the UI?**
A: Yes! Edit HTML/CSS in task-2/frontend/

**Q: How to test more reviews?**
A: Submit directly in the UI. No limit!

---

**Ready?** Start with `python task-2/backend/app.py` then open http://localhost:5000
