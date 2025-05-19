/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        dancing: ['"Dancing Script"', 'cursive'],
        sans: ['"Times New Roman"', 'serif'],
        poetsen: ['"Poetsen One"', 'cursive'],
      },
      colors: {
        celeste: '#00CFFF',
        blanco: '#FFFFFF',
        rojo: '#FF3B3B',
      },
      screens: {
	sm: '40rem',
	md: '48rem',
	lg: '64rem',
	xl: '80rem',
	'2xl': '96rem',
      },
      spacing: {
        '0' : '0rem',
        '1': '0.25rem',  // 4px
        '2': '0.5rem',   // 8px
        '3': '0.75rem',  // 12px
        '4': '1rem',     // 16px
        '5': '1.25rem',  // 20px
        '6': '1.5rem',   // 24px
        '7': '1.75rem',  // 28px
        '8': '2rem',     // 32px
        '9': '2.25rem',  // 36px
        '10': '2.5rem',  // 40px
        '12': '3rem',    // 48px
        '16': '4rem',    // 64px
        '20': '5rem',    // 80px
        '24': '6rem',    // 96px
      }
    },
  },
  plugins: [],
}

