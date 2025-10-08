# ai-review-tryout

A full-stack product management application built to test AI code review tools. Features a Python FastAPI backend with CRUD operations for product entities and a React frontend generated from Figma designs.

## Tech Stack
- **Backend**: Python FastAPI
- **Frontend**: React + TypeScript (Vite)
- **Purpose**: AI code review tool evaluation

## How to Run

### Frontend (React)
```bash
cd 05_design
yarn install
yarn dev
```

### Backend (FastAPI)
```bash
cd 03_python_fastapi_project
-m uvicorn src.python_fastapi_project.main:app
```

The frontend will be available at `http://localhost:5173` and the backend at `http://localhost:8000`.
