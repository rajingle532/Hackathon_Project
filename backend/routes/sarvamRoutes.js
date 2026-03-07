const express = require('express');
const router = express.Router();
const { sttTranslate, translateText, translateBatch } = require('../controllers/sarvamController');

// POST /api/sarvam/stt-translate — Audio file → English translated text
router.post('/stt-translate', ...sttTranslate);

// POST /api/sarvam/translate — Text → translated text
router.post('/translate', translateText);

// POST /api/sarvam/translate-batch — Array of texts → translated texts
router.post('/translate-batch', translateBatch);

module.exports = router;
