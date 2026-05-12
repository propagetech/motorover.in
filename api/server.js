/**
 * API Server
 * Express server for handling API requests
 */

import express from 'express';
import cors from 'cors';
import { handleInquiry } from './routes/inquiries.js';
import { createBooking } from './routes/bookings.js';
import { getTours, getTour } from './config/database.js';

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(express.json());

// Routes
app.post('/api/inquiries', handleInquiry);
app.post('/api/bookings', createBooking);
app.get('/api/tours', async (req, res) => {
  const tours = await getTours(req.query);
  res.json(tours);
});
app.get('/api/tours/:id', async (req, res) => {
  const tour = await getTour(req.params.id);
  if (!tour) {
    return res.status(404).json({ error: 'Tour not found' });
  }
  res.json(tour);
});

// Health check
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok' });
});

app.listen(PORT, () => {
  console.log(`API server running on port ${PORT}`);
});

export default app;
