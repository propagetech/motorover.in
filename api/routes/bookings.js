/**
 * Bookings API Routes
 * Handles tour booking creation and payment processing
 */

import { processPayment } from '../services/payment.js';
import { sendBookingConfirmation } from '../services/email.js';
import { saveBooking } from '../config/database.js';

export async function createBooking(req, res) {
  try {
    const bookingData = {
      tour: req.body.tour,
      dates: req.body.dates,
      travelers: req.body.travelers,
      addons: req.body.addons,
      totalPrice: req.body.totalPrice,
      paymentMethod: req.body.paymentMethod,
      createdAt: new Date(),
    };
    
    // Process payment
    const paymentResult = await processPayment({
      amount: bookingData.totalPrice,
      method: bookingData.paymentMethod,
      bookingData,
    });
    
    if (!paymentResult.success) {
      return res.status(400).json({
        success: false,
        message: 'Payment failed',
        error: paymentResult.error,
      });
    }
    
    // Save booking
    bookingData.paymentId = paymentResult.paymentId;
    const savedBooking = await saveBooking(bookingData);
    
    // Send confirmation email
    await sendBookingConfirmation(bookingData);
    
    res.status(200).json({
      success: true,
      message: 'Booking created successfully',
      booking: savedBooking,
    });
  } catch (error) {
    console.error('Booking creation error:', error);
    res.status(500).json({
      success: false,
      message: 'Failed to create booking',
      error: error.message,
    });
  }
}

export default { createBooking };
