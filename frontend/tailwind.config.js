/** @type {import('tailwindcss').Config} */
export default {
  theme: {
    extend: {
      colors: {
        // === Portfolio monochrome system (canonical tokens) ===
        // Black / white / grays only. Colour is reserved for the state lamps,
        // exactly as the portfolio reserves colour for brand icons.
        ink: '#1a1a1a', // primary text + dark accent
        cloud: '#e5e5e5', // page ground
        mist: '#999999', // decorative gray (dividers)
        muted: '#5c5c5c', // secondary text on light (AA-safe)
        surface: '#ffffff', // cards / raised faces

        // Signal lamps — the ONLY chromatic accent, carries state meaning.
        lamp: {
          draft: '#7a8593',
          todo: '#4a9fd4',
          doing: '#f2a41c',
          done: '#4bbd6b',
          trash: '#df5140',
        },

        // === Legacy scale names, remapped to a light-neutral ramp ===
        // Retained so existing markup (bg-steel-*, text-enamel-*) keeps working
        // without a full class rename. Prefer the canonical tokens above in new
        // code. steel = surfaces/borders, enamel = text.
        steel: {
          950: '#ffffff',
          900: '#ffffff',
          850: '#ffffff',
          800: '#ffffff',
          700: '#ececec',
          600: '#e2e2e2',
          500: '#cfcfcf',
          400: '#999999',
        },
        enamel: {
          DEFAULT: '#1a1a1a',
          dim: '#5c5c5c',
          faint: '#767676',
        },
      },
      fontFamily: {
        // Portfolio families: Montserrat (headings/labels) + Raleway (body).
        head: ['Montserrat', 'system-ui', 'sans-serif'],
        body: ['Raleway', 'system-ui', 'sans-serif'],
        // Legacy aliases → mapped onto the two portfolio families.
        stencil: ['Montserrat', 'system-ui', 'sans-serif'],
        placard: ['Montserrat', 'system-ui', 'sans-serif'],
        sans: ['Raleway', 'system-ui', 'sans-serif'],
        // No mono in the portfolio — numeric readouts use Montserrat + tnum.
        mono: ['Montserrat', 'system-ui', 'sans-serif'],
      },
      borderRadius: {
        // Portfolio radius scale
        sm: '8px',
        md: '16px',
        lg: '24px',
        pill: '999px',
      },
      boxShadow: {
        // Portfolio elevation scale
        sm: '0 2px 10px rgba(0,0,0,0.06)',
        md: '0 12px 30px rgba(0,0,0,0.08)',
        lg: '0 20px 45px rgba(0,0,0,0.14)',
        // Legacy aliases → portfolio elevation
        cell: '0 2px 10px rgba(0,0,0,0.06)',
        raised: '0 12px 30px rgba(0,0,0,0.10)',
        console: '0 2px 10px rgba(0,0,0,0.06)',
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
