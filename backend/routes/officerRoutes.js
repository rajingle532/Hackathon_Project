const express = require('express');
const router = express.Router();
const {
  listOfficers,
  getOfficer,
  bookConsultation,
  listConsultations,
  cancelConsultation,
  getAIExperts,
  saveAIExpert
} = require('../controllers/officerController');

router.get('/ai-experts', getAIExperts);
router.post('/ai-experts/save', saveAIExpert);
router.get('/', listOfficers);
router.get('/:id', getOfficer);
router.post('/consultations', bookConsultation);
router.get('/consultations/list', listConsultations);
router.patch('/consultations/:id/cancel', cancelConsultation);

module.exports = router;
