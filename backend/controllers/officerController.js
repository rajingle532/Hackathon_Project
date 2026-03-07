const Officer = require('../models/Officer');
const Consultation = require('../models/Consultation');

// ─── Officer name banks per state language ──────────────────────────
const STATE_NAMES = {
  'Andhra Pradesh':    { first: ['Venkata','Srinivas','Ramesh','Lakshmi','Padma','Raja','Suresh','Anand','Krishna','Vijay'], last: ['Reddy','Naidu','Rao','Sharma','Kumar','Prasad'] },
  'Arunachal Pradesh': ['Tashi Dorji','Nabam Tuki','Pema Khandu','Kiren Rijiju','Rina Tao','Bamin Yani','Takam Pario','Jarjum Ete','Chowna Mein','Taba Hali'],
  'Assam':             { first: ['Bhupen','Jyoti','Hemen','Pranjal','Dimbeswar','Lakshmi','Ritu','Kamal','Debajit','Parag'], last: ['Bora','Das','Hazarika','Sarma','Kalita','Baruah'] },
  'Bihar':             { first: ['Rajesh','Anil','Sunil','Vinod','Manoj','Priya','Sanjay','Ravi','Deepak','Ashok'], last: ['Kumar','Singh','Prasad','Chaudhary','Yadav','Mishra'] },
  'Chhattisgarh':      { first: ['Ramesh','Bhupesh','Tamradhwaj','Champa','Kavita','Sunil','Anil','Renu','Devendra','Prem'], last: ['Sahu','Verma','Patel','Tiwari','Nag','Dewangan'] },
  'Goa':               { first: ['Pramod','Francis','Antonio','Maria','Savio','Fatima','Rajesh','Deepak','Sunita','Nandini'], last: ['Sawant','D\'Souza','Fernandes','Naik','Gawas','Desai'] },
  'Gujarat':           { first: ['Mukesh','Jagdish','Hasmukh','Bharat','Ramesh','Jyoti','Divya','Komal','Tushar','Nitin'], last: ['Patel','Shah','Desai','Modi','Chauhan','Parmar'] },
  'Haryana':           { first: ['Suresh','Ramesh','Satish','Rajbir','Naresh','Sunita','Anita','Sandeep','Vikas','Anil'], last: ['Kumar','Singh','Yadav','Malik','Hooda','Tanwar'] },
  'Himachal Pradesh':  { first: ['Jai','Prem','Virbhadra','Shanta','Suresh','Anil','Rattan','Mukesh','Kamlesh','Asha'], last: ['Singh','Sharma','Thakur','Verma','Chauhan','Negi'] },
  'Jharkhand':         { first: ['Hemant','Babulal','Champa','Draupadi','Raghubar','Suresh','Anil','Binod','Manoj','Sanjay'], last: ['Soren','Murmu','Singh','Oraon','Mahto','Kumar'] },
  'Karnataka':         { first: ['Basavaraj','Siddaramaiah','Yediyurappa','Kumaraswamy','Reshma','Deepa','Venkatesh','Suresh','Raghav','Mahesh'], last: ['Gowda','Shetty','Naik','Patil','Hegde','Rao'] },
  'Kerala':            { first: ['Pinarayi','Oommen','Shashi','Thomas','Rosamma','Deepa','Rajesh','Suresh','Anil','Kumari'], last: ['Vijayan','Chandy','Tharoor','Isaac','Nair','Menon','Pillai','Kurup'] },
  'Madhya Pradesh':    { first: ['Shivraj','Kamal','Digvijay','Uma','Jyoti','Rajesh','Sandeep','Umesh','Anil','Mohan'], last: ['Chouhan','Nath','Singh','Tiwari','Mishra','Patel'] },
  'Maharashtra':       { first: ['Uddhav','Devendra','Ajit','Sharad','Supriya','Amruta','Rajesh','Sachin','Anil','Vinod'], last: ['Thackeray','Fadnavis','Pawar','Patil','Deshmukh','Jadhav'] },
  'Manipur':           { first: ['Biren','Ibobi','Okram','Tomba','Ibemhal','Chanu','Laishram','Yumnam','Thokchom','Akoijam'], last: ['Singh','Devi','Meitei','Sharma','Luwang'] },
  'Meghalaya':         { first: ['Conrad','Mukul','Donkupar','Pynhun','Balajied','Hambok','Kyrmen','Lasborn','Wanjop','Khraw'], last: ['Sangma','Syiemlieh','Lyngdoh','Marbaniang','Rymbai'] },
  'Mizoram':           { first: ['Zoramthanga','Lalduhoma','Lalthanhawla','Vanlalzawma','Zothanpuii','Lalremsiami','Lalbiakzuala','Malsawma','Lalchhuanawma','R.Tlanghmingthanga'], last: [] },
  'Nagaland':          { first: ['Neiphiu','T.R.','Temjen','Shurhozelie','Hekani','Visasolie','Tokheho','Keneizhakho','Neidonuo','Vitshu'], last: ['Rio','Zeliang','Imna','Liezietsu','Jakhalu','Angami'] },
  'Odisha':            { first: ['Naveen','Bijay','Dharmendra','Pratap','Jyoti','Mamata','Dibya','Sasmita','Sudhansu','Brundaban'], last: ['Patnaik','Mohanty','Pradhan','Nayak','Behera','Das'] },
  'Punjab':            { first: ['Bhagwant','Amarinder','Parkash','Sukhbir','Harsimrat','Navjot','Gurpreet','Manpreet','Jaswinder','Kulwinder'], last: ['Mann','Singh','Badal','Kaur','Sidhu','Brar'] },
  'Rajasthan':         { first: ['Ashok','Vasundhara','Sachin','Hanuman','Diya','Raghu','Govind','Babu','Jyoti','Madan'], last: ['Gehlot','Raje','Pilot','Beniwal','Sharma','Meena','Gurjar'] },
  'Sikkim':            { first: ['Prem','Pawan','Bina','Mingma','Tshering','Karma','Sonam','Dawa','Phurba','Nima'], last: ['Tamang','Gurung','Sherpa','Lepcha','Bhutia','Subba'] },
  'Tamil Nadu':        { first: ['Muthuvel','Edappadi','Jayalalithaa','Karunanidhi','Kanimozhi','Sudha','Senthil','Arun','Karthik','Lakshmi'], last: ['Stalin','Palaniswami','Panneerselvam','Ramachandran','Murugan','Kumar'] },
  'Telangana':         { first: ['Kalvakuntla','Bandi','Revanth','Harish','Kavitha','Padma','Suresh','Venkat','Ravi','Srinivas'], last: ['Rao','Reddy','Sagar','Gupta','Naidu','Sharma'] },
  'Tripura':           { first: ['Biplab','Manik','Jishnu','Pratima','Ratan','Bhanulal','Sudip','Nabakumar','Tinku','Sanjay'], last: ['Deb','Sarkar','Debbarma','Saha','Roy','Das'] },
  'Uttar Pradesh':     { first: ['Yogi','Akhilesh','Mayawati','Priyanka','Rajnath','Dinesh','Anita','Suresh','Ramesh','Brij'], last: ['Adityanath','Yadav','Singh','Sharma','Mishra','Verma'] },
  'Uttarakhand':       { first: ['Pushkar','Trivendra','Harish','Tirath','Harak','Indira','Satpal','Madan','Pritam','Kunwar'], last: ['Dhami','Rawat','Singh','Negi','Chauhan','Bisht'] },
  'West Bengal':       { first: ['Mamata','Subhas','Dilip','Abhishek','Mala','Partha','Sourav','Debashis','Tapas','Ananya'], last: ['Banerjee','Ghosh','Chatterjee','Bose','Roy','Mukherjee','Das'] },
};

const DESIGNATIONS = [
  'District Agricultural Officer (DAO)',
  'Block Development Officer (BDO)',
  'Assistant Director of Agriculture',
  'Deputy Director of Agriculture',
  'Agricultural Extension Officer',
  'Horticulture Development Officer',
  'Soil Conservation Officer',
  'Plant Protection Officer',
  'District Horticulture Officer',
  'Krishi Vigyan Kendra (KVK) Head',
  'State Agricultural Research Station Head',
  'Agricultural Technology Manager'
];

const SPECIALIZATIONS = [
  'Crop Production & Management',
  'Soil Health & Fertility Management',
  'Plant Protection & Pest Management',
  'Horticulture Development',
  'Organic Farming & Certification',
  'Water Management & Irrigation',
  'Post-Harvest Technology',
  'Agricultural Marketing',
  'Farm Mechanization',
  'Seed Quality & Certification',
  'Rice Cultivation',
  'Spice Cultivation'
];

const DEPARTMENTS = [
  'Department of Agriculture & Farmers Welfare',
  'Directorate of Agriculture',
  'Krishi Vigyan Kendra',
  'Indian Council of Agricultural Research',
  'State Horticulture Mission',
  'National Horticulture Board'
];

// ─── Deterministic hash for consistent officer data ─────────────────
function simpleHash(str) {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = ((hash << 5) - hash) + str.charCodeAt(i);
    hash |= 0;
  }
  return Math.abs(hash);
}

function generateOfficerName(state, index) {
  const nameData = STATE_NAMES[state] || STATE_NAMES['Uttar Pradesh'];
  if (Array.isArray(nameData)) {
    return nameData[index % nameData.length];
  }
  const first = nameData.first[index % nameData.first.length];
  const last = nameData.last[(index + 3) % nameData.last.length];
  return `${first} ${last}`;
}

function generateEmail(name, dept) {
  const clean = name.toLowerCase().replace(/[^a-z ]/g, '').replace(/\s+/g, '.');
  const domains = ['gov.in', 'nic.in', 'agriculture.gov.in'];
  return `${clean}@${domains[simpleHash(name) % domains.length]}`;
}

function generatePhone(state, index) {
  const prefixes = ['94', '98', '97', '96', '95', '70', '88', '91', '99', '87'];
  const prefix = prefixes[(simpleHash(state) + index) % prefixes.length];
  const num = String(simpleHash(state + index + 'ph') % 100000000).padStart(8, '0');
  return `+91 ${prefix}${num}`;
}

// ─── 1) List officers by state/district ─────────────────────────────
exports.listOfficers = async (req, res) => {
  try {
    const { state, district, specialization } = req.query;

    // Check DB first
    const query = {};
    if (state) query.state = state;
    if (district) query.district = district;
    if (specialization && specialization !== 'All Specializations') query.specialization = specialization;

    let officers = await Officer.find(query).sort({ rating: -1 }).limit(30);

    if (officers.length === 0 && state) {
      // Generate officers for this state/district
      officers = await seedOfficersForLocation(state, district);
      if (specialization && specialization !== 'All Specializations') {
        officers = officers.filter(o => o.specialization === specialization);
      }
    }

    res.json({ success: true, data: officers });
  } catch (error) {
    console.error('listOfficers error:', error);
    res.status(500).json({ success: false, message: 'Server error' });
  }
};

// ─── Seed officers for a state/district ─────────────────────────────
async function seedOfficersForLocation(state, district) {
  const count = district ? 6 : 10;
  const officers = [];

  for (let i = 0; i < count; i++) {
    const seed = simpleHash(`${state}${district || ''}${i}`);
    const name = generateOfficerName(state, i);
    const designation = DESIGNATIONS[i % DESIGNATIONS.length];
    const specialization = SPECIALIZATIONS[i % SPECIALIZATIONS.length];
    const department = DEPARTMENTS[i % DEPARTMENTS.length];

    const districtName = district || state;
    const address = `${designation.split('(')[0].trim()} Office, ${districtName}, ${state} - ${String(500000 + (seed % 50000)).padStart(6, '0')}`;

    const officer = await Officer.create({
      name,
      designation,
      department,
      specialization,
      state,
      district: district || 'State Level',
      office_address: address,
      phone: generatePhone(state, i),
      email: generateEmail(name, department),
      available_hours: i % 3 === 0 ? '9:00 AM - 5:00 PM' : i % 3 === 1 ? '10:00 AM - 4:00 PM' : '10:00 AM - 6:00 PM',
      experience_years: 5 + (seed % 25),
      languages: getLanguages(state),
      rating: parseFloat((3.5 + (seed % 15) / 10).toFixed(1)),
      is_available: i % 5 !== 4,
      consultation_fee: i % 4 === 0 ? '₹100' : 'Free'
    });
    officers.push(officer);
  }
  return officers;
}

function getLanguages(state) {
  const langMap = {
    'Andhra Pradesh': 'Telugu, Hindi, English',
    'Assam': 'Assamese, Hindi, English',
    'Bihar': 'Hindi, Bhojpuri, English',
    'Gujarat': 'Gujarati, Hindi, English',
    'Haryana': 'Hindi, English',
    'Karnataka': 'Kannada, Hindi, English',
    'Kerala': 'Malayalam, Hindi, English',
    'Madhya Pradesh': 'Hindi, English',
    'Maharashtra': 'Marathi, Hindi, English',
    'Punjab': 'Punjabi, Hindi, English',
    'Rajasthan': 'Hindi, Rajasthani, English',
    'Tamil Nadu': 'Tamil, Hindi, English',
    'Telangana': 'Telugu, Hindi, English',
    'Uttar Pradesh': 'Hindi, English',
    'West Bengal': 'Bengali, Hindi, English',
  };
  return langMap[state] || 'Hindi, English';
}

// ─── 2) Get single officer ──────────────────────────────────────────
exports.getOfficer = async (req, res) => {
  try {
    const officer = await Officer.findById(req.params.id);
    if (!officer) return res.status(404).json({ success: false, message: 'Officer not found' });
    res.json({ success: true, data: officer });
  } catch (error) {
    console.error('getOfficer error:', error);
    res.status(500).json({ success: false, message: 'Server error' });
  }
};

// ─── 3) Book consultation ───────────────────────────────────────────
exports.bookConsultation = async (req, res) => {
  try {
    const { farmer, officer, subject, description, consultation_type, preferred_date, preferred_time, farmer_phone, farmer_location, notes } = req.body;

    if (!farmer || !officer || !subject || !preferred_date) {
      return res.status(400).json({ success: false, message: 'Missing required fields: farmer, officer, subject, preferred_date' });
    }

    const consultation = await Consultation.create({
      farmer, officer, subject, description,
      consultation_type: consultation_type || 'phone',
      preferred_date: new Date(preferred_date),
      preferred_time: preferred_time || '10:00 AM',
      farmer_phone, farmer_location, notes,
      status: 'pending'
    });

    const populated = await Consultation.findById(consultation._id)
      .populate('officer', 'name designation phone')
      .populate('farmer', 'name phone');

    res.status(201).json({ success: true, data: populated });
  } catch (error) {
    console.error('bookConsultation error:', error);
    res.status(500).json({ success: false, message: 'Server error' });
  }
};

// ─── 4) List consultations for a farmer ─────────────────────────────
exports.listConsultations = async (req, res) => {
  try {
    const { farmer_id, status } = req.query;
    if (!farmer_id) return res.status(400).json({ success: false, message: 'farmer_id is required' });

    const query = { farmer: farmer_id };
    if (status) query.status = status;

    const consultations = await Consultation.find(query)
      .sort({ createdAt: -1 })
      .limit(30)
      .populate('officer', 'name designation phone specialization')
      .populate('farmer', 'name phone');

    res.json({ success: true, data: consultations });
  } catch (error) {
    console.error('listConsultations error:', error);
    res.status(500).json({ success: false, message: 'Server error' });
  }
};

// ─── 5) Cancel a consultation ───────────────────────────────────────
exports.cancelConsultation = async (req, res) => {
  try {
    const consultation = await Consultation.findByIdAndUpdate(
      req.params.id,
      { status: 'cancelled' },
      { new: true }
    );
    if (!consultation) return res.status(404).json({ success: false, message: 'Not found' });
    res.json({ success: true, data: consultation });
  } catch (error) {
    console.error('cancelConsultation error:', error);
    res.status(500).json({ success: false, message: 'Server error' });
  }
};

// ─── 5.5) Save AI expert to DB (so it gets a real ObjectId) ─────────
exports.saveAIExpert = async (req, res) => {
  try {
    const { name, designation, department, specialization, state, district,
            office_address, phone, email, available_hours, experience_years,
            languages, rating, is_available, consultation_fee } = req.body;

    if (!name || !state) {
      return res.status(400).json({ success: false, message: 'Name and state are required' });
    }

    // Check if already saved
    let officer = await Officer.findOne({ name, state });
    if (officer) {
      return res.json({ success: true, data: officer, existing: true });
    }

    officer = await Officer.create({
      name, designation: designation || 'Agricultural Expert',
      department: department || 'Department of Agriculture',
      specialization: specialization || 'General Agriculture',
      state, district: district || 'State Level',
      office_address: office_address || '',
      phone: phone || '', email: email || '',
      available_hours: available_hours || '10:00 AM - 5:00 PM',
      experience_years: experience_years || 10,
      languages: languages || 'Hindi, English',
      rating: rating || 4.0,
      is_available: is_available !== false,
      consultation_fee: consultation_fee || 'Free'
    });

    console.log(`✅ Saved AI expert to DB: ${name} (${officer._id})`);
    res.status(201).json({ success: true, data: officer });
  } catch (error) {
    console.error('saveAIExpert error:', error);
    res.status(500).json({ success: false, message: 'Failed to save expert' });
  }
};

// ─── 6) AI-powered authentic experts list ───────────────────────────
exports.getAIExperts = async (req, res) => {
  try {
    const { state } = req.query;
    if (!state) {
      return res.status(400).json({ success: false, message: 'State is required' });
    }

    const GEMINI_API_KEY = process.env.GEMINI_API_KEY;
    if (!GEMINI_API_KEY) {
      return res.json({ success: true, data: getHardcodedExperts(state), source: 'fallback' });
    }

    const prompt = `You are an Indian agricultural administration expert. Generate details of 6 representative senior agricultural officers and scientists who would typically serve in ${state}, India. These should be realistic profiles based on the typical agricultural administration structure of ${state}.

Return a JSON array. No markdown, no explanation, ONLY the JSON array:
[{"name":"Dr. Example Name","designation":"Director of Agriculture","department":"Department of Agriculture, ${state}","specialization":"Crop Science","office_address":"Directorate of Agriculture, Capital City, ${state}","phone":"0755-2551234","email":"director.agri@mp.gov.in","experience_years":20,"languages":"Hindi, English","rating":4.7,"is_available":true,"consultation_fee":"Free","notable_work":"Pioneered organic farming initiatives across the state"}]

Guidelines:
- Generate culturally appropriate names for ${state}
- Include mix of: State Agriculture Director, KVK Scientist, ICAR Researcher, University Professor, District Agriculture Officer, Horticulture Officer
- Use department names like: Department of Agriculture ${state}, ICAR, Krishi Vigyan Kendra, State Agricultural University
- Use realistic STD code phone numbers for ${state}
- Emails should use domains like gov.in, nic.in, icar.gov.in
- Notable work should relate to ${state}'s key crops and agricultural challenges
- Return exactly 6 entries as a JSON array`;

    console.log(`🤖 Fetching AI experts for ${state}...`);

    const response = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${GEMINI_API_KEY}`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contents: [{ parts: [{ text: prompt }] }],
          generationConfig: { temperature: 0.8, maxOutputTokens: 8192 }
        })
      }
    );

    const result = await response.json();

    // Log full response for debugging
    if (!result.candidates || result.candidates.length === 0) {
      console.error('⚠️ Gemini returned no candidates. Full response:', JSON.stringify(result).substring(0, 500));
    }

    const text = result?.candidates?.[0]?.content?.parts?.[0]?.text || '';

    if (!text) {
      console.error('⚠️ Empty Gemini text. Blocked reason:', result?.candidates?.[0]?.finishReason, 'Prompt feedback:', JSON.stringify(result?.promptFeedback || {}));
      return res.json({ success: true, data: getHardcodedExperts(state), source: 'fallback' });
    }

    let experts;
    try {
      let jsonStr = text.replace(/```json\n?/g, '').replace(/```\n?/g, '').trim();

      // Attempt to repair truncated JSON
      if (jsonStr && !jsonStr.endsWith(']')) {
        const lastBrace = jsonStr.lastIndexOf('}');
        if (lastBrace > 0) {
          jsonStr = jsonStr.substring(0, lastBrace + 1) + ']';
        }
      }

      experts = JSON.parse(jsonStr);
      if (!Array.isArray(experts)) throw new Error('Not an array');
      console.log(`✅ Got ${experts.length} AI experts for ${state}`);
    } catch (parseErr) {
      console.error('Failed to parse AI experts:', parseErr.message);
      console.error('Raw text length:', text.length, 'First 300 chars:', text.substring(0, 300));
      experts = getHardcodedExperts(state);
    }

    // Add state field and IDs
    experts = experts.map((e, i) => ({
      _id: `ai_${state.replace(/\s+/g, '_')}_${i}`,
      ...e,
      state,
      district: 'State Level',
      available_hours: i % 3 === 0 ? '9:00 AM - 5:00 PM' : i % 3 === 1 ? '10:00 AM - 4:00 PM' : '10:00 AM - 6:00 PM',
      rating: e.rating || (4.0 + (i % 10) / 10),
      is_available: e.is_available !== false,
      consultation_fee: e.consultation_fee || 'Free',
      experience_years: e.experience_years || (10 + i * 2),
      languages: e.languages || getLanguages(state),
    }));

    res.json({ success: true, data: experts, source: 'gemini_ai' });
  } catch (error) {
    console.error('getAIExperts error:', error);
    res.status(500).json({ success: false, message: 'Failed to fetch AI experts' });
  }
};

function getHardcodedExperts(state) {
  const langMap = {
    'Kerala': 'Malayalam, Hindi, English', 'Tamil Nadu': 'Tamil, Hindi, English',
    'Karnataka': 'Kannada, Hindi, English', 'Andhra Pradesh': 'Telugu, Hindi, English',
    'Telangana': 'Telugu, Hindi, English', 'Maharashtra': 'Marathi, Hindi, English',
    'Gujarat': 'Gujarati, Hindi, English', 'Punjab': 'Punjabi, Hindi, English',
    'West Bengal': 'Bengali, Hindi, English', 'Assam': 'Assamese, Hindi, English',
    'Odisha': 'Odia, Hindi, English', 'Rajasthan': 'Hindi, Rajasthani, English',
    'Bihar': 'Hindi, Bhojpuri, English', 'Madhya Pradesh': 'Hindi, English',
    'Chhattisgarh': 'Hindi, Chhattisgarhi, English', 'Jharkhand': 'Hindi, English',
    'Uttar Pradesh': 'Hindi, English', 'Haryana': 'Hindi, English',
  };
  const langs = langMap[state] || 'Hindi, English';

  // State-specific name prefixes
  const nameBank = STATE_NAMES[state];
  const getName = (i) => {
    if (!nameBank) return `Dr. Officer ${i + 1}`;
    if (Array.isArray(nameBank)) return nameBank[i % nameBank.length];
    return `Dr. ${nameBank.first[i % nameBank.first.length]} ${nameBank.last[(i + 2) % nameBank.last.length]}`;
  };

  const templates = [
    { designation: 'Director of Agriculture', department: `Department of Agriculture & Farmers Welfare, ${state}`, specialization: 'Crop Production & Policy', notable_work: `Leading state-wide crop diversification and soil health programs in ${state}.` },
    { designation: 'Head, Krishi Vigyan Kendra', department: `ICAR - KVK, ${state}`, specialization: 'Soil Health & Fertility Management', notable_work: `Conducted 500+ farmer training programs and soil testing camps across ${state}.` },
    { designation: 'Professor of Agronomy', department: `State Agricultural University, ${state}`, specialization: 'Agronomy & Crop Science', notable_work: `Published 50+ research papers on sustainable farming practices for ${state}'s climate.` },
    { designation: 'Principal Scientist, ICAR', department: `ICAR Regional Research Station, ${state}`, specialization: 'Plant Protection & Pest Management', notable_work: `Developed integrated pest management protocols for major crops in ${state}.` },
    { designation: 'Deputy Director of Horticulture', department: `Directorate of Horticulture, ${state}`, specialization: 'Horticulture Development', notable_work: `Expanded fruit and vegetable cultivation under National Horticulture Mission in ${state}.` },
    { designation: 'Agricultural Extension Officer', department: `District Agriculture Office, ${state}`, specialization: 'Farm Extension & Technology Transfer', notable_work: `Facilitated adoption of modern farming techniques among 10,000+ farmers in ${state}.` },
  ];

  return templates.map((t, i) => ({
    _id: `fb_${state.replace(/\s+/g, '_')}_${i}`,
    name: getName(i),
    ...t,
    state,
    district: 'State Level',
    office_address: `${t.designation} Office, ${state}`,
    phone: `+91 ${String(7000000000 + simpleHash(state + i) % 999999999)}`,
    email: `${getName(i).toLowerCase().replace(/[^a-z]/g, '.').replace(/\.+/g, '.').slice(0, 15)}@${i % 2 === 0 ? 'gov.in' : 'icar.gov.in'}`,
    experience_years: 12 + (i * 3),
    languages: langs,
    rating: parseFloat((4.0 + (i % 8) / 10).toFixed(1)),
    is_available: i !== 4,
    consultation_fee: i === 0 ? '₹100' : 'Free',
    available_hours: i % 3 === 0 ? '9:00 AM - 5:00 PM' : i % 3 === 1 ? '10:00 AM - 4:00 PM' : '10:00 AM - 6:00 PM',
  }));
}

