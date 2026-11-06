/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        primary: '#1e3a5f',
        ink: '#1c1917',
        paper: '#f3f0e8',
      },
      fontFamily: {
        sans: ['"Source Sans 3"', 'ui-sans-serif', 'system-ui', 'sans-serif'],
        serif: ['Newsreader', 'Georgia', 'serif'],
      },
      maxWidth: {
        page: '68rem',
      },
    },
  },
  plugins: [],
}
