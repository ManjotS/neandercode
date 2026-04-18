#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const sourceDir = path.join(__dirname, '.cursor');
const targetDir = path.join(process.cwd(), '.cursor');

console.log('🪨 Installing Neandercode (Caveman mode) for Cursor...');

try {
  fs.cpSync(sourceDir, targetDir, { recursive: true });
  console.log('✅ Neandercode installed successfully!');
  console.log('Open Cursor Chat and type /caveman to activate.');
} catch (err) {
  console.error('❌ Failed to install Neandercode:', err.message);
  process.exit(1);
}