/** @type {import('tailwindcss').Config} */
export default {
  theme: {
    extend: {
      colors: {
        // Enameled steel console
        steel: {
          950: '#141619',
          900: '#191c20',
          850: '#1e2228',
          800: '#23272d',
          700: '#2c313a',
          600: '#373d47',
          500: '#464d59',
          400: '#5a6270',
        },
        // Engraved / enamel signage
        enamel: {
          DEFAULT: '#e9e3d4',
          dim: '#a9b1bd',
          faint: '#7c8593',
        },
        // Signal lamps — the color system IS the state
        lamp: {
          draft: '#7a8593',
          todo: '#4a9fd4',
          doing: '#f2a41c',
          done: '#4bbd6b',
          trash: '#df5140',
        },
      },
      fontFamily: {
        stencil: ['"Saira Stencil One"', 'system-ui', 'sans-serif'],
        placard: ['"Saira Condensed"', 'system-ui', 'sans-serif'],
        sans: ['Saira', 'system-ui', 'sans-serif'],
        mono: ['"Spline Sans Mono"', 'ui-monospace', 'monospace'],
      },
      boxShadow: {
        cell: '0 1px 0 0 rgba(255,255,255,0.05) inset, 0 -1px 0 0 rgba(0,0,0,0.4) inset, 0 2px 4px rgba(0,0,0,0.35)',
        raised:
          '0 1px 0 0 rgba(255,255,255,0.08) inset, 0 14px 30px -12px rgba(0,0,0,0.7), 0 4px 10px rgba(0,0,0,0.4)',
        console:
          '0 1px 0 0 rgba(255,255,255,0.04) inset, 0 24px 60px -30px rgba(0,0,0,0.8)',
      },
      keyframes: {
        'lamp-pulse': {
          '0%,100%': { opacity: '1' },
          '50%': { opacity: '0.55' },
        },
      },
      animation: {
        'lamp-pulse': 'lamp-pulse 1.8s cubic-bezier(0.4,0,0.6,1) infinite',
      },
    },
  },
  plugins: [],
}
