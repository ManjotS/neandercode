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
  console.log('For CLI tools (neandercode-compress, evals), authenticate the agent once:');
  console.log('  cursor agent login');
  console.log('(Or set CURSOR_API_KEY for non-interactive / CI.)');
  console.log('');
  console.log('If `cursor agent` fails with a missing @anysphere/... native module:');
  console.log('  cursor agent update');
  console.log('On Apple Silicon Macs, install Cursor’s Apple Silicon (ARM) app — not the Intel/x64 build.');
} catch (err) {
  console.error('❌ Failed to install Neandercode:', err.message);
  process.exit(1);
}