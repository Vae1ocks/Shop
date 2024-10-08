const { createGlobPatternsForDependencies } = require('@nx/angular/tailwind');
const { join } = require('path');

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    join(__dirname, 'src/**/!(*.stories|*.spec).{ts,html}'),
    ...createGlobPatternsForDependencies(__dirname),
  ],
  theme: {
    colors: {
      'purple': '#7F23E1',
      'light-purple': '#C9A5ED',
      'gray': 'rgb(135 135 135)',
      'red': 'rgb(255 32 32)',
    },
    extend: {
      borderRadius: {
        'DEFAULT': '0.875rem',
      }
    },
  },
  plugins: [],
};
