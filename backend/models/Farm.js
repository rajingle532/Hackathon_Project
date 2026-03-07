const mongoose = require('mongoose');

const farmSchema = new mongoose.Schema(
  {
    farmer: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'Farmer',
      required: [true, 'Farmer is required'],
    },
    name: {
      type: String,
      required: [true, 'Farm name is required'],
      trim: true,
    },
    district: {
      type: String,
      trim: true,
    },
    state: {
      type: String,
      trim: true,
    },
    land_size_acres: {
      type: Number,
      required: [true, 'Land size is required'],
    },
    soil_type: {
      type: String,
      default: 'loamy',
    },
    irrigation_type: {
      type: String,
      default: 'rain_fed',
    },
    primary_crops: {
      type: String,
      default: '',
    },
    latitude: {
      type: Number,
    },
    longitude: {
      type: Number,
    },
    nitrogen_value: {
      type: Number,
      min: 0,
      max: 140,
    },
    phosphorus_value: {
      type: Number,
      min: 0,
      max: 145,
    },
    potassium_value: {
      type: Number,
      min: 0,
      max: 205,
    },
    soil_ph: {
      type: Number,
      min: 0,
      max: 14,
    },
  },
  {
    timestamps: { createdAt: 'created_at', updatedAt: 'updated_at' },
  }
);

farmSchema.set('toJSON', {
  virtuals: true,
  transform: (doc, ret) => {
    ret.id = ret._id.toString();
    delete ret.__v;
    return ret;
  },
});

farmSchema.set('toObject', { virtuals: true });

module.exports = mongoose.model('Farm', farmSchema);
