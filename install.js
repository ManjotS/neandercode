#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const sourceDir = path.join(__dirname, '.cursor');
const targetDir = path.join(process.cwd(), '.cursor');

console.log('🪨 Installing Neandercode (Neandercode mode) for Cursor...');

try {
  fs.cpSync(sourceDir, targetDir, { recursive: true });
  console.log('✅ Neandercode installed successfully!');
  console.log('Open Cursor Chat and type /neandercode to activate.');
  console.log('');
  console.log('Authenticating Cursor Agent for CLI tools...');
  const login = spawnSync('cursor', ['agent', 'login'], { stdio: 'inherit' });
  if (login.error) {
    console.warn('⚠️ Could not run `cursor agent login` automatically:', login.error.message);
    console.warn('Run it manually later, or set CURSOR_API_KEY for non-interactive / CI.');
  } else if (login.status !== 0) {
    console.warn(`⚠️ \`cursor agent login\` exited with code ${login.status}.`);
    console.warn('Run it again manually later, or set CURSOR_API_KEY for non-interactive / CI.');
  } else {
    console.log('✅ Cursor Agent login completed.');
  }
  console.log('');
  console.log('If `cursor agent` fails with a missing @anysphere/... native module:');
  console.log('  cursor agent update');
  console.log('On Apple Silicon Macs, install Cursor’s Apple Silicon (ARM) app — not the Intel/x64 build.');
} catch (err) {
  console.error('❌ Failed to install Neandercode:', err.message);
  process.exit(1);
}