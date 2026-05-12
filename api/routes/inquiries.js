/**
 * Inquiries API Routes
 * Handles tour inquiry submissions
 */

import { sendInquiryEmails, sendNotificationEmail } from '../services/email.js';
import { createCRMLead } from '../services/crm.js';
import { saveInquiry } from '../config/database.js';

export async function handleInquiry(req, res) {
  try {
    const inquiryData = {
      tour: req.body.tour,
      name: req.body.name,
      email: req.body.email,
      phone: req.body.phone,
      message: req.body.message,
      travelDates: req.body.travelDates,
      travelers: req.body.travelers,
      source: req.body.source,
      utmParams: req.body.utmParams,
      createdAt: new Date(),
    };
    
    // Save to database
    const savedInquiry = await saveInquiry(inquiryData);
    
    // Send emails
    await sendInquiryEmails(inquiryData);
    await sendNotificationEmail(inquiryData);
    
    // Create CRM lead
    await createCRMLead(inquiryData);
    
    res.status(200).json({
      success: true,
      message: 'Inquiry submitted successfully',
      id: savedInquiry.id,
    });
  } catch (error) {
    console.error('Inquiry handling error:', error);
    res.status(500).json({
      success: false,
      message: 'Failed to submit inquiry',
      error: error.message,
    });
  }
}

export default { handleInquiry };
