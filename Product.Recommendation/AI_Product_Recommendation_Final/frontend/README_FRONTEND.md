# Frontend (React)

## Run
```bash
cd frontend
npm install
npm start
```
The app connects to backend endpoints at `/api/query` and `/api/generate`. If you run backend at a different host/port, update proxy or use full URLs in `src/App.js`.

## Notes
- The UI will show search results and generated descriptions for each product.
- For deployment, build with `npm run build` and serve static files from any static server or integrate with FastAPI static mount.
