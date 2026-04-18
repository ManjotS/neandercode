#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const sourceDir = path.join(__dirname, '.cursor');
const targetDir = path.join(process.cwd(), '.cursor');

console.log('🪨 Installing Neandercode (Neandercode mode) for Cursor...');

try {
  fs.cpSync(sourceDir, targetDir, { recursive: true });
  console.log('✅ Neandercode installed successfully!');
  console.log('Open Cursor Chat and type /neandercode to activate.');
  console.log('');
  console.log('If `cursor agent` or neandercode-compress fails with a missing native module (@anysphere/...), run:');
  console.log('  cursor agent update');
} catch (err) {
  console.error('❌ Failed to install Neandercode:', err.message);
  process.exit(1);
}